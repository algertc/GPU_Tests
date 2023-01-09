from dask_cuda import LocalCUDACluster
from dask.distributed import Client
cluster = LocalCUDACluster()
client = Client(cluster)

import dask_cudf
import cupy as cp
import time
import os, json
import subprocess
import pandas as pd


train_dir='data/chunked_higgs/*.csv'
df = dask_cudf.read_csv(train_dir, header=None, names=colnames, chunksize=None)

print("Number of partitions is", df.npartitions)

######

df["key"] = df.feature02.round()
group_means = df.groupby("key").mean().persist()
wait(group_means);

group_means.head()