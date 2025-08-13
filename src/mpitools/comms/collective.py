from mpi4py.MPI import Comm, COMM_WORLD
from collections.abc import Callable
from functools import wraps 
  
# Broadcast decorators
def broadcast_from_main(comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on rank 0 and broadcasts result to all processes.
    
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
    Function runs only on rank 0, result is broadcast to all ranks using comm.bcast().
    All processes receive the same return value.
    """
    rank = comm.Get_rank()
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            if rank == 0:
                result = func(*args, **kwargs)
            return comm.bcast(result, root=0)
        return wrapper
    return decorator

def broadcast_from_process(process_rank: int, comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on specified rank and broadcasts result to all processes.
    
    Parameters
    ----------
    process_rank : int
        Rank of the process that should execute the function and broadcast result.
    comm : MPI.Comm, optional
        MPI communicator. Defaults to COMM_WORLD.
    
    Returns
    -------
    Callable
        Decorator function.
    
    Notes
    -----
    Function runs only on the specified rank, result is broadcast to all ranks.
    All processes receive the same return value.
    """
    rank = comm.Get_rank()
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            if rank == process_rank:
                result = func(*args, **kwargs)
            return comm.bcast(result, root=process_rank)
        return wrapper
    return decorator

# Scatter decorators
def scatter_from_main(comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on rank 0 and scatters results to all processes.
    
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
    Function runs only on rank 0, results are scattered to all ranks using comm.scatter().
    Each process receives a portion of the result.
    """
    rank = comm.Get_rank()
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            if rank == 0:
                result = func(*args, **kwargs)
            return comm.scatter(result, root=0)
        return wrapper
    return decorator

def scatter_from_process(process_rank: int, comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on specified rank and scatters results to all processes.
    
    Parameters
    ----------
    process_rank : int
        Rank of the process that should execute the function and scatter results.
    comm : MPI.Comm, optional
        MPI communicator. Defaults to COMM_WORLD.
    
    Returns
    -------
    Callable
        Decorator function.
    
    Notes
    -----
    Function runs only on the specified rank, results are scattered to all ranks.
    Each process receives a portion of the result.
    """
    rank = comm.Get_rank()
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            if rank == process_rank:
                result = func(*args, **kwargs)
            return comm.scatter(result, root=process_rank)
        return wrapper
    return decorator

# Gather decorators
def gather_to_main(comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on all processes and gathers results to rank 0.
    
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
    Function runs on all processes, results are gathered to rank 0 using comm.gather().
    Rank 0 receives a list of all results, other ranks receive None.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return comm.gather(result, root=0)
        return wrapper
    return decorator

def gather_to_process(process_rank: int, comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on all processes and gathers results to specified rank.
    
    Parameters
    ----------
    process_rank : int
        Rank of the process that should receive gathered results.
    comm : MPI.Comm, optional
        MPI communicator. Defaults to COMM_WORLD.
    
    Returns
    -------
    Callable
        Decorator function.
    
    Notes
    -----
    Function runs on all processes, results are gathered to specified rank.
    The specified rank receives a list of all results, other ranks receive None.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return comm.gather(result, root=process_rank)
        return wrapper
    return decorator

def gather_to_all(comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on all processes and gathers results to all processes.
    
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
    Function runs on all processes, results are gathered to all ranks using comm.allgather().
    All processes receive a list of all results.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return comm.allgather(result)
        return wrapper
    return decorator

# All to all decorator 
def all_to_all(comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on all processes and exchanges results between all processes.
    
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
    Function runs on all processes, results are exchanged between all ranks using comm.alltoall().
    Each process receives a list of results from all other processes.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return comm.alltoall(result)
        return wrapper
    return decorator
