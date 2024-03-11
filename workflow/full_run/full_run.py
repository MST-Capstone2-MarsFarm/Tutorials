import pandas as pd
#import plantcv as pcv
#import swifter
from pathlib import Path, PosixPath
import os, sys

input_folders = [
    Path("/mnt/stor/ceph/csb/marsfarm/projects/inputs/MV1-0039_7.11.23-8.11.23(Tomato)"),
    Path("/mnt/stor/ceph/csb/marsfarm/projects/inputs/MV1-0041_6.2.23-6.20.23(Peas)"),
    Path("/mnt/stor/ceph/csb/marsfarm/projects/inputs/MV1-0043_6.1.23-6.16.23(Purple Basil)")
]

full_input_paths = []
for folder in input_folders:
    full_input_paths.extend(folder.glob('*.jpg'))
full_input_paths.sort()

#create output files and their directories
output_folder_path = Path("/mnt/stor/ceph/csb/marsfarm/projects/leaf_detection/outputs")
def create_output_file(input_file_path: PosixPath):
    output_path = output_folder_path / input_file_path.parent.name / input_file_path.name
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return str(output_path)
file_output_paths = [create_output_file(input_file_path) for input_file_path in full_input_paths]
input_str_file_paths = tuple(str(input_path) for input_path in full_input_paths)
print(file_output_paths)
#parameters_df = pd.DataFrame({"Input_Path": input_str_file_paths, "Output_Path": file_output_paths})
#print(parameters_df)

#testing for one small dataset
#df['input_path'] = None

#df['input'].swifter.apply(my_func)