import numpy as np
from mpi4py import MPI
from mpi4py.MPI import Comm, COMM_WORLD, Op
from collections.abc import Callable
from functools import wraps
from typing import Tuple
from mpitools.comms.utils import to_mpi_dtype, build_buffer, to_mpi_op

# Buffered reduce decorators
def buffered_reduce_to_main(shape: int | Tuple[int, ...], dtype: np.dtype, op: str | Op = 'sum', comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on all processes and reduces results to rank 0.
    
    Parameters
    ----------
    shape : int or tuple of ints
        Shape of the data buffer for reduction.
    dtype : numpy.dtype
        Data type of the buffer.
    op : str or MPI.Op, optional
        Reduction operation to apply. Defaults to 'sum'.
        String options: 'sum', 'prod', 'max', 'min', 'land', 'band', 'lor', 'bor', 
        'lxor', 'bxor', 'maxloc', 'minloc'.
    comm : MPI.Comm, optional
        MPI communicator. Defaults to COMM_WORLD.
    
    Returns
    -------
    Callable
        Decorator function.

    Decorated Function Requirements
    -------------------------------
    The decorated function should return a numpy array with the specified shape and dtype.
    
    Decorated Function Returns
    --------------------------
    On rank 0: Buffer containing the reduced result from all processes.
    On other ranks: None.

    Notes
    -----
    Decorated function runs on all processes.
    """
    rank = comm.Get_rank()
    
    if isinstance(shape, int):
        shape = (shape,)
    
    op = to_mpi_op(op)
    
    mpi_dtype = to_mpi_dtype(dtype)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Execute function on all processes
            result = func(*args, **kwargs)
            
            send_buff = result
            
            # Prepare receive buffer only on rank 0
            if rank == 0:
                recv_buff = build_buffer(shape, dtype)
            else:
                recv_buff = None
            
            # Reduce data to rank 0
            comm.Reduce([send_buff, mpi_dtype], [recv_buff, mpi_dtype], op=op, root=0)
            
            return recv_buff
        return wrapper
    return decorator

def buffered_reduce_to_process(process_rank: int, shape: int | Tuple[int, ...], dtype: np.dtype, op: str | Op = 'sum', comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on all processes and reduces results to specified rank.
    
    Parameters
    ----------
    process_rank : int
        Rank of the process that should receive the reduced result.
    shape : int or tuple of ints
        Shape of the data buffer for reduction.
    dtype : numpy.dtype
        Data type of the buffer.
    op : str or MPI.Op, optional
        Reduction operation to apply. Defaults to 'sum'.
        String options: 'sum', 'prod', 'max', 'min', 'land', 'band', 'lor', 'bor', 
        'lxor', 'bxor', 'maxloc', 'minloc'.
    comm : MPI.Comm, optional
        MPI communicator. Defaults to COMM_WORLD.
    
    Returns
    -------
    Callable
        Decorator function.

    Decorated Function Requirements
    -------------------------------
    The decorated function should return a numpy array with the specified shape and dtype.
    
    Decorated Function Returns
    --------------------------
    On specified rank: Buffer containing the reduced result from all processes.
    On other ranks: None.

    Notes
    -----
    Decorated function runs on all processes.
    """
    rank = comm.Get_rank()
    
    if isinstance(shape, int):
        shape = (shape,)
    
    op = to_mpi_op(op)
    
    mpi_dtype = to_mpi_dtype(dtype)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Execute function on all processes
            result = func(*args, **kwargs)
            
            send_buff = result
            
            # Prepare receive buffer only on specified rank
            if rank == process_rank:
                recv_buff = build_buffer(shape, dtype)
            else:
                recv_buff = None
            
            # Reduce data to specified rank
            comm.Reduce([send_buff, mpi_dtype], [recv_buff, mpi_dtype], op=op, root=process_rank)
            
            return recv_buff
        return wrapper
    return decorator

def buffered_reduce_to_all(shape: int | Tuple[int, ...], dtype: np.dtype, op: str | Op = 'sum', comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on all processes and reduces results to all processes.
    
    Parameters
    ----------
    shape : int or tuple of ints
        Shape of the data buffer for reduction.
    dtype : numpy.dtype
        Data type of the buffer.
    op : str or MPI.Op, optional
        Reduction operation to apply. Defaults to 'sum'.
        String options: 'sum', 'prod', 'max', 'min', 'land', 'band', 'lor', 'bor', 
        'lxor', 'bxor', 'maxloc', 'minloc'.
    comm : MPI.Comm, optional
        MPI communicator. Defaults to COMM_WORLD.
    
    Returns
    -------
    Callable
        Decorator function.

    Decorated Function Requirements
    -------------------------------
    The decorated function should return a numpy array with the specified shape and dtype.
    
    Decorated Function Returns
    --------------------------
    Buffer containing the reduced result from all processes, available on all processes.

    Notes
    -----
    Decorated function runs on all processes.
    """
    if isinstance(shape, int):
        shape = (shape,)
    
    op = to_mpi_op(op)
    
    mpi_dtype = to_mpi_dtype(dtype)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Execute function on all processes
            result = func(*args, **kwargs)
            
            send_buff = result
            recv_buff = build_buffer(shape, dtype)
            
            # Reduce data to all processes
            comm.Allreduce([send_buff, mpi_dtype], [recv_buff, mpi_dtype], op=op)
            
            return recv_buff
        return wrapper
    return decorator

# Example usage and testing functions
if __name__ == "__main__":
    # Example 1: Sum reduction to main
    @buffered_reduce_to_main(shape=(10,), dtype=np.float64, op='sum')
    def compute_local_data():
        """Each process computes local data to be summed."""
        rank = MPI.COMM_WORLD.Get_rank()
        return np.full(10, rank + 1, dtype=np.float64)  # Process i contributes i+1
    
    # Example 2: Max reduction to specific process
    @buffered_reduce_to_process(process_rank=1, shape=(5,), dtype=np.int32, op='max')
    def find_local_max():
        """Find maximum across all processes."""
        rank = MPI.COMM_WORLD.Get_rank()
        return np.arange(rank * 5, (rank + 1) * 5, dtype=np.int32)
    
    # Example 3: Product reduction to all processes
    @buffered_reduce_to_all(shape=(3,), dtype=np.float32, op='prod')
    def multiply_contributions():
        """Each process contributes to product."""
        rank = MPI.COMM_WORLD.Get_rank()
        return np.array([2.0, 1.5, 1.0], dtype=np.float32) + rank * 0.1
    
    # Example 4: Custom MPI operation
    @buffered_reduce_to_all(shape=(1,), dtype=np.float64, op=MPI.MIN)
    def find_global_minimum():
        """Find global minimum value."""
        rank = MPI.COMM_WORLD.Get_rank()
        return np.array([rank * rank + 1.0], dtype=np.float64)
    
    print(f"Rank {MPI.COMM_WORLD.Get_rank()}: Buffered reduction decorators ready")