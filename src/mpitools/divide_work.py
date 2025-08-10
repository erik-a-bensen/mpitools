from mpi4py.MPI import Comm, COMM_WORLD
from collections.abc import Callable
from functools import wraps

# MPI tools for dividing work among processes
def eval_on_main(comm: Comm = COMM_WORLD) -> Callable:
    rank = comm.Get_rank()
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if rank == 0:
                return func(*args, **kwargs)
            else:
                return None
        return wrapper
    return decorator

def eval_on_workers(comm: Comm = COMM_WORLD) -> Callable:
    rank = comm.Get_rank()
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if rank != 0:
                return func(*args, **kwargs)
            else:
                return None
        return wrapper
    return decorator

def eval_on_single(process_rank: int, comm: Comm = COMM_WORLD) -> Callable:
    rank = comm.Get_rank()
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if rank == process_rank:
                return func(*args, **kwargs)
            else:
                return None
        return wrapper
    return decorator

def eval_on_select(process_ranks: list[int], comm: Comm = COMM_WORLD) -> Callable:
    rank = comm.Get_rank()
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if rank in process_ranks:
                return func(*args, **kwargs)
            else:
                return None
        return wrapper
    return decorator