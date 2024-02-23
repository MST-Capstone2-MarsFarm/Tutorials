import os, sys, shutil
import numpy as np
from plantcv import plantcv as pcv
import pandas as pd
from pandarallel import pandarallel
from scipy.signal import lfilter
from copy import deepcopy
pandarallel.initialize(verbose=0, progress_bar = True)

import matplotlib.pyplot as plt
import gc

from datetime import datetime
from time import mktime

input_folder = "/mnt/stor/ceph/csb/marsfarm/projects/marsfarm_image_analysis/inputs/MV1-0041_6.2.23-6.20.23(Peas)"

#function to calculate the area of an image, using the number of pixels as a proxy for area
def get_area(input_image_path: str):
    img, _, _ = pcv.readimage(filename=input_image_path)
    a = pcv.rgb2gray_lab(rgb_img=img, channel='a')
    thresholded_image = pcv.threshold.otsu(gray_img=a, object_type='dark')
    a_fill = pcv.fill(bin_img=thresholded_image, size=50)
    a_fill = pcv.fill_holes(a_fill)
    
    area = np.count_nonzero(a_fill)
    #for memory management
    #del img, a, thresholded_image, a_fill
    return area
    


#get filenames, sort them from start
picture_names_list = sorted(os.listdir(input_folder))
time_dates_military = [name.split('.jpg')[0] for name in picture_names_list]
time_dates_stripped = [datetime.strptime(datetime_string, "%Y-%m-%d_%H%M") for datetime_string in time_dates_military]
unix_time_list =  [int(mktime(datetime_object.timetuple())) for datetime_object in time_dates_stripped]
#calculate the number of hours since the taking of the first image
start_time = unix_time_list[0]
unix_times_from_start = [unix_time - start_time for unix_time in unix_time_list]
hours_from_start = [(unix_time // 3600) for unix_time in unix_times_from_start]

#get file names to calculate areas
file_names = sorted([os.path.join(input_folder, file) for file in os.listdir(input_folder)])
limit_size = -1
file_names_series = pd.Series(file_names)
#print(len(file_names_series))

#calculate the areas
#get from cache if already calculated (as csv file)
if os.path.isfile("areas.csv"): areas = pd.read_csv("areas.csv")['0']
else:
    areas_series = file_names_series.parallel_map(get_area)
    areas_series.to_csv("areas.csv", index=False)
    areas = areas_series.tolist()

graph_dataframe = pd.DataFrame({"area": areas, "hours_from_start": hours_from_start})

#filtered_df = deepcopy(graph_dataframe)

#filter dataframe using difference and iqr instead of relative difference
graph_dataframe['diff'] = graph_dataframe['area'].diff()
graph_dataframe.loc[0, 'diff'] = 0
graph_dataframe['diff'].to_csv('diff.csv', header=False, index=False)
Q1 = graph_dataframe['diff'].quantile(.25)
Q3 = graph_dataframe['diff'].quantile(.75)
IQR = Q3 - Q1
#print(IQR)
#print(Q1 - 1.5 * IQR)
#print(Q3 + 1.5 * IQR)
#find the values with a large variation

#keep looping until all of the spikes are removed
filtered_df = deepcopy(graph_dataframe)
tail_ends = []
spike_length = 1

#5 seems like a reasonable length to prepare for in case of a plateau
while spike_length < 5:
    #first get the pool of anomolous changes in area by finding the ones outside of iqr of the original graph
    filtered_df['diff'] = filtered_df['area'].diff()
    filtered_df.loc[0, 'diff'] = 0
    #find all columns that increase a lot or decrease a lot
    columns_to_remove_increase = filtered_df[(filtered_df['diff'] > (Q3 + 1.5 * IQR)) & ~filtered_df.index.isin(tail_ends)]
    columns_to_remove_decrease = filtered_df[(filtered_df['diff'] < (Q1 - 1.5 * IQR)) & ~filtered_df.index.isin(tail_ends)]
    columns_to_remove_inc_list = columns_to_remove_increase.index.tolist()
    columns_to_remove_dec_list = columns_to_remove_decrease.index.tolist()
    columns_to_remove_list = sorted(columns_to_remove_dec_list + columns_to_remove_inc_list)
    print(f"potential columns to remove {columns_to_remove_list}")
    
    #filter out the large jumps to only select spikes (i.e. values that jump one way and then another very quickly)
    #only remove the values that spike (i.e. quickly come up and down) for everything except the last element in (spike_length) group of elements
    selected_values = [columns_to_remove_inc_list[i] for i in range(len(columns_to_remove_inc_list) - 1) if (columns_to_remove_inc_list[i] + spike_length in columns_to_remove_dec_list) or i==len(graph_dataframe)-1]
    selected_values.extend([columns_to_remove_dec_list[i] for i in range(len(columns_to_remove_dec_list) - 1) if (columns_to_remove_dec_list[i] + spike_length in columns_to_remove_inc_list) or i==len(graph_dataframe)-1])

    tail_ends.extend([selected_value+spike_length for selected_value in selected_values])
    tail_ends.sort()
    selected_values = [num for i in selected_values for num in tuple(range(i, i + spike_length))]
    print(f"selected values {selected_values}")
    print(f"tail ends: {tail_ends}")
    print()
    #exit the loop if no values to remove were found
    #if not selected_values: break
    filtered_df = filtered_df[~filtered_df.index.isin(selected_values)]
    spike_length += 1



n = len(graph_dataframe)
b = [1.0 / n] * n
a = 1
filtered_df['smoothed'] = lfilter(b, a, filtered_df['area'].tolist())
filtered_df['rolling_mean'] = filtered_df['area'].rolling(window=5).mean()     
#print(pct_change_list)
#filtered_df = graph_dataframe[graph_dataframe['pct_change'].abs() <= 0.5]
#print(filtered_df['pct_change'].tolist())

#since the differentials in time are so small, having a 50% spike margin seems like a somewhat reasonable guess that won't remove normal observations
#condition = graph_dataframe['area'] > 1.5 * graph_dataframe['area'].shift(1)
#filtered_df = graph_dataframe[~condition | graph_dataframe.index.isin([0])]



plt.clf()
fig, axes = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(10,8))
fig.suptitle("Plant Area Over Time")

axes[0,0].plot(graph_dataframe['hours_from_start'], graph_dataframe['area'])
axes[0,0].set_title("Raw Results")
axes[0,1].plot(filtered_df['hours_from_start'], filtered_df['area'])
axes[0,1].set_title("50% Difference Removals")
axes[1,0].plot(filtered_df['hours_from_start'], filtered_df['rolling_mean'])
axes[1,0].set_title("50% Difference + Rolling Mean")
axes[1,1].plot(filtered_df['hours_from_start'], filtered_df['smoothed'])
axes[1,1].set_title("50% Difference Smoothed")

for ax in axes.flat:
    ax.set(xlabel="Time (hours)", ylabel="Plant area (pixels)")
plt.tight_layout()

plt.savefig("results.png")