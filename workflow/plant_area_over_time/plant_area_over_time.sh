#!/bin/bash

# ACTIVATE ANACONDA
eval "$(conda shell.bash hook)"
conda activate plantenv_pcv4_jupyter

srun --time=1-00:00:00 -p general --job-name=plant_area_over_time python3 plant_area_over_time.py