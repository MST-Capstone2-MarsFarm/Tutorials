#!/bin/bash
#SBATCH -N 3
#SBATCH -n 2

# ACTIVATE ANACONDA
eval "$(conda shell.bash hook)"
conda activate plantenv_pcv4_jupyter

input_dataset1_folder="/mnt/stor/ceph/csb/marsfarm/projects/marsfarm_image_analysis/inputs/MV1-0039_7.11.23-8.11.23(Tomato)"
input_dataset2_folder="/mnt/stor/ceph/csb/marsfarm/projects/marsfarm_image_analysis/inputs/MV1-0041_6.2.23-6.20.23(Peas)"
input_dataset3_folder="/mnt/stor/ceph/csb/marsfarm/projects/marsfarm_image_analysis/inputs/MV1-0043_6.1.23-6.16.23(Purple Basil)"

run_script()
{
    local input_folder=$1
    local output_folder=/mnt/stor/ceph/csb/marsfarm/projects/marsfarm_image_analysis/inputs/masks
    srun --time=1-00:00:00 --nodes=1 --ntasks-per-node=1 --exclusive -p general --job-name=jupyterlab python3 generate_masks.py "$input_folder" $output_folder &
}

run_script "$input_dataset1_folder"
run_script "$input_dataset2_folder"
run_script "$input_dataset3_folder"
wait 