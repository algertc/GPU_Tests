#!/bin/bash
#
#For Ubuntu 20.04
#
#

export PATH=/usr/local/cuda-11.8/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64\
                         ${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}

#may work without the following 3 lines
export CUDA_HOME=/usr/local/cuda
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64
export PATH=$PATH:$CUDA_HOME/bin


#Python prerequisites
apt-get -y install python3
apt-get -y install g++ gfortran
apt-get -y install python-dev python-scipy python-matplotlib python-pandas
apt-get -y install libatlas-base-dev
apt-get -y install python3-pip
export PATH=/Users/Ubuntu/Library/Python/3.8/bin:$PATH
pip install numpy==1.23.5 #--> Numba requires numpy <1.24.0
pip install scikit-learn
pip install xgboost
pip instal os, json, time, cupy, subprocess

#for multi gpu
pip install "dask[complete]"
pip install dask_cuda #--> Seems to be different that the main dask pkg and specific for local cuda clusters

#

#Install Cmake
apt-get -y install cmake

#install gcc
apt-get -y install gcc
gcc --version

#Clone the repo and build
git clone --recursive https://github.com/dmlc/xgboost.git xgboostmkdir
cd xgboostmkdir

#Tell CMake where to find the CUDA compiler
#set(CMAKE_CUDA_COMPILER /usr/local/cuda/bin/nvcc)
sed -i '2 a set(CMAKE_CUDA_COMPILER /usr/local/cuda/bin/nvcc)' CMakeLists.txt

#build
mkdir build
cd build
cmake .. -DUSE_CUDA=ON -DBUILD_WITH_CUDA_CUB=ON #IMPORTANT- Make with CUDA options
make -j4
#