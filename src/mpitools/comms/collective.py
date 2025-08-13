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

    Decorated Function Requirements
    -------------------------------
    The decorated function can return any pickle-able Python object.
    
    Decorated Function Returns
    --------------------------
    The broadcast result from rank 0, available on all processes.

    Notes
    -----
    Decorated function only runs on the main process.
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

    Decorated Function Requirements
    -------------------------------
    The decorated function can return any pickle-able Python object.
    
    Decorated Function Returns
    --------------------------
    The broadcast result from the specified rank, available on all processes.

    Notes
    -----
    Decorated function only runs on the specified process.
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

    Decorated Function Requirements
    -------------------------------
    The decorated function should return a sequence (list, tuple, etc.) with length equal to the number of processes.
    
    Decorated Function Returns
    --------------------------
    One element from the sequence, assigned to each process based on its rank.

    Notes
    -----
    Decorated function only runs on the main process.
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

    Decorated Function Requirements
    -------------------------------
    The decorated function should return a sequence (list, tuple, etc.) with length equal to the number of processes.
    
    Decorated Function Returns
    --------------------------
    One element from the sequence, assigned to each process based on its rank.

    Notes
    -----
    Decorated function only runs on the specified process.
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

    Decorated Function Requirements
    -------------------------------
    The decorated function can return any pickle-able Python object.
    
    Decorated Function Returns
    --------------------------
    On rank 0: List containing results from all processes.
    On other ranks: None.

    Notes
    -----
    Decorated function runs on all processes.
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

    Decorated Function Requirements
    -------------------------------
    The decorated function can return any pickle-able Python object.
    
    Decorated Function Returns
    --------------------------
    On specified rank: List containing results from all processes.
    On other ranks: None.

    Notes
    -----
    Decorated function runs on all processes.
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

    Decorated Function Requirements
    -------------------------------
    The decorated function can return any pickle-able Python object.
    
    Decorated Function Returns
    --------------------------
    List containing results from all processes, available on all processes.

    Notes
    -----
    Decorated function runs on all processes.
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

    Decorated Function Requirements
    -------------------------------
    The decorated function should return a sequence (list, tuple, etc.) with length equal to the number of processes.
    
    Decorated Function Returns
    --------------------------
    List containing one element from each process, with element order corresponding to process rank.

    Notes
    -----
    Decorated function runs on all processes.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return comm.alltoall(result)
        return wrapper
    return decorator