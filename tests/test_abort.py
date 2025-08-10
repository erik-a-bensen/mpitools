from mpitools import setup_mpi, abort_on_error
import time

comm, rank, size = setup_mpi()

@abort_on_error()
def test_abort():
    """Test that the abort_on_error decorator works correctly"""
    for i in range(3):
        if i == 1 and rank == 0:
            raise ValueError("This is a test exception to trigger abort.")
        else:
            time.sleep(0.1)
    print(f"Process {rank} finished function")


if __name__ == "__main__":
    test_abort()
    print(f"Process {rank} completed without errors.")
        