#!/bin/bash

# Assign the first argument as the job name and use it for creating the Slurm script filename
job_name="stn"

id=$$  # Use the script's process ID to ensure a unique Slurm script filename

# Create a new Slurm job script with unique identifier
slurm_script="PythonJob$id.slurm"

 
echo "#!/bin/sh" > $slurm_script
echo "#SBATCH --job-name=$job_name" >> $slurm_script
echo "#SBATCH --cpus-per-task=1" >> $slurm_script
echo "#SBATCH --mem=6GB" >> $slurm_script
echo "#SBATCH --time=5-00:00:00" >> $slurm_script
echo "#SBATCH --nodes=1" >> $slurm_script
echo "#SBATCH --ntasks=1" >> $slurm_script
echo "#SBATCH --mail-user=ls5288@princeton.edu" >> $slurm_script
echo "#SBATCH --mail-type=ALL" >> $slurm_script
echo "" >> $slurm_script

 
# Commands to load Python and run the specified script
echo "module load anaconda3/2023.3" >> $slurm_script
echo "module load gurobi/12.0.0" >> $slurm_script
echo "conda activate myenv" >> $slurm_script
echo "python main.py" >> $slurm_script

# Make the generated Slurm script executable and submit it
chmod +x $slurm_script
sbatch $slurm_script