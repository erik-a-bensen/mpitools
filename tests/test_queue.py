from mpitools.queue import MPIQueue, Task
from mpitools import setup_mpi
import time

comm, rank, size = setup_mpi()

# Example usage and custom task implementations
class ComputeTask(Task):
    """Example task that performs some computation"""
    
    def __init__(self, task_id: str, operation: str, *args, **kwargs):
        super().__init__(task_id, **kwargs)
        self.operation = operation
        self.args = args
    
    def execute(self):
        if self.operation == "square":
            return self.args[0] ** 2
        elif self.operation == "fibonacci":
            return self._fibonacci(self.args[0])
        elif self.operation == "sleep":
            time.sleep(self.args[0])
            return f"Slept for {self.args[0]} seconds"
        else:
            raise ValueError(f"Unknown operation: {self.operation}")
    
    def _fibonacci(self, n):
        if n <= 1:
            return n
        return self._fibonacci(n-1) + self._fibonacci(n-2)


if __name__ == "__main__":
    # Example usage
    queue = MPIQueue()
    
    if rank == 0:
        # Create some example tasks
        tasks = [
            ComputeTask("square_1", "square", 5),
            ComputeTask("square_2", "square", 10),
            ComputeTask("fib_1", "fibonacci", 20),
            ComputeTask("fib_2", "fibonacci", 25),
            ComputeTask("sleep_1", "sleep", 1),
            ComputeTask("sleep_2", "sleep", 2),
        ]
        
        queue.add_tasks(tasks)
        print(f"Added {len(tasks)} tasks to queue")
        
    
    results = queue.run(timeout=30)

    if rank == 0:
        # Print results
        print("\nResults:")
        for task_id, result in results.items():
            print(f"  {task_id}: {result.result} (worker {result.worker_rank}, {result.execution_time:.3f}s)")