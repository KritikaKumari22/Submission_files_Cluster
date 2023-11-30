template_script = '''#!/bin/bash -l
#$ -S /bin/bash
#$ -cwd
#$ -V

## Change the name below (after -N) to suite your requirement
#$ -N coat13_permutes_{}

# Change the number of cores demanded (after orte) to suite your code-run requirement
#$ -pe orte 200
## Change the name below (after -o and -e ) to output and error log files
#$ -o 13_permutes_result_{}.out
#$ -e 13_permutes_error_{}.out

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

module load /softwares/miniconda/bin/python3.9
conda activate /home/thattai/kritikak/.conda/envs/KK

cd /home/thattai/kritikak/Graph_solus/4_comp13/

python get_coat_labels2.py

exit 0
'''

for i in range(1, 5):
    with open(f'coats2_{i}.sh', 'w') as f:
        f.write(template_script.format(i, i, i))
