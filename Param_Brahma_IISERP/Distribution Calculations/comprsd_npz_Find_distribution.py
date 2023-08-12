import numpy as np
import pickle

print("Hi")
loaded = np.load("/scratch/madhu/kritika/Depth/compressd_nbrs/6A_rnbrs_29_03_clean.npz", allow_pickle=True)

D = loaded['x']
print("This is the length of the no, of nbrhoods, not necessarily unique: ",len(D))
temp = {}

for i in D:
    key = i[0]
    if len(i)>2:
        val = tuple(i[1:-1])
        if key not in temp:
            temp[key] = []
            temp[key].append(val)
        elif key in temp:
            temp[key].append(val)


Nrs={}
for key,values in temp.items():
    Nrs[key]=[]
    for v in values:
        # v=tuple(v)
        Nrs[key].append(len(v))

for key in Nrs:
    Nrs[key] = [sum(Nrs[key]) / len(Nrs[key])]

#print(Nrs)
#for key,value in Nrs.items():
    #print("Amino acid: ",key," avg no. of residues in neighbourhood = ", str(value))
with open('/scratch/madhu/kritika/Depth/distribution/new_Cleaned_6A_Dstrbutn_30_03.txt', 'a+') as fi:
    for key,value in Nrs.items():
        fi.write("Amino acid: "+str(key)+" avg no. of residues in neighbourhood = "+str(value[0])+'\n')
