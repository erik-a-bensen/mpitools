from mpi4py import MPI
from mpi4py.MPI import Comm, COMM_WORLD, Op
from collections.abc import Callable
from functools import wraps

# Broadcast decorators
def broadcast_from_main(comm: Comm = COMM_WORLD) -> Callable:
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
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return comm.gather(result, root=0)
        return wrapper
    return decorator

def gather_to_process(process_rank: int, comm: Comm = COMM_WORLD) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return comm.gather(result, root=process_rank)
        return wrapper
    return decorator

def gather_to_all(comm: Comm = COMM_WORLD) -> Callable:
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
    if isinstance(op, str):
        if op not in reduce_ops:
            raise ValueError(f"Invalid reduction operation: {op}. Supported operations (case insensitive): {list(reduce_ops.keys())}")
        op = reduce_ops[op.lower()]

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return comm.reduce(result, op=op, root=process_rank)
        return wrapper
    return decorator

def reduce_to_all(op: str | Op = 'sum', comm: Comm = COMM_WORLD) -> Callable:
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