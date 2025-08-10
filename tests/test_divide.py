from mpitools import setup_mpi, eval_on_main, eval_on_workers, eval_on_single, eval_on_select
import time

comm, rank, size = setup_mpi()

def main_print(x):
    if rank == 0:
        print(x)

@eval_on_main()
def main_only():
    print(f"Executing main_only on rank {rank}")

@eval_on_workers()
def worker_only():
    print(f"Executing worker_only on rank {rank}")

@eval_on_single(size-1)
def single_only():
    print(f"Executing single_only on rank {rank}")

@eval_on_select([0, 1])
def select_only():
    print(f"Executing select_only on rank {rank}")


if __name__ == "__main__":
    main_print('Testing Main Only')
    main_only()
    time.sleep(1)
    comm.barrier()

    main_print('\nTesting Worker Only')
    worker_only()
    time.sleep(1)
    comm.barrier()

    main_print('\nTesting Single Only')
    single_only()
    time.sleep(1)
    comm.barrier()

    main_print('\nTesting Select Only')
    select_only()
    comm.barrier()
    