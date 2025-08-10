from mpi4py.MPI import Comm, COMM_WORLD
import sys
from collections.abc import Callable
from functools import wraps
import traceback

def setup_mpi() -> tuple[Comm, int, int]:
    """
    Initialize MPI and return the communicator, rank, and size.
    
    Returns:
        tuple: A tuple containing the MPI communicator, rank, and size.
    """
    comm = COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    return comm, rank, size

def abort_on_error(exception_type: Exception = Exception, comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that aborts all MPI processes when an exception occurs.
    
    Parameters
    ----------
    exception_type : Exception, optional
        Type of exception to catch. Defaults to Exception (all exceptions).
    comm : MPI.Comm, optional
        MPI communicator to abort. Defaults to COMM_WORLD.
    
    Returns
    -------
    Callable
        Decorator function.
    
    Notes
    -----
    Prints error traceback and calls comm.Abort(1) to terminate all processes.
    """
    rank = comm.Get_rank()
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception_type:
                print(f"Error in process {rank}")
                print(traceback.format_exc())
                comm.Abort(1)
                sys.exit(1)
        return wrapper
    return decorator
