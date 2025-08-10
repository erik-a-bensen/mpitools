from mpi4py.MPI import Comm, COMM_WORLD
from collections.abc import Callable
from functools import wraps

# MPI tools for dividing work among processes
def eval_on_main(comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that only executes function on rank 0 (main process).
    
    Parameters
    ----------
    comm : MPI.Comm, optional
        MPI communicator. Defaults to COMM_WORLD.
    
    Returns
    -------
    Callable
        Decorator function.
    
    Notes
    -----
    Function runs only on rank 0, returns None on all other ranks.
    """
    rank = comm.Get_rank()
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if rank == 0:
                return func(*args, **kwargs)
            else:
                return None
        return wrapper
    return decorator

def eval_on_workers(comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that only executes function on worker processes (rank != 0).
    
    Parameters
    ----------
    comm : MPI.Comm, optional
        MPI communicator. Defaults to COMM_WORLD.
    
    Returns
    -------
    Callable
        Decorator function.
    
    Notes
    -----
    Function runs only on ranks 1, 2, ..., n-1, returns None on rank 0.
    """
    rank = comm.Get_rank()
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if rank != 0:
                return func(*args, **kwargs)
            else:
                return None
        return wrapper
    return decorator

def eval_on_single(process_rank: int, comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that only executes function on a specific process rank.
    
    Parameters
    ----------
    process_rank : int
        Rank of the process that should execute the function.
    comm : MPI.Comm, optional
        MPI communicator. Defaults to COMM_WORLD.
    
    Returns
    -------
    Callable
        Decorator function.
    
    Notes
    -----
    Function runs only on the specified rank, returns None on all other ranks.
    """
    rank = comm.Get_rank()
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if rank == process_rank:
                return func(*args, **kwargs)
            else:
                return None
        return wrapper
    return decorator

def eval_on_select(process_ranks: list[int], comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that only executes function on selected process ranks.
    
    Parameters
    ----------
    process_ranks : list[int]
        List of ranks that should execute the function.
    comm : MPI.Comm, optional
        MPI communicator. Defaults to COMM_WORLD.
    
    Returns
    -------
    Callable
        Decorator function.
    
    Notes
    -----
    Function runs only on ranks in process_ranks, returns None on all other ranks.
    """
    rank = comm.Get_rank()
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if rank in process_ranks:
                return func(*args, **kwargs)
            else:
                return None
        return wrapper
    return decorator