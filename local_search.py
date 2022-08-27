import sys
import getopt
import numpy as np
import pickle
import datetime

def ls_kmedian(facility_distances, k):
    """
    Local search for k-median.

    Input:
    facility_distances: precomputed matrix of facility-to-client distances.
    k: the cardinality of the output facility set.

    Output: a list with the indices of the chosen facilities.
    
    """
    
    facilities = range(facility_distances.shape[0])
    # Initialize facility set randomly
    S = np.random.choice(facilities, k, replace=False)
    converged = False
    times = []
    all_dists = np.min(facility_distances[S,:], axis=0)
    current_cost = np.sum(all_dists)
    
    while not converged:
        start = datetime.datetime.now()
        pre_cost = np.copy(current_cost)
        for pos in range(k):
            # Remove one for local-search swap
            reduced_set = np.delete(S, pos)
            current_S_distances = facility_distances[reduced_set,:]            
            provisional_mins = np.min(current_S_distances, axis=0) # This, instead of taking mins of the whole submatrix, cuts running times substantially
            costs = []

            all_mins = np.minimum(provisional_mins, facility_distances)
            costs = np.sum(all_mins, axis=1)
            if np.min(costs) < current_cost:
                S[pos] = np.argmin(costs)
                current_cost = np.min(costs)
            
        end = datetime.datetime.now()
        times.append((end-start).total_seconds())
        
        converged = pre_cost == current_cost 

    return S
