from dask_cuda import LocalCUDACluster
from dask.distributed import Client
cluster = LocalCUDACluster()
client = Client(cluster)

import numpy as np
import time
from xgboost.sklearn import XGBRegressor
 
trials = 1
X = np.random.randint(0,100,size=(10000000,60))
Y = np.random.randint(0,10,size=(10000000))
 
def timeit(mdl):

    print(mdl)
    for _ in range(trials):
        start = time.time()
        mdl.fit(X,Y)
        print(time.time() - start)
   

for mdl in [XGBRegressor(tree_method="gpu_hist"), XGBRegressor(tree_method="hist"),
            XGBRegressor(tree_method="gpu_hist", colsample_bytree=0.1), XGBRegressor(tree_method="hist", colsample_bytree=0.1),
            XGBRegressor(tree_method="gpu_hist", max_bin=6), XGBRegressor(tree_method="hist", max_bin=6),
            XGBRegressor(tree_method="hist", n_jobs=1), XGBRegressor(tree_method="hist", n_jobs=5), XGBRegressor(tree_method="hist", n_jobs=-1)]:
    timeit(mdl)