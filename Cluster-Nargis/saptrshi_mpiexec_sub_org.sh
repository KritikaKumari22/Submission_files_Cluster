#!/bin/bash -l

#$ -S /bin/bash

#$ -cwd

#$ -V



## Change the name below (after -N) to suite your requirement

#$ -N simon_cat



# Change the number of cores demanded (after orte) to suite your code-run requirement

#$ -pe orte 16

## Change the name below (after -o and -e ) to output and error log files

#$ -o out

#$ -e err



## set the queue depending on Job run time.

#$ -q all.q



## Email address to send email to

#$ -M sahanaks@ncbs.res.in



## To send email when job ends or aborts

#$ -m ea



export PATH=$HOME/.conda/envs/simon/bin/python3:$PATH

export PATH=$HOME/.conda/envs/simon/bin/mpiexec:$PATH

python3 = ~/.conda/envs/simon/bin/python3

mpiexec = ~/.conda/envs/simon/bin/mpiexec

echo "Starting MPI job at: " `date`

export MKL_NUM_THREADS=1

export NUMEXPR_NUM_THREADS=1

export OMP_NUM_THREADS=1

echo "Starting MPI job on: " `hostname`

echo "Total cores demanded: " $NSLOTS

echo "Job name given: " $JOB_NAME

echo "Job ID: " $JOB_ID

echo "Starting MPI job..."



## Change the executable to match your path and executable filename (last line with ./xxx)

mpiexec -n 16 python3 mpi_test.py



exit 0
