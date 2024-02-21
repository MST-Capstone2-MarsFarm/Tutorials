#!/bin/bash

# ACTIVATE ANACONDA
eval "$(conda shell.bash hook)"
conda activate plantenv_pcv4_jupyter

srun --time=1-00:00:00 -p general --job-name=jupyterlab --pty jupyter lab --no-browser --port=8888