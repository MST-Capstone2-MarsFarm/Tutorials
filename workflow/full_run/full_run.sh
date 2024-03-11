#!/bin/bash

# ACTIVATE ANACONDA
eval "$(conda shell.bash hook)"
conda activate plantenv_pcv4_jupyter

NUM_CPUS=$(sinfo -e -N -h -O cpus | head -n 1 | awk '{print $1}')
srun --time=2-00:00:00 --cpus-per-task=$NUM_CPUS --tasks-per-node=1 --ntasks=1 -p general --job-name=leaf_detection python3 full_run.py