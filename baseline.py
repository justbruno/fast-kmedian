import sys
import getopt
import numpy as np
import pickle
import datetime

def compute_cost(S, facility_distances, clients):
    floating_cost = 0
    for c in clients:
        mindist = np.inf
        for fac in S:
            dist = facility_distances[fac, c]
            if dist < mindist:
                mindist = dist
                
        floating_cost += mindist

    return floating_cost


def ls_kmedian(facility_distances, k):
    """
    Local search for k-median.

    Input:
    facility_distances: precomputed matrix of facility-to-client distances.
    k: the cardinality of the output facility set.

    Output: a list with the indices of the chosen facilities.
    
    """
    nf = facility_distances.shape[0]
    nc = facility_distances.shape[1]
    
    facilities = range(nf)
    clients = range(nc)
    # Initialize facility set randomly
    S = np.random.choice(facilities, k, replace=False)
    print("initial set: ", S)
    converged = False
    iterations = 0
    times = []
    current_cost = compute_cost(S, facility_distances, clients)
    
    while not converged:        
        pre_cost = np.copy(current_cost)
        improved = False
        start = datetime.datetime.now()
        for pos in range(k):
            # Remove one for local-search swap

            candidate_mincost = np.inf
            winner = None
            for f in facilities:
                if f in S:
                    continue
                fS = np.copy(S)
                fS[pos] = f

                floating_cost = compute_cost(fS, facility_distances, clients)

                if floating_cost < candidate_mincost:
                    candidate_mincost = floating_cost
                    winner = f
                fS[pos] = f                    
            # We only make a replacement if the cost improves
            if candidate_mincost < current_cost:
                S[pos] = winner
                current_cost = candidate_mincost
                improved = True
               
        end = datetime.datetime.now()
        times.append((end-start).total_seconds())
        
        converged = pre_cost == current_cost 
        iterations += 1
