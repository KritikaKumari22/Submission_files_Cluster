#!/bin/bash -l
#$ -S /bin/bash
#$ -cwd
#$ -V

## Change the name below (after -N) to suite your requirement
#$ -N f4c12

# Change the number of cores demanded (after orte) to suite your code-run requirement
#$ -pe orte 256
## Change the name below (after -o and -e ) to output and error log files
#$ -o 4c12_result.out
#$ -e 4c12_error.out

## set the queue depending on Job run time.
#$ -q all.q

start_time=$(date +"%Y-%m-%d %H:%M:%S")

# Rest of your submission script
echo "Starting MPI job at: $start_time"

# Rest of your submission script
echo "Starting MPI job at: " `date`
echo "Starting MPI job on: " `hostname`
echo "Total cores demanded: " $NSLOTS
echo "Job name given: " $JOB_NAME
echo "Job ID: " $JOB_ID
echo "Starting MPI job..."

#module load /softwares/python-3.6.6/bin/python3.6
# module load /softwares/miniconda/bin/python3.9
conda activate /home/thattai/kritikak/.conda/envs/KK


cd /home/thattai/kritikak/Param_Brahma_IISERP/


cmd_list="command_list"  # Replace with the path to your list of commands
while read cmd; do
    bash -c "$cmd" &
done < "$cmd_list"

wait

end_time=$(date +"%Y-%m-%d %H:%M:%S")

# Calculate the time taken for the job
start_timestamp=$(date -d "$start_time" +%s)
end_timestamp=$(date -d "$end_time" +%s)
time_taken=$((end_timestamp - start_timestamp))

echo "Job finished at: $end_time"
echo "Time taken for the job: $time_taken seconds"
