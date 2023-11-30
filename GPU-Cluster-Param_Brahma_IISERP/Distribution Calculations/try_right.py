import numpy as np
import pickle

# Load data
loaded = np.load("/scratch/madhu/kritika/Depth/compressd_nbrs/6.5A_rnbrs_17_03_clean.npz", allow_pickle=True)
D = loaded['x']

#Divide and Conquer A, right half
mid = len(D) // 2
D_right = D[mid:]

# Divide D into 10 equal parts
part_size = len(D_right) // 20
for j in range(20):
    # Get the slice of D for this part
    part_D = D_right[j*part_size : (j+1)*part_size]
    
    # Calculate temp dictionary for this part
    temp = {}
    for i in part_D:
        key = i[0]
        if len(i) > 2:
            val = tuple(i[1:-1])
            if key not in temp or val not in temp[key]:
                if key not in temp:
                    temp[key] = []
                temp[key].append(val)

    # Calculate Nrs dictionary for this part
    Nrs = {}
    for key, values in temp.items():
        Nrs[key] = []
        for v in values:
            Nrs[key].append(len(v))
    for key in Nrs:
        Nrs[key] = [sum(Nrs[key]) / len(Nrs[key])]

    # Save Nrs dictionary to pickle file
    with open(f"/scratch/madhu/kritika/Depth/scoring_nbrs/distribution/Rightpart_{j}.pickle", "wb") as f:
        pickle.dump(Nrs, f)
