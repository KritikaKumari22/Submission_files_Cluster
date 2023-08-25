#Usage python3 file.py <pdb_list> <out_dir> <work_id>
# saves pdb in the name pdb-residue_depth.pdb

from make_depth_db_module import Make_depth_db
import pickle
import sys

pdb_list_file = sys.argv[1]
out_dir = sys.argv[2]
work_id = sys.argv[3]

with open(pdb_list_file, 'rb') as inf:
    pdb_list =  pickle.load(inf)

mdd = Make_depth_db(work_id = work_id)
mdd.calc_depth_for_pdb_list(pdb_list,out_dir)
