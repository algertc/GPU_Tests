import numpy as np
import os.path
import pandas
import time
import xgboost as xgb
import sys
from dask.distributed import Client, wait
from dask_cuda import LocalCUDACluster
import dask_xgboost
import dask_cudf
import dask
from xgboost.dask import DaskDMatrix
import matplotlib.pyplot as plt
import matplotlib

if sys.version_info[0] >= 3:
    from urllib.request import urlretrieve
else:
    from urllib import urlretrieve

data_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00280/HIGGS.csv.gz"
dmatrix_train_filename = "higgs_train.dmatrix"
dmatrix_test_filename = "higgs_test.dmatrix"
csv_filename = "HIGGS.csv.gz"
train_rows = 10500000
test_rows = 500000
num_round = 1000

plot = True

def load_higgs_for_dask(client):
    # 1. read the CSV File using Pandas
    df_higgs_train = pandas.read_csv(csv_filename, dtype=np.float32, 
                                     nrows=train_rows, header=None).ix[:, 0:30]
    df_higgs_test = pandas.read_csv(csv_filename, dtype=np.float32, 
                                    skiprows=train_rows, nrows=test_rows, 
                                    header=None).ix[:, 0:30]

    # 2. Create a Dask Dataframe from Pandas Dataframe.
    ddf_higgs_train = dask.dataframe.from_pandas(df_higgs_train, npartitions=8)
    ddf_higgs_test = dask.dataframe.from_pandas(df_higgs_test, npartitions=8)
    ddf_y_train = ddf_higgs_train[0]
    del ddf_higgs_train[0]
    ddf_y_test = ddf_higgs_test[0]
    del ddf_higgs_test[0]
    
    #3. Create Dask DMatrix Object using dask dataframes
    ddtrain = DaskDMatrix(client, ddf_higgs_train ,ddf_y_train)
    ddtest = DaskDMatrix(client, ddf_higgs_test ,ddf_y_test)
    
    return ddtrain, ddtest


cluster = LocalCUDACluster()
client = Client(cluster)

ddtrain, ddtest = load_higgs_for_dask(client)
param = {}
param['objective'] = 'binary:logitraw'
param['eval_metric'] = 'error'
param['silence'] = 1
param['tree_method'] = 'gpu_hist'
param['nthread'] = 1


print("Training with Multiple GPUs ...")
tmp = time.time()
output = xgb.dask.train(client, param, ddtrain, num_boost_round=1000, evals=[(ddtest, 'test')])
multigpu_time = time.time() - tmp
bst = output['booster']
multigpu_res = output['history']
print("Multi GPU Training Time: %s seconds" % (str(multigpu_time)))



