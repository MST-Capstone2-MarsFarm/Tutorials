#!/bin/bash

# ACTIVATE ANACONDA
eval "$(conda shell.bash hook)"
conda activate plantenv_pcv4_jupyter

srun --time=1-00:00:00 -p general --job-name=jupyterlab jupyter lab --no-browser --port=8888 &
echo "$(squeue -u $(whoami))"
wait