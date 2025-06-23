#!/bin/bash

#SBATCH --time=24:00:00                                     # walltime
#SBATCH --ntasks=1                                          # number of processor cores (i.e. tasks)
#SBATCH --nodes=1                                           # number of nodes
#SBATCH --mem-per-cpu=6144M                                 # memory per CPU core
#SBATCH --output=logs/PythonJob%j_$SLURM_ARRAY_TASK_ID.slurm     # standard output
#SBATCH --error=logs/PythonJob%j_$SLURM_ARRAY_TASK_ID.err        # standard error
#SBATCH --constraint=cascade                                # CPU type constraint

# Load necessary modules
module load anaconda3/2023.3
module load gurobi/12.0.0

# Activate Conda environment
conda activate myenv

# Run python script with the SLURM array task ID as argument
python main.py $SLURM_ARRAY_TASK_ID

# HOW TO RUN: sbatch --array=1-100 slurm/slurm.sh. This will run instances with IDS from 1 to 100 in parallel.