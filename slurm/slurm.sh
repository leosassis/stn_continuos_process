#!/bin/bash

#SBATCH --job-name=PythonArrayJob                            	 # Job name
#SBATCH --time=24:00:00                                     	 # Walltime
#SBATCH --ntasks=1                                          	 # Number of processor cores (i.e. tasks)
#SBATCH --nodes=1                                           	 # Number of nodes
#SBATCH --mem-per-cpu=6144M                                 	 # Memory per CPU core
#SBATCH --output=logs/PythonJob%A_%a.slurm     			 # Standard output
#SBATCH --error=logs/PythonJob%A_%a.err        			 # Standard error
#SBATCH --constraint=cascade                                	 # CPU type constraint

# Load necessary modules
module load anaconda3/2023.3
module load gurobi/12.0.0

# Activate Conda environment
conda activate myenv

# Run python script with the SLURM array task ID as argument
python main.py $SLURM_ARRAY_TASK_ID

# HOW TO RUN: sbatch --array=1-100 slurm.sh. This will run instances with IDS from 1 to 100 in parallel.
# HOW TO RUN: sbatch --array=2,10,15,67,98 slurm.sh. This will run run tasks with IDs [2, 10, 15, 67, 98] in parallel.