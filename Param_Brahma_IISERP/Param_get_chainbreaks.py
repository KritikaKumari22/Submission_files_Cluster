def get_ATOM_lines_from_PDB_lines(all_PDB_lines):    
    # Long version of the code easy to understand
    ATOM_lines = []
    for line in all_PDB_lines:
        if line.startswith('ATOM'):
            ATOM_lines.append(line)
    
    # Shorter version can be writen in one line
    #ATOM_lines = [line for line in all_PDB_lines if line.startswith('ATOM')]    
    return ATOM_lines
    
def find_chain_breaks(ATOM_lines):
    chain_res_dict = find_chain_wise_residue_list(ATOM_lines)    
    break_dict = find_breaks_from_chain_res_dict(chain_res_dict)
    return break_dict


def find_chain_wise_residue_list(ATOM_lines): 
    # finds a list of residue numbers for each chain    
    # Initiating a dictionary where chain id forms the key and the value is an empty dictioary
    chain_res_dict = dict([(line[21:22],[]) for line in ATOM_lines]) # this is short hand version of a for loop
    
    # Filling the empty dictionary with residue numbers for each chain
    for line in ATOM_lines:        
        chain_res_dict[line[21:22]].append(int(line[22:26].strip()))
    return chain_res_dict

def find_breaks_from_chain_res_dict(chain_res_dict):
    break_dict = {} # dictionary to store breaks
    for chain in chain_res_dict.keys():
        # Finding missing ints from residue number ilst
        k = find_missing_ints_starting_from_1(chain_res_dict[chain])
        if len(k)!=0:
            break_dict[chain] = find_missing_ints_starting_from_1(chain_res_dict[chain])
    return break_dict

def find_missing_ints_starting_from_1(list_of_ints):
    # loop thorugh interger from 1 to largest int in the list
    # if the input has a missing number, store it in a list    
    missing_ints = [] 
    for x in range(1,max(list_of_ints)+1):
        if x not in list_of_ints:
            missing_ints.append(x)
    return missing_ints


import os
import sys

UNK_file="PDBs_w_UNK.txt"
UNK_path="/scratch/madhu/kritika/Depth/Filtered_pdbs/"
UNK__filepath= os.path.join(UNK_path, UNK_file)

Broken_file="Broken_PDBs.txt"
Broken_path="/scratch/madhu/kritika/Depth/Filtered_pdbs/"
Broken_filepath=os.path.join(Broken_path, Broken_file)


filename = sys.argv[1]

with open(filename.strip()) as inf:
                # ensemble_lines = [y for y in inf.readlines()]
                atom_lines = [x for x in inf.readlines() if x.startswith('ATOM')]


                break_dict = find_chain_breaks(atom_lines)
                if len(break_dict) > 0: 
                              
                    with open(Broken_filepath,'a+') as uf:
                                    uf.write(str(filename)+'\n')
                                    missing_Res=[]
                                    for chain in break_dict.keys():
                                        # Finding missing ints from residue number ilst
                                        values_str = ''.join(str(break_dict[chain]))
                                        missing_Res.append(str(chain+':'+values_str))
                                    # missing_Res.append('\n'.join([str(j)+' '+str(filename)+missing_Res+'\n']) 
                                    for  item in missing_Res:
                                        uf.write(item+'\n')
                                    uf.close()
