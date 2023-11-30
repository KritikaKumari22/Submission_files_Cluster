#$ -S /bin/bash
#$ -N sarek_XXX
#$ -pe mpi 28
#$ -q all.q
echo ------------------------------------------------------
echo -n 'Job is running on node '; cat $PBS_NODEFILE
echo ------------------------------------------------------
echo PBS: qsub is running on $PBS_O_HOST
echo PBS: originating queue is $PBS_O_QUEUE
echo PBS: executing queue is $PBS_QUEUE
echo PBS: working directory is $PBS_O_WORKDIR
echo PBS: execution mode is $PBS_ENVIRONMENT
echo PBS: job identifier is $PBS_JOBID
echo PBS: job name is $PBS_JOBNAME
echo PBS: node file is $PBS_NODEFILE
echo PBS: current home directory is $PBS_O_HOME
echo PBS: PATH = $PBS_O_PATH
echo ------------------------------------------------------

# set the sarek path
sarekPath=/home/sabari/sabari/sarek_3.1.2/
# the docker images were available in the above path
cd /home/sabari/sabari/dataset/ov/sarek/XXX

# set the specific java version, which nextflow requires
export JAVA_HOME=/softwares/jdk-16.0.1/

#alignment and recalibration
/home/sabari/sabari/nextflow run /home/sabari/sabari/sarek_3.1.2/nf-core-sarek-3.1.2/workflow/main.nf -profile singularity --tools Mutect2 --input input.csv --outdir . --igenomes_base /home/sabari/sabari/sarek_3.1.2/references/ --wes --intervals /home/sabari/sabari/dataset/ov/sarek/truseqhg38_sorted.bed --max_memory '240.GB' --max_cpus 28 --tools mutect2,vep

##module load /softwares/anaconda3/bin/python3.9
##source /softwares/anaconda3/bin/activate
module load /softwares/anaconda3/bin/python3.9
##conda activate /home/thattai/kritikak/ .conda/envs/KK

cd /home/thattai/kritikak

python t.py
exit 0