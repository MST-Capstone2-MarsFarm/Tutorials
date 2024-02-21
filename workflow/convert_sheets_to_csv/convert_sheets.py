import pandas as pd
import os, glob.glob

def convert_to_csv(input_sheets_path: str, output_csv_path: str):
    pass

input_sheets_folder = "/mnt/stor/ceph/csb/marsfarm/projects/marsfarm_image_analysis/inputs/environment_data_sheets"
output_csvs_folder = "/mnt/stor/ceph/csb/marsfarm/projects/marsfarm_image_analysis/inputs/environment_data_csv"

input_pattern = os.path.join(input_sheets_folder, '*.xlsx')

xlsx_files = glob(input_pattern)

csv_output_files = [os.path.join(dest_dir, os.path.basename(x).replace('.xlsx', '.csv')) for x in xlsx_files]

