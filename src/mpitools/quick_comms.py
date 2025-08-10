from mpi4py import MPI
from mpi4py.MPI import Comm, COMM_WORLD, Op
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

# Reduce decorators
reduce_ops = {
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
    
    Notes
    -----
    Function runs on all processes, results are reduced to specified rank using comm.reduce().
    The specified rank receives the reduced result, other ranks receive None.
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
    
    Notes
    -----
    Function runs on all processes, results are reduced to all ranks using comm.allreduce().
    All processes receive the same reduced result.
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