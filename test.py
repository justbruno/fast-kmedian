import numpy as np
from numpy.linalg import norm

import local_search
import baseline

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
            
    np.random.seed(0)
    S_ours = local_search.ls_kmedian(distances, k)

    np.random.seed(0)
    S_baseline = baseline.ls_kmedian(distances, k)

    return np.all(S_ours == S_baseline)

    
    
nf = 100
nc = 200
k = 10
d = 10
for _ in range(REPS):
    print("="*50) 
    print("Running test: {}, {}, {}, {}".format(nc, nf, k, d))
    success = run_test(nc, nf, k, d)
    print("Result: {}".format("OK" if success else "FAILED"))
    print("-"*50) 

    
