#$ -S /bin/bash
#####$ -cwd
####$ -V
#$ -N KK_merge
#$ -pe mpi 32
#$ -q all.q
#$ -o merg_o
#$ -e merg_e
echo ------------------------------------------------------
echo "Starting MPI job at: " `date`
echo "Starting MPI job on: " `hostname`
echo ------------------------------------------------------
echo "Total cores demanded: " $NSLOTS
echo "Job name given: " $JOB_NAME
echo "Job ID: " $JOB_ID
echo ------------------------------------------------------
#module load /softwares/anaconda3/bin/python3
cd /home/thattai/kritikak
export PATH=.conda/envs/KK:$PATH
python3=~/.conda/envs/KK/bin/python3
##mpiexec=~/.conda/envs/KK/bin/mpiexec
##echo "Current working directory: $(pwd)"
##cd /home/thattai/kritikak
##$mpiexec -n 32 $python3 h.py
$python3 m2.py
