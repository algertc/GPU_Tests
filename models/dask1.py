from dask_cuda import LocalCUDACluster
from dask.distributed import Client
cluster = LocalCUDACluster()
client = Client(cluster)
