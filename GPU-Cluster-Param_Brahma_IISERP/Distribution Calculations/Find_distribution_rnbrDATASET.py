import glob
import os
import numpy as np

os.chdir("/scratch/madhu/kritika/Depth/radial_nbrDATASET/")
files = glob.iglob('*.npz')

temp = {}
for file in files:
    print(str(file))
    d = np.load(file, allow_pickle=True)
    try:
        for i in d['x'][0]:
            key = i[0]
            if len(i)>2:
                val = tuple(i[1:-1])
                if key not in temp:
                    temp[key] = []
                    temp[key].append(val)
                elif key in temp:
                    temp[key].append(val)
    except:
        print("This file "+str(file)+" has no nbrs in it")

Nrs={}
for key,values in temp.items():
    Nrs[key]=[]
    for v in values:
        Nrs[key].append(len(v))

for key in Nrs:
    Nrs[key] = [sum(Nrs[key]) / len(Nrs[key])]

print(Nrs)
for key,value in Nrs.items():
    print("Amino acid: ",str(key)," avg no. of residues in neighbourhood = ", str(value))
