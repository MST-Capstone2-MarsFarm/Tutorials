#!/bin/bash

# ACTIVATE ANACONDA
eval "$(conda shell.bash hook)"
conda activate plantenv_pcv4_jupyter

#jupyter lab --no-browser --allow-root
srun --time=1-00:00:00 -p general --job-name=convert_sheets python3 convert_sheets.py
#jupyter lab --no-browser --port=9999