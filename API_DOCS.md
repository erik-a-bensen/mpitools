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
