from .tasks import Task, TaskResult
from mpi4py import MPI
from mpi4py.MPI import Comm, COMM_WORLD
import time
from typing import List, Optional
from enum import Enum

class _MessageTag(Enum):
    """Message tags for MPI communication"""
    TASK_ASSIGNMENT = 1
    TASK_RESULT = 2
    SHUTDOWN = 3


class _SerialQueueManager:
    """
    Serial manager class that executes tasks sequentially on a single process.
    Used when MPI size is 1.
    """
    
    def __init__(self, comm: Comm = COMM_WORLD):
        self.task_queue: List[Task] = []
        self.completed_results = {}  # task_id -> TaskResult
    
    def add_task(self, task: Task):
        """Add a task to the queue"""
        self.task_queue.append(task)
    
    def add_tasks(self, tasks: List[Task]):
        """Add multiple tasks to the queue"""
        self.task_queue.extend(tasks)
    
    def run(self, timeout: Optional[float] = None) -> dict:
        """
        Run tasks serially on the current process.
        
        Args:
            timeout: Maximum time to wait for all tasks to complete (seconds)
            
        Returns:
            Dictionary mapping task_id to TaskResult
        """
        start_time = time.time()
        
        while self.task_queue:
            if timeout and (time.time() - start_time) > timeout:
                break
            
            # Execute task directly
            task = self.task_queue.pop(0)
            task.started_at = time.time()
            task_id = task.task_id
            
            result = self._execute_task(task)
            self.completed_results[task_id] = result
            
            # Release task memory after execution
            del task
        
        return self.completed_results
    
    def _execute_task(self, task: Task) -> TaskResult:
        """Execute a single task and return the result"""
        start_time = time.time()
        
        result = task.execute()
        execution_time = time.time() - start_time
        task.completed_at = time.time()
        
        return TaskResult(
            task_id=task.task_id,
            result=result,
            execution_time=execution_time,
            worker_rank=0  # All tasks run on rank 0 in serial mode
        )


class _MPIQueueManager:
    """
    Manager class that distributes tasks to worker processes.
    Runs on rank 0 (master process).
    """
    
    def __init__(self, comm: Comm = COMM_WORLD):
        self.comm = comm
        self.rank = comm.Get_rank()
        self.size = comm.Get_size()
        
        if self.rank != 0:
            raise ValueError("QueueManager must run on rank 0")
        
        self.task_queue: List[Task] = []
        self.pending_tasks = {}  # rank -> task_id
        self.completed_results = {}  # task_id -> TaskResult
        self.worker_ranks = list(range(1, self.size))
    
    def add_task(self, task: Task):
        """Add a task to the queue"""
        self.task_queue.append(task)
    
    def add_tasks(self, tasks: List[Task]):
        """Add multiple tasks to the queue"""
        self.task_queue.extend(tasks)
    
    def run(self, timeout: Optional[float] = None) -> dict:
        """
        Run the queue manager, distributing tasks and collecting results.
        
        Args:
            timeout: Maximum time to wait for all tasks to complete (seconds)
            
        Returns:
            Dictionary mapping task_id to TaskResult
        """
        start_time = time.time()
        
        # Distribute initial tasks to all workers
        self._distribute_initial_tasks()
        
        # Main execution loop - wait for results and send next tasks
        while self.pending_tasks:
            if timeout and (time.time() - start_time) > timeout:
                break
            
            # Wait for any worker to return a result
            status = MPI.Status()
            result = self.comm.recv(source=MPI.ANY_SOURCE, tag=_MessageTag.TASK_RESULT.value, status=status)
            worker_rank = status.Get_source()
            
            # Store the result
            task_id = self.pending_tasks.pop(worker_rank)
            self.completed_results[task_id] = result
            
            # Send next task to this worker if available
            if self.task_queue:
                task = self.task_queue.pop(0)
                task.started_at = time.time()
                task.worker_rank = worker_rank
                task_id = task.task_id
                
                self.comm.send(task, dest=worker_rank, tag=_MessageTag.TASK_ASSIGNMENT.value)
                self.pending_tasks[worker_rank] = task_id
                
                # Release task memory after sending
                del task
        
        # Shutdown workers
        self._shutdown_workers()
        
        return self.completed_results
    
    def _distribute_initial_tasks(self):
        """Distribute initial tasks to all available workers"""
        for worker_rank in self.worker_ranks:
            if self.task_queue:
                task = self.task_queue.pop(0)
                task.started_at = time.time()
                task.worker_rank = worker_rank
                
                # Send task to worker
                self.comm.send(task, dest=worker_rank, tag=_MessageTag.TASK_ASSIGNMENT.value)
                self.pending_tasks[worker_rank] = task.task_id
    
    def _shutdown_workers(self):
        """Send shutdown signals to all workers"""
        for worker_rank in self.worker_ranks:
            self.comm.send(None, dest=worker_rank, tag=_MessageTag.SHUTDOWN.value)


class _MPIQueueWorker:
    """
    Worker class that executes tasks.
    Runs on worker processes (rank > 0).
    """
    
    def __init__(self, comm: Comm = COMM_WORLD):
        self.comm = comm
        self.rank = comm.Get_rank()
        
        if self.rank == 0:
            raise ValueError("Worker cannot run on rank 0")
    
    def run(self):
        """Main worker loop - wait for tasks and execute them"""
        while True:
            # Wait for a message from manager
            status = MPI.Status()
            message = self.comm.recv(source=0, tag=MPI.ANY_TAG, status=status)
            
            if status.Get_tag() == _MessageTag.SHUTDOWN.value:
                break
            elif status.Get_tag() == _MessageTag.TASK_ASSIGNMENT.value:
                task = message
                result = self._execute_task(task)
                
                # Send result back to manager
                self.comm.send(result, dest=0, tag=_MessageTag.TASK_RESULT.value)
    
    def _execute_task(self, task: Task) -> TaskResult:
        """Execute a single task and return the result"""
        start_time = time.time()
        
        result = task.execute()
        execution_time = time.time() - start_time
        task.completed_at = time.time()
        
        return TaskResult(
            task_id=task.task_id,
            result=result,
            execution_time=execution_time,
            worker_rank=self.rank
        )


class MPIQueue:
    """
    Interface for the MPI queue system.
    Automatically determines whether to run as manager or worker based on rank.
    If running on a single process (size 1), uses serial execution.
    """
    
    def __init__(self, comm: Comm = COMM_WORLD):
        self.comm = comm
        self.rank = comm.Get_rank()
        self.size = comm.Get_size()
        self.manager = None
        self.worker = None
        
        if self.size == 1:
            self.manager = _SerialQueueManager(comm)
        elif self.rank == 0:
            self.manager = _MPIQueueManager(comm)
        else:
            self.worker = _MPIQueueWorker(comm)
    
    def add_task(self, task: Task):
        """Add a task to the queue (only valid on manager)"""
        if self.rank != 0:
            raise RuntimeError("Tasks can only be added on the manager process (rank 0)")
        self.manager.add_task(task)
    
    def add_tasks(self, tasks: List[Task]):
        """Add multiple tasks to the queue (only valid on manager)"""
        if self.rank != 0:
            raise RuntimeError("Tasks can only be added on the manager process (rank 0)")
        self.manager.add_tasks(tasks)
    
    def run(self, timeout: Optional[float] = None) -> dict[str, TaskResult]:
        """
        Run the queue system.
        
        For manager (rank 0): distributes tasks and returns results
        For workers (rank > 0): executes tasks until shutdown
        
        Returns:
            Dictionary of results indexed by task_id (only on manager), None on workers
        """
        if self.rank == 0:
            return self.manager.run(timeout)
        else:
            self.worker.run()
            return None
