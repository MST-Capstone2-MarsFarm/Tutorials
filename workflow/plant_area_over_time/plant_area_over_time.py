import os, sys, shutil

from datetime import datetime
from time import mktime

input_folder = "/mnt/stor/ceph/csb/marsfarm/projects/marsfarm_image_analysis/inputs/MV1-0041_6.2.23-6.20.23(Peas)"

#get filenames, sort them from start
picture_names_list = sorted(os.listdir(input_folder))

time_dates_military = [name.split('.jpg')[0] for name in picture_names_list]

time_dates_stripped = [datetime.strptime(datetime_string, "%Y-%m-%d_%H%M") for datetime_string in time_dates_military]

unix_time_list =  [int(mktime(datetime_object.timetuple())) for datetime_object in time_dates_stripped]

start_time = unix_time_list[0]
unix_times_from_start = [unix_time - start_time for unix_time in unix_time_list]
hours_from_start = [(unix_time // 3600) for unix_time in unix_times_from_start]

#print([picture_names_list[0], picture_names_list[2]])
#print([time_dates_military[0], time_dates_military[2]])
#print([time_dates_stripped[0], time_dates_stripped[2]])
#print([unix_times_from_start[0], unix_times_from_start[2]])
print()
print(hours_from_start)