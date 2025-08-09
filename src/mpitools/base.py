from mpi4py import MPI
import sys
from collections.abc import Callable
from functools import wraps
import traceback

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def setup_mpi() -> tuple[MPI.Comm, int, int]:
    """
    Initialize MPI and return the communicator, rank, and size.
    
    Returns:
        tuple: A tuple containing the MPI communicator, rank, and size.
    """
    return comm, rank, size

def abort_on_error(func: Callable, exception_type: Exception = Exception) -> Callable:
    """
    Decorator to handle MPI errors by aborting the process.
    
    Args:
        func (callable): The function to wrap.
        
    Returns:
        callable: The wrapped function that aborts on error.
    """
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
