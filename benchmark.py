import sys
import getopt

import numpy as np
from numpy.linalg import norm

import pickle
import time


import local_search
import baseline
import noloops

np.random.seed(0)
REPS = 10

def euclidean_distance(x,y):
    return norm(x-y)

dist = euclidean_distance

def run_test(nc, nf, k, d):
    facilities = np.random.random((nf, d))
    clients = np.random.random((nc, d))
    
    distances = np.zeros((nf, nc))
    for i in range(nf):
        for j in range(nc):
            f = facilities[i,:]
            c = clients[j,:]
            distances[i,j] = dist(f,c)
            
    start = time.time()
    local_search.ls_kmedian(distances, k)
    end = time.time()
    print("Time: {}".format(end-start))
    with open("res_ours.csv", "a") as out:
        out.write("{},{},{},{}\n".format(nf, nc, k, end-start))

    start = time.time()
    baseline.ls_kmedian(distances, k)
    end = time.time()
    print("Time: {}".format(end-start))
    with open("res_baseline.csv", "a") as out:
        out.write("{},{},{},{}\n".format(nf, nc, k, end-start))


##################################################
# Change k
##################################################
nf = 100
nc = 1000
d = 10
for exponent in np.arange(2, 9):
    k = int(2**exponent)

    for _ in range(REPS):
        run_test(nc, nf, k, d)     

##################################################
# Change nc (Client set size)
##################################################
nf = 100
k = 10
d = 10
for exponent in np.arange(7, 14):
    nc = int(2**exponent)

    for _ in range(REPS):
        run_test(nc, nf, k, d)     

##################################################
# Change nf (Facility set size)
##################################################
nc = 1000
k = 10
d = 10
for exponent in np.arange(7, 12):
    nf = int(2**exponent)

    for _ in range(REPS):
        run_test(nc, nf, k, d)     
