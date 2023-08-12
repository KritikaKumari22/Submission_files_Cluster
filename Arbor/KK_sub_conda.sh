#$ -S /bin/bash
#$ -N KK
#$ -pe mpi 16
#$ -q all.q
#$ -o job_o
#$ -e job_e
echo ------------------------------------------------------
echo "Starting MPI job at: " `date`
echo "Starting MPI job on: " `hostname`
echo ------------------------------------------------------
echo "Total cores demanded: " $NSLOTS
echo "Job name given: " $JOB_NAME
echo "Job ID: " $JOB_ID
echo ------------------------------------------------------
cd /home/thattai/kritikak
export PATH=.conda/envs/KK:$PATH
#echo "Current working directory: $(pwd)"

~/.conda/envs/KK/bin/python3 ./t.py