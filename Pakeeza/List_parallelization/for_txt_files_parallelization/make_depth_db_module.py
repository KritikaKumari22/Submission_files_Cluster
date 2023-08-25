class Make_depth_db:
    def __init__(self,work_id='',work_dir='./work_dir'):
        self.work_id = work_id
        self.work_dir = work_dir+work_id
        # self.depth_exe = './DEPTH'
        #self.req_file_ends = ['-atomic_depth.pdb','-residue_depth.pdb','out-atom.depth','out-residue.depth']
        #self.req_file_ends = ['-atomic_depth.pdb']
        self.req_file_ends = ['-residue_depth.pdb']
        #self.req_file_ends = ['-atomic_depth.pdb']
        pass

    def calc_depth_for_pdb_list(self,pdb_list,out_dir):
        for pdb in pdb_list:
            self.generate_atom_depth_file(pdb,out_dir)
    
    def generate_atom_depth_file(self,pdb,out_dir):
        self.setup_work_dir()
        self.run_depth(pdb)
        self.move_files(out_dir)
        self.clean_up()
    
    def setup_work_dir(self):
        import os
        try:
            os.makedirs(self.work_dir)
        except:
            pass

    def run_depth(self,pdb):
        import os
        pwd = os.getcwd()
        os.chdir(self.work_dir)
        pdb_with_apostrophes = '\'' + pdb + '\''
        depth_cmd = 'python '+pwd+'/all_graphs.py '+ pdb_with_apostrophes
        print(depth_cmd)
        os.system(depth_cmd)
        os.chdir(pwd)

    def move_files(self,out_dir):
        import os
        file_list = os.listdir(self.work_dir)

        self.required_files = [x for x in file_list if self.in_req_list(x)]

        for file in self.required_files:
            cmd = 'cp '+self.work_dir+'/'+file+' '+out_dir+'/'
            print(cmd)
            os.system(cmd)
    
    def clean_up(self):
        import os
        cmd = 'rm -r '+self.work_dir
        print(cmd)
        os.system(cmd)
    def in_req_list(self,x):
        for y in self.req_file_ends:
            if x.endswith(y):
                return True
        return False

