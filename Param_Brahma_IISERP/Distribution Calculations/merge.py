import pickle
from collections import defaultdict

#Merging
# Merge Nrs dictionaries from left all parts
Nrs_merged = defaultdict(list)
for i in range(20):
    # Load Nrs dictionary from pickle file
    with open(f"Leftpart_{i}.pickle", "rb") as f:
        Nrs_part = pickle.load(f)

    # Merge Nrs_part with Nrs_merged
    for key, value in Nrs_part.items():
        Nrs_merged[key].extend(value)

# Merge Nrs dictionaries from right all parts
for j in range(20):
    # Load Nrs dictionary from pickle file
    with open(f"Rightpart_{j}.pickle", "rb") as fi:
        Nrs_part_r = pickle.load(fi)

    # Merge Nrs_part with Nrs_merged
    for key, value in Nrs_part_r.items():
        Nrs_merged[key].extend(value)

# Average values for each key
Nrs_avg = {}
for key, values in Nrs_merged.items():
    Nrs_avg[key] = sum(values) / len(values)

for key,value in Nrs_avg.items():
    print("Amino acid: ",str(key)," avg no. of residues in neighbourhood = ", str(value))
