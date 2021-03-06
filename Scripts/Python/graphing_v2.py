# Done - Debug Data With Missing Graphs
# Done - Preset Workspace Variables
# Done - remove first outlier data point
# Done - Save all pictures for data
# Done - Shift Manav's data left by 5 seconds (scrap out first 5 seconds)
# Done - apply filter
# TODO - Confirm noise is being removed
# TODO - Maybe consider building bar graph on python?
# TODO - Add a README file

import numpy as np
from scipy import stats, signal, fft, ifft
from scipy.fftpack import fftshift
import math
import matplotlib as mpl
import matplotlib.pyplot as plt


def preset_params():
    mpl.rcParams['figure.subplot.wspace'] = .2
    mpl.rcParams['figure.subplot.hspace'] = .70
    mpl.rcParams['figure.subplot.left'] = .11
    mpl.rcParams['figure.subplot.bottom'] = .10
    mpl.rcParams['figure.subplot.right'] = .98
    mpl.rcParams['figure.subplot.top'] = .94
    mpl.rcParams['axes.titlesize'] = 'small'
    mpl.rcParams['axes.labelsize'] = 'small'


def selecting_files_read(file_handle, local_person_reading_pos):
    team_members = ['Andreea', 'Malek', 'Manav', 'Maureen']
    maureen_files = ['Maureen_Participant 1_Part 1.csv', 'Maureen_Participant 1_Part 2.csv', 'Maureen_Participant 2_Part 1.csv', 'Maureen_Participant 2_Part 2.csv']
    manav_files = ['Participant1_out.csv', 'Participant1_In.csv', 'Participant2_in.csv', 'Participant2_out.csv', 'Participant3_in.csv', 'Participant3_out.csv', 'Participant4_in.csv', 'Participant4_out.csv']
    andreea_files =['AR- in context.csv', 'AR- out of context.csv', 'JR- in context.csv', 'JR-out of context.csv', 'OK- in context.csv', 'OK- out of context.csv', 'VS in context.csv', 'VS out of context.csv']
    malek_files = ['CDP1_MM.csv', 'CDP2_MM.csv', 'DW1_MM.csv', 'DW2_MM.csv']
    local_person_reading_name = team_members[local_person_reading_pos]
    local_files_read = []
    if local_person_reading_pos == 0:
        local_files_read = andreea_files
        file_handle.write('\nSaving Andreea\'s files')
    elif local_person_reading_pos == 1:
        local_files_read = malek_files
        file_handle.write('\nSaving Malek\'s files')
    elif local_person_reading_pos == 2:
        local_files_read = manav_files
        file_handle.write('\nSaving Manav\'s files')
    elif local_person_reading_pos == 3:
        local_files_read = maureen_files
        file_handle.write('\nSaving Maureen\'s files')
    else:
        file_handle.write("\nNot reading in any data")
    return local_person_reading_name, local_files_read


def reading_in_file(file_handle, file_path):
    local_point_id, local_total_micro, local_minutes, local_sec, local_val = np.loadtxt(file_path, skiprows=1, unpack=True, delimiter=",")

    # pre-processing

    # getting rid of Nan values
    if np.isnan(np.sum(local_val)):
        local_nan_values_bool = np.isnan(local_val)
        local_old_length = len(local_val)
        local_val = local_val[~local_nan_values_bool]
        local_new_length = len(local_val)
        local_total_micro = local_total_micro[~local_nan_values_bool]
        local_minutes = local_minutes[~local_nan_values_bool]
        local_sec = local_sec[~local_nan_values_bool]
        local_point_id = local_point_id[~local_nan_values_bool]
        file_handle.write("\nFound this many NaN Values: " + str(local_old_length - local_new_length) + "\n")

    # deleting voltage spikes
    if any(local_val > 3000):
        file_handle.write('\nentering')
        local_outlier_values_bool = (local_val > 3000)
        local_old_length = len(local_val)
        local_val = local_val[~local_outlier_values_bool]
        local_new_length = len(local_val)
        local_total_micro = local_total_micro[~local_outlier_values_bool]
        local_minutes = local_minutes[~local_outlier_values_bool]
        local_sec = local_sec[~local_outlier_values_bool]
        local_point_id = local_point_id[~local_outlier_values_bool]
        file_handle.write("\nFound this many Voltage Spikes: " + str(local_old_length - local_new_length))

    return local_point_id, local_total_micro, local_minutes, local_sec, local_val


def adding_expected_markers(local_markers_x):
    # markers_x = np.add(markers_x, 5) only for manav
    markers_x_2 = np.divide(np.multiply(local_markers_x, 1000), 200)
    for i in range(len(local_markers_x)):
        axs[0].axvline(local_markers_x[i], color='r', zorder=100)
        axs[1].axvline(local_markers_x[i], color='r', zorder=100)
        axs[2].axvline(markers_x_2[i], color='r', zorder=100)


def data_processing(local_total_micro, local_val):
    # rectifying data
    local_rectified_1 = abs(local_val - sum(local_val) / len(local_val))

    # Binning the data
    local_total_milli = local_total_micro / 1000.0
    bin_size = 200
    num_of_bins1 = math.floor(local_total_milli[-1] / bin_size)
    local_rectified_1_bins = []
    curr_local_val = 0  # curr milli second point

    for i in range(num_of_bins1):
        curr_sum = 0
        counter = 0
        while local_total_milli[curr_local_val] < (i + 1) * bin_size:
            curr_sum += local_rectified_1[curr_local_val]
            counter += 1
            curr_local_val += 1
        if counter != 0:
            curr_average = curr_sum / counter
            local_rectified_1_bins.append(curr_average)
    local_rectified1_zscore = stats.zscore(local_rectified_1_bins)
    return local_rectified_1, local_rectified_1_bins, local_rectified1_zscore


def plotting_signal_time_domain(file_handle, local_axs, local_sec, local_val, local_rectified_1, local_rectified_1_bins, local_rectified1_zscore, local_markers_x):

    # plotting times for expected reaction
    adding_expected_markers(local_markers_x)

    # plotting raw data
    local_axs[0].plot(local_sec, local_val, zorder=1)

    # plotting rectified data
    local_axs[1].plot(local_sec, local_rectified_1, zorder=1)
    file_handle.write(str(len(local_rectified_1_bins)) +  " Total Bins Created")

    # plotting z-score data
    local_axs[2].plot(range(len(local_rectified_1_bins)), local_rectified1_zscore, zorder=1)

    # setting axis labels
    local_axs[0].set(ylabel="Raw Values (mV)", xlabel="Seconds", title="Raw EMG Recording")
    local_axs[1].set(ylabel="Rectified Values (mV)", xlabel="Seconds", title="Rectified EMG Recording")
    local_axs[2].set(ylabel="Z-Score", xlabel="Bin Number (Window Size: 200ms)", title="Facial Reactivity (Binned Z-Score) of Recording")


# FFT CODE: https://www.gaussianwaves.com/2020/01/how-to-plot-fft-in-python-fft-of-basic-signals-sine-and-cosine-waves/
def fft_graphing(local_axs, local_subplot_pos, local_val, local_rectified1_zscore, local_color):
    # now for fft
    fs = math.ceil(len(local_val) / 60)
    nfft = len(local_val)
    x2 = fftshift(fft(local_rectified1_zscore, nfft))
    f_vals = np.arange(start=-nfft / 2, stop=nfft / 2) * fs / nfft
    half_start = math.floor(len(f_vals) / 2)
    half_end = len(f_vals)
    local_axs[0].plot(f_vals[half_start:half_end], np.abs(x2[half_start:half_end]), color=local_color)
    local_axs[local_subplot_pos].plot(f_vals[half_start:half_end], np.abs(x2[half_start:half_end]), color=local_color)
    # this is for magnitude spectrum
    #local_axs[local_subplot_pos + 1].magnitude_spectrum(local_rectified1_zscore, color=local_color
    local_axs[0].set(ylabel="DFT Value", title="All Data")
    local_axs[1].set(ylabel="DFT Value", title="Unfiltered Data")
    local_axs[2].set(ylabel="DFT Value", xlabel="Frequency (Hz)", title="Filtered Data")


def notch_filter(file_handle, local_val):
    fs = math.ceil(len(local_val) / 60)
    file_handle.write('\nOur frequency is' + str(fs))
    w0 = 60
    q0 = 5
    b, a = signal.iirnotch(w0, q0, fs)
    filtered_data = signal.lfilter(b, a, local_val)
    return filtered_data


def averaging_zscore(file_handle, local_markers_x, local_rectified1_zscore, local_filtered_rectified1_zscore):
    start_sfr_bin = np.divide(np.multiply(local_markers_x, 1000), 200).astype(int)
    start_baseline_bin = np.divide(np.multiply(np.subtract(local_markers_x, 5), 1000), 200).astype(int)
    start_baseline_bin = np.append(start_baseline_bin, 300)
    print(start_sfr_bin)
    print(start_baseline_bin)
    baseline_zscore_averages = []
    sfr_zscore_averages = []
    for i in range(len(start_sfr_bin)):
        #print(i)
        #print(start_baseline_bin[i])
        #print(start_sfr_bin[i])
        #print(local_rectified1_zscore[start_baseline_bin[i]:start_sfr_bin[i]])
        baseline_zscore_averages.append(np.average(local_rectified1_zscore[start_baseline_bin[i]:start_sfr_bin[i]]))
        sfr_zscore_averages.append(np.average(local_rectified1_zscore[start_sfr_bin[i]:start_baseline_bin[i+1]]))
    file_handle.write("\nBaseline: " + str(baseline_zscore_averages))
    file_handle.write("\nSFR: " + str(sfr_zscore_averages))
    filtered_baseline_zscore_averages = []
    filtered_sfr_zscore_averages = []
    for i in range(len(start_sfr_bin)):
        #print(i)
        #print(start_baseline_bin[i])
        #print(start_sfr_bin[i])
        #print(local_rectified1_zscore[start_baseline_bin[i]:start_sfr_bin[i]])
        filtered_baseline_zscore_averages.append(np.average(local_filtered_rectified1_zscore[start_baseline_bin[i]:start_sfr_bin[i]]))
        filtered_sfr_zscore_averages.append(np.average(local_filtered_rectified1_zscore[start_sfr_bin[i]:start_baseline_bin[i+1]]))
    file_handle.write("\nFiltered Baseline: " + str(filtered_baseline_zscore_averages))
    file_handle.write("\nFiltered SFR: "+ str(filtered_sfr_zscore_averages))



def creating_output_file(file_name):
    file1 = open(file_name, "w")
    return file1


def closing_file(file_name):
    file_name.close()


if __name__ == '__main__':
    txt_file_name = 'Data/Pictures/Maureen\'s2 Data.txt'

    #to save z-score
    file_handle = creating_output_file(txt_file_name)

    # setting params for subplot graphing
    preset_params()
    # team_members - Andreea: 0, Malek: 1, Manav: 2, Maureen: 3
    # files to read
    person_reading_pos = 3
    folder_name = 'Data/'
    person_reading_name, files_read = selecting_files_read(file_handle, person_reading_pos)
    #files_read = ['CDP1_MM.csv']
    # adding expected times of reaction
    markers_x = [5, 17, 29, 41, 53]

    # working through all the files that are to be looked at
    for x in range(len(files_read)):
        # reading in the data & pre-processing
        file_handle.write("\n\n")
        file_handle.write(folder_name + files_read[x])
        point_id, total_micro, minutes, sec, val = reading_in_file(file_handle, folder_name + files_read[x])

        # plotting with pyplot
        fig, axs = plt.subplots(3)

        # processing the data & binning
        rectified_1, rectified_1_bins, rectified1_zscore = data_processing(total_micro, val)

        # plotting raw, rectified & z-score signal
        plotting_signal_time_domain(file_handle, axs, sec, val, rectified_1, rectified_1_bins, rectified1_zscore, markers_x)

        fig.savefig(folder_name + 'Pictures/' +  person_reading_name + '/' + files_read[x][0:len(files_read[x]) - 4])
        print('Saved fig: ', files_read[x])


        # now for fft
        #fig2, axs2 = plt.subplots(3)
        #suplot_plot_pos = 1
        #fft_graphing(axs2, suplot_plot_pos, val, rectified1_zscore, 'red')
        
        # apply notch filter (60Hz)
        filtered_val = notch_filter(file_handle, val)

        # processing filtered data
        filtered_rectified_1, filtered_rectified_1_bins, filtered_rectified1_zscore = data_processing(total_micro, filtered_val)
        # axs[1].plot(sec, filtered_val)
        
        # graphing fft
        suplot_plot_pos = 2
        #fft_graphing(axs2, suplot_plot_pos, filtered_val, filtered_rectified1_zscore, 'blue')
        averaging_zscore(file_handle, markers_x, rectified1_zscore, filtered_rectified1_zscore)


        #plt.show()
    closing_file(file_handle)
