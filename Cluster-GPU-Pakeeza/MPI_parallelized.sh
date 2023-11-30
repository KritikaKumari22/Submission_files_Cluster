#!/bin/bash -l
#$ -S /bin/bash
#$ -cwd
#$ -V

## Change the name below (after -N) to suite your requirement
#$ -N c4_13

# Change the number of cores demanded (after orte) to suite your code-run requirement
#$ -pe orte 128
## Change the name below (after -o and -e ) to output and error log files
#$ -o c4_13_result.out
#$ -e c4_13_error.out

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
module load /softwares/miniconda/bin/python3.9
conda activate /home/thattai/kritikak/.conda/envs/KK



cd /home/thattai/kritikak/Graph_solus

## Change the executable to match your path and executable filename (last line with ./xxx)
mpiexec -n 128 j3.py
exit 0
