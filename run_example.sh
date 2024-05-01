#!/bin/bash

set -Eeo pipefail
# ACTIVATE ANACONDA
eval "$(conda shell.bash hook)"
conda activate plantenv_pcv4_jupyter

python calculate_rois.py
