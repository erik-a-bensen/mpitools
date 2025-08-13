# mpitools

![PyPI Version](https://img.shields.io/pypi/v/mpi4pytools)
![Development Status](https://img.shields.io/pypi/status/mpi4pytools)
![Python Versions](https://img.shields.io/pypi/pyversions/mpi4pytools)
![License](https://img.shields.io/pypi/l/mpi4pytools)

> **⚠️ Development Notice**: This package is in active development. The API may change significantly between versions until v1.0.0. Use in production environments is not recommended.


A Python package providing simple decorators and utilities for MPI (Message Passing Interface) parallel computing. Built on top of mpi4py, mpitools makes it easy to write parallel code with minimal boilerplate.

## Features

- **Work distribution decorators**: Execute functions on specific ranks or groups of processes
- **Communication decorators**: Collective communications and reduce operations made simple
- **Error handling**: Graceful error handling across all MPI processes
- **Task queue system**: Distributed task processing with the queue submodule

## Installation

```bash
pip install mpi4pytools
```

**Requirements:**
- Python 3.7+
- mpi4py
- An MPI implementation (OpenMPI, MPICH, etc.)

## Quick Start

### Basic Usage

```python
from mpitools import setup_mpi, broadcast_from_main, gather_to_main, eval_on_main

# Initialize MPI environment
comm, rank, size = setup_mpi()

# Execute only on rank 0, broadcast result to all processes
@broadcast_from_main()
def load_config():
    return {"num_iterations": 1000, "tolerance": 1e-6}

# Execute on all processes, gather results to rank 0
@gather_to_main()
def compute_partial_sum():
    return sum(range(rank * 100, (rank + 1) * 100))

# Execute only on rank 0
@eval_on_main()
def save_results(data):
    with open("results.txt", "w") as f:
        f.write(str(data))

# Usage
config = load_config()  # Same config on all processes
partial_sums = compute_partial_sum()  # List of sums on rank 0, None elsewhere
save_results(partial_sums)  # Only saves on rank 0
```

### Task Queue System

```python
from mpitools import setup_mpi
from mpitools.queue import MPIQueue, Task

# Initialize MPI environment
comm, rank, size = setup_mpi()

# Define a task class
class MyTask(Task):
    def __init__(self, task_id: str, data: int):
        super().__init__(task_id)
        self.data = data

    def execute(self):
        # Perform some computation
        result = self.data * 2  # Example computation
        return result

# Create a distributed task queue
queue = MPIQueue()

# Add tasks to the queue
if rank == 0:
    tasks = [MyTask(f"task_{i}", i) for i in range(10)]
    queue.add_tasks(tasks)

# Run the task queue
results = queue.run()

```

### Error Handling

```python
from mpitools import abort_on_error

@abort_on_error()  # Aborts all processes if any process encounters an error
def risky_computation():
    # If this fails on any process, all processes will terminate
    result = 1 / some_calculation()
    return result
```

## Core Decorators

### Error Handling
- `@abort_on_error()` - Abort all processes if any process raises an exception

### Work Distribution
- `@eval_on_main()` - Execute only on rank 0
- `@eval_on_workers()` - Execute only on worker ranks (1, 2, ...)  
- `@eval_on_single(rank)` - Execute only on specified rank
- `@eval_on_select([ranks])` - Execute only on specified ranks

### Collective Communication
- `@broadcast_from_main()` - Execute on rank 0, broadcast result to all processes
- `@broadcast_from_process(rank)` - Execute on specified rank, broadcast to all processes
- `@scatter_from_main()` - Execute on rank 0, scatter data to all processes
- `@scatter_from_process(rank)` - Execute on specified rank, scatter data to all processes
- `@gather_to_main()` - Execute on all processes, gather results to rank 0
- `@gather_to_process(rank)` - Execute on all processes, gather results to specified rank
- `@gather_to_all()` - Execute on all processes, gather results to all processes
- `@all_to_all()` - Execute on all processes, exchange data between all processes

### Reduction Operations
- `@reduce_to_main(op='sum')` - Execute on all processes, reduce to rank 0
- `@reduce_to_process(rank, op='sum')` - Execute on all processes, reduce to specified rank
- `@reduce_to_all(op='sum')` - Execute on all processes, reduce to all processes

Supported reduction operations: `'sum'`, `'prod'`, `'max'`, `'min'`, `'land'`, `'band'`, `'lor'`, `'bor'`, `'lxor'`, `'bxor'`, `'maxloc'`, `'minloc'`

### Decorator Variants
- `@buffered_*` - Buffered versions of collective communication and reduction operations for improved performance. 
- `@variable_*` - Variable-sized versions of buffered scatter, gather and all_to_all communications for handling dynamic data sizes.
- Currently, only numpy arrays are supported.

## Running MPI Programs

```bash
# Run with 4 processes
mpirun -n 4 python your_script.py

# Run with specific hosts
mpirun -n 4 -H host1,host2 python your_script.py
```

## Documentation

- [Full API Reference](API_DOCS.md) - Complete documentation of all functions and classes
- [MPI4PY Documentation](https://mpi4py.readthedocs.io/) - Underlying MPI library

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built on [mpi4py](https://github.com/mpi4py/mpi4py)
