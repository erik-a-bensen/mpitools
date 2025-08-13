from mpi4py import MPI

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