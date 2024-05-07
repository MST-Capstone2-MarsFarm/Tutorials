#!/bin/bash

set -Eeo pipefail
# ACTIVATE ANACONDA
eval "$(conda shell.bash hook)"
conda activate plantenv_auto_roi

python auto_roi_example.py
