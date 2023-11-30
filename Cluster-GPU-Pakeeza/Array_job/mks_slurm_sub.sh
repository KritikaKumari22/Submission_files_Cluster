./rv_hem_glu_trimer_openmm_min/run_array.sh
#!/bin/bash
#SBATCH --job-name=MK_rv_min
#SBATCH --time=4-00:00:00
#SBATCH --gres=gpu:1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
##SBATCH --mem=50GB
#SBATCH --partition=gpu
#SBATCH --output=MIN-%A_%a.out
#SBATCH --error=MIN-%A_%a.err
#SBATCH --array=1-11%11
#SBATCH --qos=array-job

cd $SLURM_SUBMIT_DIR

hostname

## reading an array as lines from cmd list file and indexing the array with array index
old_ifs=$IFS
IFS='
'
array=($(cat cmd_list))
var=${array[`expr $SLURM_ARRAY_TASK_ID - 1`]}
IFS=$old_ifs

echo $var

$var