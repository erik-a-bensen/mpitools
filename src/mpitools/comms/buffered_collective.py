import numpy as np
from mpi4py import MPI
from mpi4py.MPI import Comm, COMM_WORLD
from collections.abc import Callable
from functools import wraps
from typing import Tuple
from mpitools.comms.utils import to_mpi_dtype, build_buffer

# Buffered broadcast decorators
def buffered_broadcast_from_main(shape: int | Tuple[int, ...], dtype: np.dtype, comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on rank 0 and broadcasts result to all processes.
    
    Parameters
    ----------
    shape : int or tuple of ints
        Shape of the data buffer to broadcast.
    dtype : numpy.dtype
        Data type of the buffer.
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
    Buffer containing the broadcast data on all processes.

    Notes
    -----
    Decorated function only runs on the main process.
    """
    rank = comm.Get_rank()
    if isinstance(shape, int):
        shape = (shape,)
    
    mpi_dtype = to_mpi_dtype(dtype)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Allocate buffer on all processes
            buff = build_buffer(shape, dtype)
            
            if rank == 0:
                # Execute function and get result
                result = func(*args, **kwargs)
                
                # Copy to buffer
                buff[:] = result
            
            # Broadcast buffer from rank 0
            comm.Bcast([buff, mpi_dtype], root=0)
            
            return buff
        return wrapper
    return decorator

def buffered_broadcast_from_process(process_rank: int, shape: int | Tuple[int, ...], dtype: np.dtype, comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on specified rank and broadcasts result to all processes.
    
    Parameters
    ----------
    process_rank : int
        Rank of the process that should execute the function and broadcast result.
    shape : int or tuple of ints
        Shape of the data buffer to broadcast.
    dtype : numpy.dtype
        Data type of the buffer.
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
    Buffer containing the broadcast data on all processes.

    Notes
    -----
    Decorated function only runs on the specified process.
    """
    rank = comm.Get_rank()
    if isinstance(shape, int):
        shape = (shape,)
    
    mpi_dtype = to_mpi_dtype(dtype)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            buff = build_buffer(shape, dtype)
            
            if rank == process_rank:
                result = func(*args, **kwargs)
                buff[:] = result
            
            comm.Bcast([buff, mpi_dtype], root=process_rank)
            return buff
        return wrapper
    return decorator

# Buffered scatter decorator
def buffered_scatter_from_main(chunk_shape: int | Tuple[int, ...], dtype: np.dtype, comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on rank 0 and scatters results to all processes.
    
    Parameters
    ----------
    chunk_shape : int or tuple of ints
        Shape of each chunk to be scattered to each process.
    dtype : numpy.dtype
        Data type of the buffer.
    comm : MPI.Comm, optional
        MPI communicator. Defaults to COMM_WORLD.
    
    Returns
    -------
    Callable
        Decorator function.

    Decorated Function Requirements
    -------------------------------
    The decorated function should return a numpy array with shape (num_processes, *chunk_shape) and the specified dtype.
    
    Decorated Function Returns
    --------------------------
    Buffer containing the scattered chunk assigned to each process.

    Notes
    -----
    Decorated function only runs on the main process.
    """
    rank = comm.Get_rank()
    
    if isinstance(chunk_shape, int):
        chunk_shape = (chunk_shape,)
    
    mpi_dtype = to_mpi_dtype(dtype)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Allocate receive buffer on all processes
            recv_buff = build_buffer(chunk_shape, dtype)
            
            if rank == 0:
                # Execute function and prepare send buffer
                result = func(*args, **kwargs)
                send_buff = result
            else:
                send_buff = None
            
            # Scatter data
            comm.Scatter([send_buff, mpi_dtype], [recv_buff, mpi_dtype], root=0)
            
            return recv_buff
        return wrapper
    return decorator

def buffered_scatter_from_process(process_rank: int, chunk_shape: int | Tuple[int, ...], dtype: np.dtype, comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on specified rank and scatters results to all processes.
    
    Parameters
    ----------
    process_rank : int
        Rank of the process that should execute the function and scatter results.
    chunk_shape : int or tuple of ints
        Shape of each chunk to be scattered to each process.
    dtype : numpy.dtype
        Data type of the buffer.
    comm : MPI.Comm, optional
        MPI communicator. Defaults to COMM_WORLD.
    
    Returns
    -------
    Callable
        Decorator function.

    Decorated Function Requirements
    -------------------------------
    The decorated function should return a numpy array with shape (num_processes, *chunk_shape) and the specified dtype.
    
    Decorated Function Returns
    --------------------------
    Buffer containing the scattered chunk assigned to each process.

    Notes
    -----
    Decorated function only runs on the specified process.
    """
    rank = comm.Get_rank()
    
    if isinstance(chunk_shape, int):
        chunk_shape = (chunk_shape,)
    
    mpi_dtype = to_mpi_dtype(dtype)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Allocate receive buffer on all processes
            recv_buff = build_buffer(chunk_shape, dtype)
            
            if rank == process_rank:
                # Execute function and prepare send buffer
                result = func(*args, **kwargs)
                send_buff = result
            else:
                send_buff = None
            
            # Scatter data
            comm.Scatter([send_buff, mpi_dtype], [recv_buff, mpi_dtype], root=process_rank)
            
            return recv_buff
        return wrapper
    return decorator

# Buffered gather decorators
def buffered_gather_to_process(process_rank: int, shape: int | Tuple[int, ...], dtype: np.dtype, comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on all processes and gathers results to specified rank.
    
    Parameters
    ----------
    process_rank : int
        Rank of the process that should receive gathered results.
    shape : int or tuple of ints
        Shape of data from each process.
    dtype : numpy.dtype
        Data type of the buffer.
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
    On specified rank: Buffer with shape (num_processes, *shape) containing all gathered data.
    On other ranks: None.

    Notes
    -----
    Decorated function runs on all processes.
    """
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    if isinstance(shape, int):
        shape = (shape,)
    
    mpi_dtype = to_mpi_dtype(dtype)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Execute function on all processes
            result = func(*args, **kwargs)
            
            send_buff = result
            
            # Prepare receive buffer only on specified rank
            if rank == process_rank:
                recv_buff = build_buffer((size,) + shape, dtype)
            else:
                recv_buff = None
            
            # Gather data to specified rank
            comm.Gather([send_buff, mpi_dtype], [recv_buff, mpi_dtype], root=process_rank)
            
            return recv_buff
        return wrapper
    return decorator

def buffered_gather_to_all(shape: int | Tuple[int, ...], dtype: np.dtype, comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on all processes and gathers results to all processes.
    
    Parameters
    ----------
    shape : int or tuple of ints
        Shape of data from each process.
    dtype : numpy.dtype
        Data type of the buffer.
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
    Buffer with shape (num_processes, *shape) containing all gathered data on all processes.

    Notes
    -----
    Decorated function runs on all processes.
    """
    size = comm.Get_size()
    
    if isinstance(shape, int):
        shape = (shape,)
    
    mpi_dtype = to_mpi_dtype(dtype)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Execute function on all processes
            result = func(*args, **kwargs)
            
            send_buff = result
            recv_buff = build_buffer((size,) + shape, dtype)
            
            # Gather data to all processes
            comm.Allgather([send_buff, mpi_dtype], [recv_buff, mpi_dtype])
            
            return recv_buff
        return wrapper
    return decorator

# Buffered gather decorator
def buffered_gather_to_main(shape: int | Tuple[int, ...], dtype: np.dtype, comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on all processes and gathers results to rank 0.
    
    Parameters
    ----------
    shape : int or tuple of ints
        Shape of data from each process.
    dtype : numpy.dtype
        Data type of the buffer.
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
    On rank 0: Buffer with shape (num_processes, *shape) containing all gathered data.
    On other ranks: None.

    Notes
    -----
    Decorated function runs on all processes.
    """
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    if isinstance(shape, int):
        shape = (shape,)
    
    mpi_dtype = to_mpi_dtype(dtype)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Execute function on all processes
            result = func(*args, **kwargs)
            
            send_buff = result
            
            # Prepare receive buffer only on rank 0
            if rank == 0:
                recv_buff = build_buffer((size,) + shape, dtype)
            else:
                recv_buff = None
            
            # Gather data to rank 0
            comm.Gather([send_buff, mpi_dtype], [recv_buff, mpi_dtype], root=0)
            
            return recv_buff
        return wrapper
    return decorator

# All to all decorator
def buffered_all_to_all(element_shape: int | Tuple[int, ...], dtype: np.dtype, comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on all processes and exchanges results between all processes.
    
    Parameters
    ----------
    element_shape : int or tuple of ints
        Shape of data element being sent to each process.
    dtype : numpy.dtype
        Data type of the buffer.
    comm : MPI.Comm, optional
        MPI communicator. Defaults to COMM_WORLD.
    
    Returns
    -------
    Callable
        Decorator function.

    Decorated Function Requirements
    -------------------------------
    The decorated function should return a numpy array with shape (num_processes, *element_shape) and the specified dtype.
    
    Decorated Function Returns
    --------------------------
    Buffer with shape (num_processes, *element_shape) containing exchanged data from all processes.

    Notes
    -----
    Decorated function runs on all processes.
    """
    size = comm.Get_size()
    
    if isinstance(element_shape, int):
        element_shape = (element_shape,)
    
    mpi_dtype = to_mpi_dtype(dtype)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Execute function on all processes
            result = func(*args, **kwargs)
            
            send_buff = result
            recv_buff = build_buffer((size,) + element_shape, dtype)
            
            # All-to-all exchange
            comm.Alltoall([send_buff, mpi_dtype], [recv_buff, mpi_dtype])
            
            return recv_buff
        return wrapper
    return decorator

# Example usage and testing functions
if __name__ == "__main__":
    # Example 1: Simple buffered broadcast
    @buffered_broadcast_from_main(shape=(5,), dtype=np.float64)
    def get_coefficients():
        """Generate some coefficients on rank 0."""
        return np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    
    # Example 2: Scatter large array chunks
    @buffered_scatter_from_main(chunk_shape=(100,), dtype=np.float32)
    def distribute_work():
        """Create work chunks for each process."""
        size = MPI.COMM_WORLD.Get_size()
        # Each process gets 100 random numbers
        return np.random.random((size, 100)).astype(np.float32)
    
    # Example 3: Gather results
    @buffered_gather_to_main(shape=(10,), dtype=np.int32)
    def compute_local_result():
        """Each process computes some local result."""
        rank = MPI.COMM_WORLD.Get_rank()
        return np.arange(rank * 10, (rank + 1) * 10, dtype=np.int32)
    
    # Example 4: Scatter from specific process
    @buffered_scatter_from_process(process_rank=1, chunk_shape=(20,), dtype=np.float32)
    def distribute_from_process_1():
        """Process 1 distributes work chunks."""
        rank = MPI.COMM_WORLD.Get_rank()
        size = MPI.COMM_WORLD.Get_size()
        if rank == 1:
            return np.random.random((size, 20)).astype(np.float32)
    
    # Example 5: Gather to specific process
    @buffered_gather_to_process(process_rank=2, shape=(8,), dtype=np.int64)
    def gather_to_process_2():
        """Gather results to process 2."""
        rank = MPI.COMM_WORLD.Get_rank()
        return np.arange(rank * 8, (rank + 1) * 8, dtype=np.int64)
    
    # Example 6: Gather to all processes
    @buffered_gather_to_all(shape=(6,), dtype=np.float32)
    def gather_everywhere():
        """All processes get all results."""
        rank = MPI.COMM_WORLD.Get_rank()
        return np.full(6, rank, dtype=np.float32)
    
    # Example 7: All-to-all exchange
    @buffered_all_to_all(element_shape=(5,), dtype=np.float64)
    def exchange_data():
        """Each process exchanges data with all other processes."""
        rank = MPI.COMM_WORLD.Get_rank()
        size = MPI.COMM_WORLD.Get_size()
        # Create data to send to each process
        data = np.zeros((size, 5))
        for i in range(size):
            data[i] = rank * 100 + np.arange(5) + i
        return data
    
    print(f"Rank {MPI.COMM_WORLD.Get_rank()}: Examples ready to run")