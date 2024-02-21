#!/bin/bash

# ACTIVATE ANACONDA
eval "$(conda shell.bash hook)"
conda activate plantenv_pcv4_jupyter

python3 generate_masks.py