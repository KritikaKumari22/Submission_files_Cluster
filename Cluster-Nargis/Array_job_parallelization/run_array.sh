#!/bin/bash -l
#$ -S /bin/bash
#$ -cwd
#$ -V
####$ -l gpu=1
####################$ -pe smp 1
#$ -pe mpi 1
#$ -l h_vmem=120G
#$ -q short.q
#$ -N Fr13e_1
#$ -t 1-10
#$ -tc 5
#$ -j n
#$ -e /home/thattai/kritikak/Param_Brahma_IISERP/Mk_array_job/Err_\$TASK_ID
#$ -o /home/thattai/kritikak/Param_Brahma_IISERP/Mk_array_job/Res_\$TASK_ID
####$ -l qname=array-job



start_time=$(date +"%Y-%m-%d %H:%M:%S")
echo "Starting MPI job: $JOB_NAME with Job-ID: $JOB_ID On: `date` at: $start_time"
echo "Starting on Node: `hostname` with total cores: $NSLOTS Task ID is: $SGE_TASK_ID"


conda activate /home/thattai/kritikak/.conda/envs/KK

hostname

# Reading an array as lines from cmd list file and indexing the array with array index
IFS=$'\n' read -d '' -r -a array < cmd_list
var="${array[$SGE_TASK_ID-1]}"

echo "$var"

$var

end_time=$(date +"%Y-%m-%d %H:%M:%S")

start_timestamp=$(date -d "$start_time" +%s)
end_timestamp=$(date -d "$end_time" +%s)
time_taken=$((end_timestamp - start_timestamp))
echo "Job started at: $start_time"
echo "Job finished at: $end_time"
echo "Time taken for the job: $time_taken seconds"

