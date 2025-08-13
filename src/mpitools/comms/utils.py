from mpi4py import MPI
import numpy as np
from typing import Tuple

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

# Helper function to convert string operations to MPI.Op
def to_mpi_op(op: str | MPI.Op) -> MPI.Op:
    if isinstance(op, str):
        if op not in reduce_ops:
            raise ValueError(f"Invalid reduction operation: {op}. Supported operations: {list(reduce_ops.keys())}")
        op = reduce_ops[op.lower()]
    return op

# Helper function to build buffers
def build_buffer(shape: int | Tuple[int, ...], dtype: np.dtype) -> np.ndarray:
    """Build buffer for MPI communication."""
    return np.empty(shape, dtype=dtype)

# Helper functions to convert dtypes to MPI datatypes
def numpy_to_mpi_dtype(np_dtype: np.dtype) -> MPI.Datatype:
    """Convert numpy dtype to MPI datatype."""
    dtype_map = {
        np.int8: MPI.INT8_T,
        np.int16: MPI.INT16_T, 
        np.int32: MPI.INT32_T,
        np.int64: MPI.INT64_T,
        np.uint8: MPI.UINT8_T,
        np.uint16: MPI.UINT16_T,
        np.uint32: MPI.UINT32_T,
        np.uint64: MPI.UINT64_T,
        np.float32: MPI.FLOAT,
        np.float64: MPI.DOUBLE,
        np.complex64: MPI.COMPLEX,
        np.complex128: MPI.DOUBLE_COMPLEX,
    }
    
    # Handle numpy dtype objects
    if hasattr(np_dtype, 'type'):
        np_dtype = np_dtype.type
    
    return dtype_map.get(np_dtype, MPI.BYTE)

def to_mpi_dtype(dtype: np.dtype) -> MPI.Datatype:
    return numpy_to_mpi_dtype(dtype)