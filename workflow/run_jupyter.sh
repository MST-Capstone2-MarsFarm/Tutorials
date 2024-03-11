#!/bin/bash

# ACTIVATE ANACONDA
eval "$(conda shell.bash hook)"
conda activate plantenv_pcv4_jupyter

srun --time=1-00:00:00 -p general --job-name=jupyterlab jupyter lab --no-browser --port=8888 > /dev/null 2>&1 &
#get node name that you most recently submitted
compute_node_name="$(squeue --noheader -u $(whoami) --format=%N | tail -n 1)"
sleep 5
#this should work if you don't submit any other sbatch jobs simultaneously
echo "use this node name for the ssh command to run jupyter on a browser"
echo $compute_node_name
echo "$(squeue --noheader -u $(whoami) --format=%N | tail -n 1)"
echo 
wait
