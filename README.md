# mpitools

Description, installation, examples...









## API Reference

## `abort_on_error`

```python
abort_on_error(exception_type: Exception = <class 'Exception'>, comm: mpi4py.MPI.Comm = <mpi4py.MPI.Intracomm object at 0x7f856a1843c0>) -> collections.abc.Callable
```


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


## `broadcast_from_main`

```python
broadcast_from_main(comm: mpi4py.MPI.Comm = <mpi4py.MPI.Intracomm object at 0x7f856a1843c0>) -> collections.abc.Callable
```


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


## `broadcast_from_process`

```python
broadcast_from_process(process_rank: int, comm: mpi4py.MPI.Comm = <mpi4py.MPI.Intracomm object at 0x7f856a1843c0>) -> collections.abc.Callable
```


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


## `eval_on_main`

```python
eval_on_main(comm: mpi4py.MPI.Comm = <mpi4py.MPI.Intracomm object at 0x7f856a1843c0>) -> collections.abc.Callable
```


Decorator that only executes function on rank 0 (main process).

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
Function runs only on rank 0, returns None on all other ranks.


## `eval_on_select`

```python
eval_on_select(process_ranks: list[int], comm: mpi4py.MPI.Comm = <mpi4py.MPI.Intracomm object at 0x7f856a1843c0>) -> collections.abc.Callable
```


Decorator that only executes function on selected process ranks.

Parameters
----------
process_ranks : list[int]
    List of ranks that should execute the function.
comm : MPI.Comm, optional
    MPI communicator. Defaults to COMM_WORLD.

Returns
-------
Callable
    Decorator function.

Notes
-----
Function runs only on ranks in process_ranks, returns None on all other ranks.


## `eval_on_single`

```python
eval_on_single(process_rank: int, comm: mpi4py.MPI.Comm = <mpi4py.MPI.Intracomm object at 0x7f856a1843c0>) -> collections.abc.Callable
```


Decorator that only executes function on a specific process rank.

Parameters
----------
process_rank : int
    Rank of the process that should execute the function.
comm : MPI.Comm, optional
    MPI communicator. Defaults to COMM_WORLD.

Returns
-------
Callable
    Decorator function.

Notes
-----
Function runs only on the specified rank, returns None on all other ranks.


## `eval_on_workers`

```python
eval_on_workers(comm: mpi4py.MPI.Comm = <mpi4py.MPI.Intracomm object at 0x7f856a1843c0>) -> collections.abc.Callable
```


Decorator that only executes function on worker processes (rank != 0).

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
Function runs only on ranks 1, 2, ..., n-1, returns None on rank 0.


## `gather_to_all`

```python
gather_to_all(comm: mpi4py.MPI.Comm = <mpi4py.MPI.Intracomm object at 0x7f856a1843c0>) -> collections.abc.Callable
```


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


## `gather_to_main`

```python
gather_to_main(comm: mpi4py.MPI.Comm = <mpi4py.MPI.Intracomm object at 0x7f856a1843c0>) -> collections.abc.Callable
```


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


## `gather_to_process`

```python
gather_to_process(process_rank: int, comm: mpi4py.MPI.Comm = <mpi4py.MPI.Intracomm object at 0x7f856a1843c0>) -> collections.abc.Callable
```


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


## `reduce_to_all`

```python
reduce_to_all(op: str | mpi4py.MPI.Op = 'sum', comm: mpi4py.MPI.Comm = <mpi4py.MPI.Intracomm object at 0x7f856a1843c0>) -> collections.abc.Callable
```


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


## `reduce_to_main`

```python
reduce_to_main(op: str | mpi4py.MPI.Op = 'sum', comm: mpi4py.MPI.Comm = <mpi4py.MPI.Intracomm object at 0x7f856a1843c0>) -> collections.abc.Callable
```


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


## `reduce_to_process`

```python
reduce_to_process(process_rank: int, op: str | mpi4py.MPI.Op = 'sum', comm: mpi4py.MPI.Comm = <mpi4py.MPI.Intracomm object at 0x7f856a1843c0>) -> collections.abc.Callable
```


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


## `setup_mpi`

```python
setup_mpi() -> tuple[mpi4py.MPI.Comm, int, int]
```


Initialize MPI and return the communicator, rank, and size.

Returns:
    tuple: A tuple containing the MPI communicator, rank, and size.

