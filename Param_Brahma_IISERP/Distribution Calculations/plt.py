import numpy as np
import pickle
import os
import matplotlib.pyplot as plt

print("Hi")
loaded = np.load("/scratch/madhu/kritika/Depth/compressd_nbrs/7.5A_rnbrs_06_04_clean.npz", allow_pickle=True)
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


with open('/scratch/madhu/kritika/Depth/distribution/Raw_AA_wise_distribn_7.5A.txt', 'a+') as fi:
    for key,value in Nrs.items():
        fi.write(str(key)+" "+str(value)+'\n')


nrs={}
with open('/scratch/madhu/kritika/Depth/distribution/Raw_AA_wise_distribn_7.5A.txt', 'r') as fi:
    for line in fi.readlines():
        if len(line)>0:
            # nrs[str(line.split(' ')[0])]=[]
            # nrs[str(line.split(' ')[0])]= float((line.strip()).split(' ')[1])
                    # Extract the amino acid code from the line
            aa_code = line.split()[0][:3]
            # print(aa_code)

                    # Extract the list following the amino acid code
            lst = line.split(" ")[1:]
            k=[]
            for i in lst:
                k.append(int(i.strip("[").strip(",").strip("]\n")))

            # Add the amino acid code and list to the dictionary
            nrs[aa_code] = k




for key,value in nrs.items():
        y=sorted(value)
        
        # Count frequency of each value in the list
        unique, counts = np.unique(y, return_counts=True)
        frequency = dict(zip(unique, counts))

        ## Create bar plot with frequency of each value
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.bar(frequency.keys(), frequency.values(), color='#b80d1b', alpha=0.8)
        mean=np.mean(y)
        SD=np.std(y)
        print(str(key)+' ',mean, SD)
        plt.rcParams['font.family'] = 'Times New Roman'
        ax.set_xlabel('No. of Residues in a Neighbourhood', fontsize=12,fontweight="bold") # Set x-axis label with font size
        ax.set_ylabel('Frequency of the Neighbourhood', fontsize=12,fontweight="bold") # Set y-axis label with font size
        ax.set_title('Distribution of No. of Residues in a 7.5A Neighbourhood as seen in 22207 PDBs for '+str(key), fontsize=14,fontweight="bold")
        ax.axvspan(np.mean(y)-np.std(y), np.mean(y)+np.std(y), alpha=0.2, color='gray', label='Std Dev: {:.2f}'.format(SD))
        ax.axvline(mean, color='black', linestyle='--', label='Mean: {:.2f}'.format(mean))
        ax.legend(loc='upper right')
        ax.set_xticks(np.arange(0,15,1))
        ax.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.5, zorder=0)
        ax.tick_params(axis='both', labelsize=10)
        plt.savefig('./plot_horizontal'+str(key)+'.png',dpi=400, bbox_inches='tight')
