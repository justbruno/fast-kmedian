import sys
import getopt
import numpy as np
import pickle
import datetime

rng = default_rng()

def km_cost(facility_distances):
    all_dists = np.min(facility_distances, axis=0)
    total_cost = np.sum(all_dists)
    return float(total_cost)#/facility_distances.shape[1]

def compute_cost(S, facility_distances):
    return km_cost(facility_distances)# + reg_lambda*pd_cost(S, pairwise_distance_matrix)


def ls_kmedian(facility_distances, k):
    """
    Local search for k-median.

    Input:
    facility_distances: precomputed matrix of facility-to-client distances.
    k: the cardinality of the output facility set.

    Output: a list with the indices of the chosen facilities.
    
    """

    rs = RandomState(MT19937(SeedSequence(123456789)))
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
    current_cost = compute_cost(S, facility_distances[S,:])
    
    while not converged:        
        pre_cost = np.copy(current_cost)
        for pos in range(k):
            start = datetime.datetime.now()
            # Remove one for local-search swap
            reduced_set = [S[i] for i in range(k) if i != pos]
            current_S_distances = facility_distances[reduced_set,:]
            costs = []
            fS = np.copy(S)
            for f in facilities:
                if f in S:
                    costs.append(np.inf)
                    continue
                else:
                    facility_distances_submat = np.vstack([facility_distances[[f],:], current_S_distances])
                    fS[pos] = f                    
                    cost = compute_cost(fS, facility_distances_submat)

                    all_dists = np.min(facility_distances_submat, axis=0)
                    total_cost = np.sum(all_dists)
                    #cost = float(total_cost)#/facility_distances.shape[1]

                    
                    costs.append(cost)
                    
            # We only make a replacement if the cost improves
            if np.min(costs) < current_cost:
                S[pos] = np.argmin(costs)
                current_cost = np.min(costs)
               
            end = datetime.datetime.now()
            times.append((end-start).total_seconds())
        
        converged = pre_cost == current_cost 
        iterations += 1

    print('Facilities: {}\n'.format(','.join([str(x) for x in S])))        
    print('Cost: {}\n'.format(km_cost(facility_distances[S,:])))
    print('Iterations: {}\n'.format(iterations))
    print('Running times: {}\n'.format(times))
    print('Avg. Running times: {}\n'.format(np.mean(times)))
    print('Med. Running times: {}\n'.format(np.median(times)))
    
if __name__ == "__main__":
   main(sys.argv[1:])
