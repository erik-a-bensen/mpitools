from mpi4py import MPI
from mpi4py.MPI import Comm, COMM_WORLD, Op
from collections.abc import Callable
from functools import wraps

# Reduce decorators
_reduce_ops = {
    'sum': MPI.SUM,
    'prod': MPI.PROD,
    'max': MPI.MAX,
    'min': MPI.MIN,
    'land': MPI.LAND,
    'band': MPI.BAND,
    'lor': MPI.LOR,
    'bor': MPI.BOR,
    'lxor': MPI.LXOR,
    'bxor': MPI.BXOR,
    'maxloc': MPI.MAXLOC,
    'minloc': MPI.MINLOC
}

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
    
    Notes
    -----
    Function runs on all processes, results are reduced to rank 0 using comm.reduce().
    Rank 0 receives the reduced result, other ranks receive None.
    """
    if isinstance(op, str):
        if op not in _reduce_ops:
            raise ValueError(f"Invalid reduction operation: {op}. Supported operations: {list(_reduce_ops.keys())}")
        op = _reduce_ops[op.lower()]

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
    
    Notes
    -----
    Function runs on all processes, results are reduced to specified rank using comm.reduce().
    The specified rank receives the reduced result, other ranks receive None.
    """
    if isinstance(op, str):
        if op not in _reduce_ops:
            raise ValueError(f"Invalid reduction operation: {op}. Supported operations: {list(_reduce_ops.keys())}")
        op = _reduce_ops[op.lower()]

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
    
    Notes
    -----
    Function runs on all processes, results are reduced to all ranks using comm.allreduce().
    All processes receive the same reduced result.
    """
    if isinstance(op, str):
        if op not in _reduce_ops:
            raise ValueError(f"Invalid reduction operation: {op}. Supported operations: {list(_reduce_ops.keys())}")
        op = _reduce_ops[op.lower()]

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return comm.allreduce(result, op=op)
        return wrapper
    return decorator