import os
import pandas as pd

# Specify the directory containing the .xlsx files
source_directory = '/mnt/stor/ceph/csb/marsfarm/projects/marsfarm_image_analysis/inputs/environment_data_sheets'
# Specify the target directory for the .csv files
target_directory = '/mnt/stor/ceph/csb/marsfarm/projects/marsfarm_image_analysis/inputs/environment_data_csv'

# List all files in the source directory
for filename in os.listdir(source_directory):
    # Check if the file is an Excel file
    if filename.endswith('.xlsx'):
        # Construct the full file path
        file_path = os.path.join(source_directory, filename)
        # Read the Excel file
        df = pd.read_excel(file_path)
        
        # Construct the target CSV file path
        csv_file_path = os.path.join(target_directory, filename.replace('.xlsx', '.csv'))
        # Save the DataFrame to CSV
        df.to_csv(csv_file_path, index=False)

print("Conversion completed.")
