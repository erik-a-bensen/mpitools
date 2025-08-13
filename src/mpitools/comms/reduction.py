from mpi4py.MPI import Comm, COMM_WORLD, Op
from collections.abc import Callable
from functools import wraps
from mpitools.comms.utils import reduce_ops

# Reduce decorators
def reduce_to_main(op: str | Op = 'sum', comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on all processes and reduces results to rank 0.
    
    Parameters
    ----------
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
    The decorated function should return data compatible with the specified reduction operation.
    
    Decorated Function Returns
    --------------------------
    On rank 0: The reduced result from all processes.
    On other ranks: None.

    Notes
    -----
    Decorated function runs on all processes.
    """
    if isinstance(op, str):
        if op not in reduce_ops:
            raise ValueError(f"Invalid reduction operation: {op}. Supported operations: {list(reduce_ops.keys())}")
        op = reduce_ops[op.lower()]

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return comm.reduce(result, op=op, root=0)
        return wrapper
    return decorator

def reduce_to_process(process_rank: int, op: str | Op = 'sum', comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on all processes and reduces results to specified rank.
    
    Parameters
    ----------
    process_rank : int
        Rank of the process that should receive the reduced result.
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
    The decorated function should return data compatible with the specified reduction operation.
    
    Decorated Function Returns
    --------------------------
    On specified rank: The reduced result from all processes.
    On other ranks: None.

    Notes
    -----
    Decorated function runs on all processes.
    """
    if isinstance(op, str):
        if op not in reduce_ops:
            raise ValueError(f"Invalid reduction operation: {op}. Supported operations: {list(reduce_ops.keys())}")
        op = reduce_ops[op.lower()]

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return comm.reduce(result, op=op, root=process_rank)
        return wrapper
    return decorator

def reduce_to_all(op: str | Op = 'sum', comm: Comm = COMM_WORLD) -> Callable:
    """
    Decorator that executes function on all processes and reduces results to all processes.
    
    Parameters
    ----------
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
    The decorated function should return data compatible with the specified reduction operation.
    
    Decorated Function Returns
    --------------------------
    The reduced result from all processes, available on all processes.

    Notes
    -----
    Decorated function runs on all processes.
    """
    if isinstance(op, str):
        if op not in reduce_ops:
            raise ValueError(f"Invalid reduction operation: {op}. Supported operations: {list(reduce_ops.keys())}")
        op = reduce_ops[op.lower()]

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return comm.allreduce(result, op=op)
        return wrapper
    return decorator