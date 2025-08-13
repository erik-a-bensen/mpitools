# API Reference

> **⚠️ Development Version**: This API is subject to change until v1.0.0. Breaking changes may occur in minor releases.

## `setup_mpi`

```python
setup_mpi() -> tuple[MPI.Comm, int, int]
```

Initialize MPI and return the communicator, rank, and size.

Returns:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;tuple: A tuple containing the MPI communicator, rank, and size.

## `abort_on_error`

```python
abort_on_error(exception_type: Exception = Exception, comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that aborts all MPI processes when an exception occurs.

Parameters<br>
----------<br>
exception_type : Exception, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Type of exception to catch. Defaults to Exception (all exceptions).<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator to abort. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Notes<br>
-----<br>
Prints error traceback and calls comm.Abort(1) to terminate all processes.

## `eval_on_main`

```python
eval_on_main(comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that only executes function on rank 0 (main process).

Parameters<br>
----------<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Notes<br>
-----<br>
Function runs only on rank 0, returns None on all other ranks.

## `eval_on_workers`

```python
eval_on_workers(comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that only executes function on worker processes (rank != 0).

Parameters<br>
----------<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Notes<br>
-----<br>
Function runs only on ranks 1, 2, ..., n-1, returns None on rank 0.

## `eval_on_single`

```python
eval_on_single(process_rank: int, comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that only executes function on a specific process rank.

Parameters<br>
----------<br>
process_rank : int<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Rank of the process that should execute the function.<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Notes<br>
-----<br>
Function runs only on the specified rank, returns None on all other ranks.

## `eval_on_select`

```python
eval_on_select(process_ranks: list[int], comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that only executes function on selected process ranks.

Parameters<br>
----------<br>
process_ranks : list[int]<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;List of ranks that should execute the function.<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Notes<br>
-----<br>
Function runs only on ranks in process_ranks, returns None on all other ranks.

---

# Comms Module

## `broadcast_from_main`

```python
broadcast_from_main(comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on rank 0 and broadcasts result to all processes.

Parameters<br>
----------<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function can return any pickle-able Python object.

Decorated Function Returns<br>
--------------------------<br>
The broadcast result from rank 0, available on all processes.

Notes<br>
-----<br>
Decorated function only runs on the main process.

## `broadcast_from_process`

```python
broadcast_from_process(process_rank: int, comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on specified rank and broadcasts result to all processes.

Parameters<br>
----------<br>
process_rank : int<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Rank of the process that should execute the function and broadcast result.<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function can return any pickle-able Python object.

Decorated Function Returns<br>
--------------------------<br>
The broadcast result from the specified rank, available on all processes.

Notes<br>
-----<br>
Decorated function only runs on the specified process.

## `scatter_from_main`

```python
scatter_from_main(comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on rank 0 and scatters results to all processes.

Parameters<br>
----------<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function should return a sequence (list, tuple, etc.) with length equal to the number of processes.

Decorated Function Returns<br>
--------------------------<br>
One element from the sequence, assigned to each process based on its rank.

Notes<br>
-----<br>
Decorated function only runs on the main process.

## `scatter_from_process`

```python
scatter_from_process(process_rank: int, comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on specified rank and scatters results to all processes.

Parameters<br>
----------<br>
process_rank : int<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Rank of the process that should execute the function and scatter results.<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function should return a sequence (list, tuple, etc.) with length equal to the number of processes.

Decorated Function Returns<br>
--------------------------<br>
One element from the sequence, assigned to each process based on its rank.

Notes<br>
-----<br>
Decorated function only runs on the specified process.

## `gather_to_main`

```python
gather_to_main(comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on all processes and gathers results to rank 0.

Parameters<br>
----------<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function can return any pickle-able Python object.

Decorated Function Returns<br>
--------------------------<br>
On rank 0: List containing results from all processes.<br>
On other ranks: None.

Notes<br>
-----<br>
Decorated function runs on all processes.

## `gather_to_process`

```python
gather_to_process(process_rank: int, comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on all processes and gathers results to specified rank.

Parameters<br>
----------<br>
process_rank : int<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Rank of the process that should receive gathered results.<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function can return any pickle-able Python object.

Decorated Function Returns<br>
--------------------------<br>
On specified rank: List containing results from all processes.<br>
On other ranks: None.

Notes<br>
-----<br>
Decorated function runs on all processes.

## `gather_to_all`

```python
gather_to_all(comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on all processes and gathers results to all processes.

Parameters<br>
----------<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function can return any pickle-able Python object.

Decorated Function Returns<br>
--------------------------<br>
List containing results from all processes, available on all processes.

Notes<br>
-----<br>
Decorated function runs on all processes.

## `all_to_all`

```python
all_to_all(comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on all processes and exchanges results between all processes.

Parameters<br>
----------<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns <br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function should return a sequence (list, tuple, etc.) with length equal to the number of processes.

Decorated Function Returns<br>
--------------------------<br>
List containing one element from each process, with element order corresponding to process rank.

Notes<br>
-----<br>
Decorated function runs on all processes.

## `reduce_to_main`

```python
reduce_to_main(op: str | MPI.Op = 'sum', comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on all processes and reduces results to rank 0.

Parameters<br>
----------<br>
op : str or MPI.Op, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Reduction operation to apply. Defaults to 'sum'.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;String options: 'sum', 'prod', 'max', 'min', 'land', 'band', 'lor', 'bor', <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'lxor', 'bxor', 'maxloc', 'minloc'.<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function should return data compatible with the specified reduction operation.

Decorated Function Returns<br>
--------------------------<br>
On rank 0: The reduced result from all processes.<br>
On other ranks: None.

Notes<br>
-----<br>
Decorated function runs on all processes.

## `reduce_to_process`

```python
reduce_to_process(process_rank: int, op: str | MPI.Op = 'sum', comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on all processes and reduces results to specified rank.

Parameters<br>
----------<br>
process_rank : int<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Rank of the process that should receive the reduced result.<br>
op : str or MPI.Op, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Reduction operation to apply. Defaults to 'sum'.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;String options: 'sum', 'prod', 'max', 'min', 'land', 'band', 'lor', 'bor', <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'lxor', 'bxor', 'maxloc', 'minloc'.<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function should return data compatible with the specified reduction operation.

Decorated Function Returns<br>
--------------------------<br>
On specified rank: The reduced result from all processes.<br>
On other ranks: None.

Notes<br>
-----<br>
Decorated function runs on all processes.

## `reduce_to_all`

```python
reduce_to_all(op: str | MPI.Op = 'sum', comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on all processes and reduces results to all processes.

Parameters<br>
----------<br>
op : str or MPI.Op, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Reduction operation to apply. Defaults to 'sum'.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;String options: 'sum', 'prod', 'max', 'min', 'land', 'band', 'lor', 'bor', <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'lxor', 'bxor', 'maxloc', 'minloc'.<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function should return data compatible with the specified reduction operation.

Decorated Function Returns<br>
--------------------------<br>
The reduced result from all processes, available on all processes.

Notes<br>
-----<br>
Decorated function runs on all processes.

## `buffered_broadcast_from_main`

```python
buffered_broadcast_from_main(shape: Union[int, Tuple[int, ...]], dtype: numpy.dtype, comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on rank 0 and broadcasts result to all processes.

Parameters<br>
----------<br>
shape : int or tuple of ints<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Shape of the data buffer to broadcast.<br>
dtype : numpy.dtype<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Data type of the buffer.<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function should return a numpy array with the specified shape and dtype.

Decorated Function Returns<br>
--------------------------<br>
Buffer containing the broadcast data on all processes.

Notes<br>
-----<br>
Decorated function only runs on the main process.

## `buffered_broadcast_from_process`

```python
buffered_broadcast_from_process(process_rank: int, shape: Union[int, Tuple[int, ...]], dtype: numpy.dtype, comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on specified rank and broadcasts result to all processes.

Parameters<br>
----------<br>
process_rank : int<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Rank of the process that should execute the function and broadcast result.<br>
shape : int or tuple of ints<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Shape of the data buffer to broadcast.<br>
dtype : numpy.dtype<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Data type of the buffer.<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function should return a numpy array with the specified shape and dtype.

Decorated Function Returns<br>
--------------------------<br>
Buffer containing the broadcast data on all processes.

Notes<br>
-----<br>
Decorated function only runs on the specified process.

## `buffered_scatter_from_main`

```python
buffered_scatter_from_main(chunk_shape: Union[int, Tuple[int, ...]], dtype: numpy.dtype, comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on rank 0 and scatters results to all processes.

Parameters<br>
----------<br>
chunk_shape : int or tuple of ints<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Shape of each chunk to be scattered to each process.<br>
dtype : numpy.dtype<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Data type of the buffer.<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function should return a numpy array with shape (num_processes, *chunk_shape) and the specified dtype.

Decorated Function Returns<br>
--------------------------<br>
Buffer containing the scattered chunk assigned to each process.

Notes<br>
-----<br>
Decorated function only runs on the main process.

## `buffered_scatter_from_process`

```python
buffered_scatter_from_process(process_rank: int, chunk_shape: Union[int, Tuple[int, ...]], dtype: numpy.dtype, comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on specified rank and scatters results to all processes.

Parameters<br>
----------<br>
process_rank : int<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Rank of the process that should execute the function and scatter results.<br>
chunk_shape : int or tuple of ints<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Shape of each chunk to be scattered to each process.<br>
dtype : numpy.dtype<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Data type of the buffer.<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function should return a numpy array with shape (num_processes, *chunk_shape) and the specified dtype.

Decorated Function Returns<br>
--------------------------<br>
Buffer containing the scattered chunk assigned to each process.

Notes<br>
-----<br>
Decorated function only runs on the specified process.

## `buffered_gather_to_main`

```python
buffered_gather_to_main(shape: Union[int, Tuple[int, ...]], dtype: numpy.dtype, comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on all processes and gathers results to rank 0.

Parameters<br>
----------<br>
shape : int or tuple of ints<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Shape of data from each process.<br>
dtype : numpy.dtype<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Data type of the buffer.<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function should return a numpy array with the specified shape and dtype.

Decorated Function Returns<br>
--------------------------<br>
On rank 0: Buffer with shape (num_processes, *shape) containing all gathered data.<br>
On other ranks: None.

Notes<br>
-----<br>
Decorated function runs on all processes.

## `buffered_gather_to_process`

```python
buffered_gather_to_process(process_rank: int, shape: Union[int, Tuple[int, ...]], dtype: numpy.dtype, comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on all processes and gathers results to specified rank.

Parameters<br>
----------<br>
process_rank : int<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Rank of the process that should receive gathered results.<br>
shape : int or tuple of ints<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Shape of data from each process.<br>
dtype : numpy.dtype<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Data type of the buffer.<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function should return a numpy array with the specified shape and dtype.

Decorated Function Returns<br>
--------------------------<br>
On specified rank: Buffer with shape (num_processes, *shape) containing all gathered data.<br>
On other ranks: None.

Notes<br>
-----<br>
Decorated function runs on all processes.

## `buffered_gather_to_all`

```python
buffered_gather_to_all(shape: Union[int, Tuple[int, ...]], dtype: numpy.dtype, comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on all processes and gathers results to all processes.

Parameters<br>
----------<br>
shape : int or tuple of ints<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Shape of data from each process.<br>
dtype : numpy.dtype<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Data type of the buffer.<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function should return a numpy array with the specified shape and dtype.

Decorated Function Returns<br>
--------------------------<br>
Buffer with shape (num_processes, *shape) containing all gathered data on all processes.

Notes<br>
-----<br>
Decorated function runs on all processes.

## `buffered_all_to_all`

```python
buffered_all_to_all(element_shape: Union[int, Tuple[int, ...]], dtype: numpy.dtype, comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on all processes and exchanges results between all processes.

Parameters<br>
----------<br>
element_shape : int or tuple of ints<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Shape of data element being sent to each process.<br>
dtype : numpy.dtype<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Data type of the buffer.<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function should return a numpy array with shape (num_processes, *element_shape) and the specified dtype.

Decorated Function Returns<br>
--------------------------<br>
Buffer with shape (num_processes, *element_shape) containing exchanged data from all processes.

Notes<br>
-----<br>
Decorated function runs on all processes.

## `buffered_reduce_to_main`

```python
buffered_reduce_to_main(shape: Union[int, Tuple[int, ...]], dtype: numpy.dtype, op: str | MPI.Op = 'sum', comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on all processes and reduces results to rank 0.

Parameters<br>
----------<br>
shape : int or tuple of ints<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Shape of the data buffer for reduction.<br>
dtype : numpy.dtype<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Data type of the buffer.<br>
op : str or MPI.Op, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Reduction operation to apply. Defaults to 'sum'.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;String options: 'sum', 'prod', 'max', 'min', 'land', 'band', 'lor', 'bor', <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'lxor', 'bxor', 'maxloc', 'minloc'.<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function should return a numpy array with the specified shape and dtype.

Decorated Function Returns<br>
--------------------------<br>
On rank 0: Buffer containing the reduced result from all processes.<br>
On other ranks: None.

Notes<br>
-----<br>
Decorated function runs on all processes.

## `buffered_reduce_to_process`

```python
buffered_reduce_to_process(process_rank: int, shape: Union[int, Tuple[int, ...]], dtype: numpy.dtype, op: str | MPI.Op = 'sum', comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on all processes and reduces results to specified rank.

Parameters<br>
----------<br>
process_rank : int<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Rank of the process that should receive the reduced result.<br>
shape : int or tuple of ints<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Shape of the data buffer for reduction.<br>
dtype : numpy.dtype<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Data type of the buffer.<br>
op : str or MPI.Op, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Reduction operation to apply. Defaults to 'sum'.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;String options: 'sum', 'prod', 'max', 'min', 'land', 'band', 'lor', 'bor', <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'lxor', 'bxor', 'maxloc', 'minloc'.<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function should return a numpy array with the specified shape and dtype.

Decorated Function Returns<br>
--------------------------<br>
On specified rank: Buffer containing the reduced result from all processes.<br>
On other ranks: None.

Notes<br>
-----<br>
Decorated function runs on all processes.

## `buffered_reduce_to_all`

```python
buffered_reduce_to_all(shape: Union[int, Tuple[int, ...]], dtype: numpy.dtype, op: str | MPI.Op = 'sum', comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on all processes and reduces results to all processes.

Parameters<br>
----------<br>
shape : int or tuple of ints<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Shape of the data buffer for reduction.<br>
dtype : numpy.dtype<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Data type of the buffer.<br>
op : str or MPI.Op, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Reduction operation to apply. Defaults to 'sum'.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;String options: 'sum', 'prod', 'max', 'min', 'land', 'band', 'lor', 'bor', <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'lxor', 'bxor', 'maxloc', 'minloc'.<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function should return a numpy array with the specified shape and dtype.

Decorated Function Returns<br>
--------------------------<br>
Buffer containing the reduced result from all processes, available on all processes.

Notes<br>
-----<br>
Decorated function runs on all processes.

## `variable_scatter_from_main`

```python
variable_scatter_from_main(counts: Sequence[int], dtype: numpy.dtype, comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on rank 0 and scatters variable-sized results to all processes.

Parameters<br>
----------<br>
counts : sequence of ints<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Number of elements to send to each process.<br>
dtype : numpy.dtype<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Data type of the buffer.<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function should return a 1D numpy array with size sum(counts) and the specified dtype.

Decorated Function Returns<br>
--------------------------<br>
Buffer containing the variable-sized chunk assigned to each process based on counts array.

Notes<br>
-----<br>
Decorated function only runs on the main process.

## `variable_scatter_from_process`

```python
variable_scatter_from_process(process_rank: int, counts: Sequence[int], dtype: numpy.dtype, comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on specified rank and scatters variable-sized results to all processes.

Parameters<br>
----------<br>
process_rank : int<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Rank of the process that should execute the function and scatter results.<br>
counts : sequence of ints<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Number of elements to send to each process.<br>
dtype : numpy.dtype<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Data type of the buffer.<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function should return a 1D numpy array with size sum(counts) and the specified dtype.

Decorated Function Returns<br>
--------------------------<br>
Buffer containing the variable-sized chunk assigned to each process based on counts array.

Notes<br>
-----<br>
Decorated function only runs on the specified process.

## `variable_gather_to_main`

```python
variable_gather_to_main(counts: Sequence[int], dtype: numpy.dtype, comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on all processes and gathers variable-sized results to rank 0.

Parameters<br>
----------<br>
counts : sequence of ints<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Number of elements to receive from each process.<br>
dtype : numpy.dtype<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Data type of the buffer.<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function should return a 1D numpy array with size counts[rank] and the specified dtype.

Decorated Function Returns<br>
--------------------------<br>
On rank 0: Buffer containing concatenated variable-sized data from all processes.<br>
On other ranks: None.

Notes<br>
-----<br>
Decorated function runs on all processes.

## `variable_gather_to_process`

```python
variable_gather_to_process(process_rank: int, counts: Sequence[int], dtype: numpy.dtype, comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on all processes and gathers variable-sized results to specified rank.

Parameters<br>
----------<br>
process_rank : int<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Rank of the process that should receive gathered results.<br>
counts : sequence of ints<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Number of elements to receive from each process.<br>
dtype : numpy.dtype<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Data type of the buffer.<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function should return a 1D numpy array with size counts[rank] and the specified dtype.

Decorated Function Returns<br>
--------------------------<br>
On specified rank: Buffer containing concatenated variable-sized data from all processes.<br>
On other ranks: None.

Notes<br>
-----<br>
Decorated function runs on all processes.

## `variable_gather_to_all`

```python
variable_gather_to_all(counts: Sequence[int], dtype: numpy.dtype, comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on all processes and gathers variable-sized results to all processes.

Parameters<br>
----------<br>
counts : sequence of ints<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Number of elements to receive from each process.<br>
dtype : numpy.dtype<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Data type of the buffer.<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function should return a 1D numpy array with size counts[rank] and the specified dtype.

Decorated Function Returns<br>
--------------------------<br>
Buffer containing concatenated variable-sized data from all processes, available on all processes.

Notes<br>
-----<br>
Decorated function runs on all processes.

## `variable_all_to_all`

```python
variable_all_to_all(send_counts: Sequence[int], recv_counts: Sequence[int], dtype: numpy.dtype, comm: MPI.Comm = MPI.COMM_WORLD) -> Callable
```

Decorator that executes function on all processes and exchanges variable-sized results between all processes.

Parameters<br>
----------<br>
send_counts : sequence of ints<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Number of elements to send to each process.<br>
recv_counts : sequence of ints<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Number of elements to receive from each process.<br>
dtype : numpy.dtype<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Data type of the buffer.<br>
comm : MPI.Comm, optional<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MPI communicator. Defaults to COMM_WORLD.

Returns<br>
-------<br>
Callable<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decorator function.

Decorated Function Requirements<br>
-------------------------------<br>
The decorated function should return a 1D numpy array with size sum(send_counts) and the specified dtype.

Decorated Function Returns<br>
--------------------------<br>
Buffer containing variable-sized data received from all processes based on recv_counts array.

Notes<br>
-----<br>
Decorated function runs on all processes.

---

# Queue Module

## `Task` (class)

```python
Task(task_id: str)
```

Abstract base class for MPIQueue tasks.<br>
Users should inherit from this class and implement the execute method.

attributes:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;task_id: Unique identifier for the task.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;created_at: Timestamp when the task was created.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;started_at: Timestamp when the task started execution.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;completed_at: Timestamp when the task was completed.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;worker_rank: Rank of the worker that executed the task.

### Methods

### `execute`

```python
execute(self) -> Any
```

Execute the task and return the result.<br>
This method must be implemented by subclasses.

## `TaskResult` (class)

```python
TaskResult(task_id: str, result: Any, execution_time: float = 0.0, worker_rank: int = -1)
```

Class to hold the result of a completed task.

attributes:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;task_id: Unique identifier for the task.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;result: The result of the task execution.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;execution_time: Time taken to execute the task in seconds.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;worker_rank: Rank of the worker that executed the task.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;completed_at: Timestamp when the task was completed.

## `MPIQueue` (class)

```python
MPIQueue(comm: MPI.Comm = MPI.COMM_WORLD)
```

Interface for the MPI queue system.<br>
Automatically determines whether to run as manager or worker based on rank.<br>
If running on a single process (size 1), uses serial execution.

### Methods

### `add_task`

```python
add_task(self, task: mpitools.queue.Task)
```

Add a task to the queue (only valid on manager)

### `add_tasks`

```python
add_tasks(self, tasks: List[mpitools.queue.Task])
```

Add multiple tasks to the queue (only valid on manager)

### `run`

```python
run(self, timeout: Optional[float] = None) -> dict[str, mpitools.queue.TaskResult]
```

Run the queue system.

For manager (rank 0): distributes tasks and returns results<br>
For workers (rank > 0): executes tasks until shutdown

Returns:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Dictionary of results indexed by task_id (only on manager), None on workers
