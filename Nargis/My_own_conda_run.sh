#!/bin/bash -l
#$ -S /bin/bash
#$ -cwd
#$ -V

## Change the name below (after -N) to suite your requirement
#$ -N MSA_Covers

# Change the number of cores demanded (after orte) to suite your code-run requirement
#$ -pe orte 64
## Change the name below (after -o and -e ) to output and error log files
#$ -o Job_result.out
#$ -e Job_error.out

## set the queue depending on Job run time.
#$ -q all.q

## Email address to send email to
#$ -M kritikak@ncbs.res.in

## To send email when job ends or aborts
#$ -m ea

echo "Starting MPI job at: " `date`
echo "Starting MPI job on: " `hostname`
echo "Total cores demanded: " $NSLOTS
echo "Job name given: " $JOB_NAME
echo "Job ID: " $JOB_ID
echo "Starting MPI job..."

#module load /softwares/python-3.6.6/bin/python3.6
#module load /softwares/miniconda/bin/python3.9
module load /home/thattai/kritikak/miniconda3/bin/python3.11
#source activate /home/thattai/kritikak/miniconda3/envs/Kritika
#mpiexec=/home/thattai/kritikak/miniconda3/envs/Kritika/bin/mpiexec

#module load /softwares/miniconda/bin/python3.9
source activate /home/thattai/kritikak/.conda/envs/KK



cd /home/thattai/kritikak/MSA_covers

## Change the executable to match your path and executable filename (last line with ./xxx)
##mpiexec -n 32 python t.py

python Plot_ordereddMX.py

exit 0
