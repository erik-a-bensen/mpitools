import time
from abc import ABC, abstractmethod
from typing import Any

class Task(ABC):
    """
    Abstract base class for tasks.
    Users should inherit from this class and implement the execute method.
    """
    
    def __init__(self, task_id: str, **kwargs):
        self.task_id = task_id
        self.kwargs = kwargs
        self.created_at = time.time()
        self.started_at = None
        self.completed_at = None
        self.worker_rank = None
    
    @abstractmethod
    def execute(self) -> Any:
        """
        Execute the task and return the result.
        This method must be implemented by subclasses.
        """
        pass
    
    def __str__(self):
        return f"Task({self.task_id})"

class TaskResult:
    """Container for task execution results"""
    
    def __init__(self, task_id: str, result: Any, execution_time: float = 0.0,
                 worker_rank: int = -1):
        self.task_id = task_id
        self.result = result
        self.execution_time = execution_time
        self.worker_rank = worker_rank
        self.completed_at = time.time()

    def __str__(self):
        return f"TaskResult(\n\ttask_id={self.task_id},\n\t" \
               f"worker_rank={self.worker_rank},\n\t" \
               f"execution_time={self.execution_time:.4f}s,\n\t" \
               f"result={self.result}\n)"