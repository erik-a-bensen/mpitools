from .base import comm, rank
from collections.abc import Callable
from functools import wraps

# MPI tools for dividing work among processes
def main_process(func: Callable) -> Callable:
    """
    Decorator to ensure a function runs only on the main process (rank 0).
    
    Args:
        func (callable): The function to wrap.
        
    Returns:
        callable: The wrapped function that runs only on rank 0.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if rank == 0:
            return func(*args, **kwargs)
        else:
            return None
    return wrapper

def worker_process(func: Callable) -> Callable:
    """
    Decorator to ensure a function runs only on worker processes (not rank 0).
    
    Args:
        func (callable): The function to wrap.
        
    Returns:
        callable: The wrapped function that runs only on worker processes.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if rank != 0:
            return func(*args, **kwargs)
        else:
            return None
    return wrapper

# Evaluate on main and broadcast results to workers
def broadcast_main(func: Callable) -> Callable:
    """
    Decorator to run a function on the main process and broadcast the result to all workers.
    
    Args:
        func (callable): The function to wrap.
        
    Returns:
        callable: The wrapped function that runs on rank 0 and broadcasts the result.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        if rank == 0:
            result = func(*args, **kwargs)
        return comm.bcast(result, root=0)
    return wrapper

# Evaluate on all processes and gather results on the main process
def gather_main(func: Callable) -> Callable:
    """
    Decorator to run a function on all processes and gather results on the main process.
    
    Args:
        func (callable): The function to wrap.
        
    Returns:
        callable: The wrapped function that gathers results on rank 0.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return comm.gather(result, root=0)
    return wrapper