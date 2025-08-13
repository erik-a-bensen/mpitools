import numpy as np
from mpi4py import MPI
from mpi4py.MPI import Comm, COMM_WORLD
from collections.abc import Callable
from functools import wraps
from typing import Sequence
from mpitools.comms.utils import to_mpi_dtype, build_buffer

# Buffered variable scatter decorators
def variable_scatter_from_main(counts: Sequence[int], dtype: np.dtype, comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on rank 0 and scatters variable-sized results to all processes.
    
    Parameters
    ----------
    counts : sequence of ints
        Number of elements to send to each process.
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
    The decorated function should return a 1D numpy array with size sum(counts) and the specified dtype.
    
    Decorated Function Returns
    --------------------------
    Buffer containing the variable-sized chunk assigned to each process based on counts array.

    Notes
    -----
    Decorated function only runs on the main process.
    """
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    counts = list(counts)
    if len(counts) != size:
        raise ValueError(f"counts length {len(counts)} must equal number of processes {size}")
    
    # Calculate displacements
    displs = [sum(counts[:i]) for i in range(size)]
    
    mpi_dtype = to_mpi_dtype(dtype)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Allocate receive buffer on all processes
            recv_buff = build_buffer((counts[rank],), dtype)
            
            if rank == 0:
                # Execute function and prepare send buffer
                result = func(*args, **kwargs)
                send_buff = result
            else:
                send_buff = None
            
            # Scatter variable data
            comm.Scatterv([send_buff, counts, displs, mpi_dtype], [recv_buff, mpi_dtype], root=0)
            
            return recv_buff
        return wrapper
    return decorator

def variable_scatter_from_process(process_rank: int, counts: Sequence[int], dtype: np.dtype, comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on specified rank and scatters variable-sized results to all processes.
    
    Parameters
    ----------
    process_rank : int
        Rank of the process that should execute the function and scatter results.
    counts : sequence of ints
        Number of elements to send to each process.
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
    The decorated function should return a 1D numpy array with size sum(counts) and the specified dtype.
    
    Decorated Function Returns
    --------------------------
    Buffer containing the variable-sized chunk assigned to each process based on counts array.

    Notes
    -----
    Decorated function only runs on the specified process.
    """
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    counts = list(counts)
    if len(counts) != size:
        raise ValueError(f"counts length {len(counts)} must equal number of processes {size}")
    
    # Calculate displacements
    displs = [sum(counts[:i]) for i in range(size)]
    
    mpi_dtype = to_mpi_dtype(dtype)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Allocate receive buffer on all processes
            recv_buff = build_buffer((counts[rank],), dtype)
            
            if rank == process_rank:
                # Execute function and prepare send buffer
                result = func(*args, **kwargs)
                send_buff = result
            else:
                send_buff = None
            
            # Scatter variable data
            comm.Scatterv([send_buff, counts, displs, mpi_dtype], [recv_buff, mpi_dtype], root=process_rank)
            
            return recv_buff
        return wrapper
    return decorator

# Buffered variable gather decorators
def variable_gather_to_main(counts: Sequence[int], dtype: np.dtype, comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on all processes and gathers variable-sized results to rank 0.
    
    Parameters
    ----------
    counts : sequence of ints
        Number of elements to receive from each process.
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
    The decorated function should return a 1D numpy array with size counts[rank] and the specified dtype.
    
    Decorated Function Returns
    --------------------------
    On rank 0: Buffer containing concatenated variable-sized data from all processes.
    On other ranks: None.

    Notes
    -----
    Decorated function runs on all processes.
    """
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    counts = list(counts)
    if len(counts) != size:
        raise ValueError(f"counts length {len(counts)} must equal number of processes {size}")
    
    # Calculate displacements
    displs = [sum(counts[:i]) for i in range(size)]
    
    mpi_dtype = to_mpi_dtype(dtype)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Execute function on all processes
            result = func(*args, **kwargs)
            
            send_buff = result
            
            # Prepare receive buffer only on rank 0
            if rank == 0:
                recv_buff = build_buffer((sum(counts),), dtype)
            else:
                recv_buff = None
            
            # Gather variable data to rank 0
            comm.Gatherv([send_buff, mpi_dtype], [recv_buff, counts, displs, mpi_dtype], root=0)
            
            return recv_buff
        return wrapper
    return decorator

def variable_gather_to_process(process_rank: int, counts: Sequence[int], dtype: np.dtype, comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on all processes and gathers variable-sized results to specified rank.
    
    Parameters
    ----------
    process_rank : int
        Rank of the process that should receive gathered results.
    counts : sequence of ints
        Number of elements to receive from each process.
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
    The decorated function should return a 1D numpy array with size counts[rank] and the specified dtype.
    
    Decorated Function Returns
    --------------------------
    On specified rank: Buffer containing concatenated variable-sized data from all processes.
    On other ranks: None.

    Notes
    -----
    Decorated function runs on all processes.
    """
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    counts = list(counts)
    if len(counts) != size:
        raise ValueError(f"counts length {len(counts)} must equal number of processes {size}")
    
    # Calculate displacements
    displs = [sum(counts[:i]) for i in range(size)]
    
    mpi_dtype = to_mpi_dtype(dtype)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Execute function on all processes
            result = func(*args, **kwargs)
            
            send_buff = result
            
            # Prepare receive buffer only on specified rank
            if rank == process_rank:
                recv_buff = build_buffer((sum(counts),), dtype)
            else:
                recv_buff = None
            
            # Gather variable data to specified rank
            comm.Gatherv([send_buff, mpi_dtype], [recv_buff, counts, displs, mpi_dtype], root=process_rank)
            
            return recv_buff
        return wrapper
    return decorator

def variable_gather_to_all(counts: Sequence[int], dtype: np.dtype, comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on all processes and gathers variable-sized results to all processes.
    
    Parameters
    ----------
    counts : sequence of ints
        Number of elements to receive from each process.
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
    The decorated function should return a 1D numpy array with size counts[rank] and the specified dtype.
    
    Decorated Function Returns
    --------------------------
    Buffer containing concatenated variable-sized data from all processes, available on all processes.

    Notes
    -----
    Decorated function runs on all processes.
    """
    size = comm.Get_size()
    
    counts = list(counts)
    if len(counts) != size:
        raise ValueError(f"counts length {len(counts)} must equal number of processes {size}")
    
    # Calculate displacements
    displs = [sum(counts[:i]) for i in range(size)]
    
    mpi_dtype = to_mpi_dtype(dtype)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Execute function on all processes
            result = func(*args, **kwargs)
            
            send_buff = result
            recv_buff = build_buffer((sum(counts),), dtype)
            
            # Gather variable data to all processes
            comm.Allgatherv([send_buff, mpi_dtype], [recv_buff, counts, displs, mpi_dtype])
            
            return recv_buff
        return wrapper
    return decorator

# Buffered variable all-to-all decorator
def variable_all_to_all(send_counts: Sequence[int], recv_counts: Sequence[int], dtype: np.dtype, comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on all processes and exchanges variable-sized results between all processes.
    
    Parameters
    ----------
    send_counts : sequence of ints
        Number of elements to send to each process.
    recv_counts : sequence of ints
        Number of elements to receive from each process.
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
    The decorated function should return a 1D numpy array with size sum(send_counts) and the specified dtype.
    
    Decorated Function Returns
    --------------------------
    Buffer containing variable-sized data received from all processes based on recv_counts array.

    Notes
    -----
    Decorated function runs on all processes.
    """
    size = comm.Get_size()
    
    send_counts = list(send_counts)
    recv_counts = list(recv_counts)
    
    if len(send_counts) != size:
        raise ValueError(f"send_counts length {len(send_counts)} must equal number of processes {size}")
    if len(recv_counts) != size:
        raise ValueError(f"recv_counts length {len(recv_counts)} must equal number of processes {size}")
    
    # Calculate displacements
    send_displs = [sum(send_counts[:i]) for i in range(size)]
    recv_displs = [sum(recv_counts[:i]) for i in range(size)]
    
    mpi_dtype = to_mpi_dtype(dtype)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Execute function on all processes
            result = func(*args, **kwargs)
            
            send_buff = result
            recv_buff = build_buffer((sum(recv_counts),), dtype)
            
            # Variable all-to-all exchange
            comm.Alltoallv([send_buff, send_counts, send_displs, mpi_dtype], 
                          [recv_buff, recv_counts, recv_displs, mpi_dtype])
            
            return recv_buff
        return wrapper
    return decorator

# Example usage and testing functions
if __name__ == "__main__":
    size = MPI.COMM_WORLD.Get_size()
    rank = MPI.COMM_WORLD.Get_rank()
    
    # Example 1: Variable scatter - each process gets different amount
    counts_scatter = [10, 20, 15, 25][:size]  # Adjust for actual number of processes
    @variable_scatter_from_main(counts=counts_scatter, dtype=np.float64)
    def create_variable_work():
        """Create variable-sized work chunks."""
        total_size = sum(counts_scatter)
        return np.arange(total_size, dtype=np.float64)
    
    # Example 2: Variable gather - each process contributes different amount
    counts_gather = [5, 15, 10, 20][:size]
    @variable_gather_to_main(counts=counts_gather, dtype=np.int32)
    def contribute_variable_data():
        """Each process contributes different amount of data."""
        my_count = counts_gather[rank]
        return np.full(my_count, rank * 100, dtype=np.int32)
    
    # Example 3: Variable all-to-all - different send/receive counts
    send_counts = [rank + 1] * size  # Send rank+1 elements to each process
    recv_counts = [i + 1 for i in range(size)]  # Receive i+1 elements from process i
    @variable_all_to_all(send_counts=send_counts, recv_counts=recv_counts, dtype=np.float32)
    def exchange_variable_data():
        """Exchange variable amounts with each process."""
        total_send = sum(send_counts)
        data = np.zeros(total_send, dtype=np.float32)
        start = 0
        for i in range(size):
            count = send_counts[i]
            data[start:start+count] = rank * 1000 + i * 10 + np.arange(count)
            start += count
        return data
    
    print(f"Rank {rank}: Buffered variable-length decorators ready")