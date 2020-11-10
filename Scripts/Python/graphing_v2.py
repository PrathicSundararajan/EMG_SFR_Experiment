# Done - Debug Data With Missing Graphs
# Done - Preset Workspace Variables
# Done - remove first outlier data point
# Done - Save all pictures for data
# Done - Shift Manav's data left by 5 seconds (scrap out first 5 seconds)
# Done - apply filter
# TODO - Confirm noise is being removed
# TODO - Maybe consider building bar graph on python?

import numpy as np
import statistics
from scipy import stats, signal, fft, ifft
from scipy.fftpack import fftshift
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
#from scipy import



def preset_params():
    mpl.rcParams['figure.subplot.wspace'] = .2
    mpl.rcParams['figure.subplot.hspace'] = .70
    mpl.rcParams['figure.subplot.left'] = .11
    mpl.rcParams['figure.subplot.bottom'] = .10
    mpl.rcParams['figure.subplot.right'] = .98
    mpl.rcParams['figure.subplot.top'] = .94
    mpl.rcParams['axes.titlesize'] = 'small'
    mpl.rcParams['axes.labelsize'] = 'small'


def selecting_files_read(team_member_pos):
    team_members = ['Andreea', 'Malek', 'Manav', 'Maureen']
    maureen_files = ['Maureen_Participant 1_Part 1.csv', 'Maureen_Participant 1_Part 2.csv', 'Maureen_Participant 2_Part 1.csv', 'Maureen_Participant 2_Part 2.csv']
    manav_files = ['Participant1_out.csv', 'Participant1_In.csv', 'Participant2_in.csv', 'Participant2_out.csv', 'Participant3_in.csv', 'Participant3_out.csv', 'Participant4_in.csv', 'Participant4_out.csv']
    andreea_files =['AR- in context.csv', 'AR- out of context.csv', 'JR- in context.csv', 'JR-out of context.csv', 'OK- in context.csv', 'OK- out of context.csv', 'VS in context.csv', 'VS out of context.csv']
    malek_files = ['CDP1_MM.csv', 'CDP2_MM.csv', 'DW1_MM.csv', 'DW2_MM.csv']
    local_person_reading_name = team_members[person_reading_pos]
    local_files_read = []
    if person_reading_pos == 0:
        local_files_read = andreea_files
        print('Saving Andreea\'s files')
    elif person_reading_pos == 1:
        local_files_read = malek_files
        print('Saving Malek\'s files')
    elif person_reading_pos == 2:
        local_files_read = manav_files
        print('Saving Manav\'s files')
    elif person_reading_pos == 3:
        local_files_read = malek_files
        print('Saving Malek\'s files')
    else:
        print("Not reading in any data")
    return local_person_reading_name, local_files_read


def reading_in_file(file_path):
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
        print("Found this many NaN Values: ", local_old_length - local_new_length)

    # deleting voltage spikes
    if any(local_val > 3000):
        print('entering')
        local_outlier_values_bool = (local_val > 3000)
        local_old_length = len(local_val)
        local_val = local_val[~local_outlier_values_bool]
        local_new_length = len(local_val)
        local_total_micro = local_total_micro[~local_outlier_values_bool]
        local_minutes = local_minutes[~local_outlier_values_bool]
        local_sec = local_sec[~local_outlier_values_bool]
        local_point_id = local_point_id[~local_outlier_values_bool]
        print("Found this many Voltage Spikes: ", local_old_length - local_new_length)

    return local_point_id, local_total_micro, local_minutes, local_sec, local_val

def adding_expected_markers():
    # plotting times for expected reaction
    markers_x = [5, 17, 29, 41, 53]
    # markers_x = np.add(markers_x, 5) only for manav
    markers_x_2 = np.divide(np.multiply(markers_x, 1000), 200)
    for i in range(len(markers_x)):
        axs[0].axvline(markers_x[i], color='r', zorder=100)
        axs[1].axvline(markers_x[i], color='r', zorder=100)
        axs[2].axvline(markers_x_2[i], color='r', zorder=100)

def data_processing(local_total_micro, local_val):
    # rectifying data
    local_rectified_1 = abs(local_val - sum(local_val) / len(local_val))

    # Binning the data
    local_total_milli = local_total_micro / 1000.0
    BIN_SIZE = 200
    num_of_bins1 = math.floor(local_total_milli[-1] / BIN_SIZE)
    local_rectified_1_bins = []
    curr_local_val = 0  # curr milli second point

    for i in range(num_of_bins1):
        curr_sum = 0
        counter = 0
        while local_total_milli[curr_local_val] < (i + 1) * BIN_SIZE:
            curr_sum += local_rectified_1[curr_local_val]
            counter += 1
            curr_local_val += 1
        if counter != 0:
            curr_average = curr_sum / counter
            local_rectified_1_bins.append(curr_average)
    local_rectified1_zscore = stats.zscore(local_rectified_1_bins)
    return local_rectified_1, local_rectified_1_bins, local_rectified1_zscore


def plotting_signal_time_domain(sec, local_val, local_rectified_1, local_rectified_1_bins, local_rectified1_zscore):
    # adding expected times of reaction
    adding_expected_markers()

    # plotting raw data
    axs[0].plot(sec, local_val, zorder=1)

    # plotting rectified data
    axs[1].plot(sec, local_rectified_1, zorder=1)
    print(len(local_rectified_1_bins), "Total Bins Created")

    # plotting z-score data
    axs[2].plot(range(len(local_rectified_1_bins)), local_rectified1_zscore, zorder=1)

    # setting axis labels
    axs[0].set(ylabel="Raw (mV)", xlabel="Seconds", title="Raw EMG Recording")
    axs[1].set(ylabel="Rectified (mV)", xlabel="Seconds", title="Rectified EMG Recording")
    axs[2].set(ylabel="Z-Score", xlabel="Bin Number (Window Size: 200ms)", title="Facial Reactivity (Binned Z-Score) of Recording")

# def fft_graphing():

if __name__ == '__main__':
    # setting params for subplot graphing
    preset_params()

    # files to read
    person_reading_pos = 3
    folder_name = 'Data/'
    person_reading_name, files_read = selecting_files_read(person_reading_pos)
    files_read = ['CDP1_MM.csv']



    for x in range(len(files_read)):
        # reading in the data & pre-processing
        print(folder_name + files_read[x])
        point_id, total_micro, minutes, sec, val = reading_in_file(folder_name + files_read[x])
        # plotting with pyplot
        fig, axs = plt.subplots(3)

        # processing the data & binning
        rectified_1, rectified_1_bins, rectified1_zscore = data_processing(total_micro, val)

        # plotting raw, rectified & z-score signal
        plotting_signal_time_domain(sec, val, rectified_1, rectified_1_bins, rectified1_zscore)

        # fig.savefig(folder_name + 'Pictures/' +  person_reading_name + '/' + files_read[x][0:len(files_read[x]) - 4])
        # print('Saved fig: ', files_read[x])

        #plt.figure()  # now for fft
        fig2, axs2 = plt.subplots(1)

        # sample spacing
        # FFT CODE: https://www.gaussianwaves.com/2020/01/how-to-plot-fft-in-python-fft-of-basic-signals-sine-and-cosine-waves/
        fs = math.ceil(len(val) / 60)
        NFFT = len(val)
        yf = fft(rectified1_zscore)
        X = fftshift(fft(rectified1_zscore, NFFT))
        fVals = np.arange(start=-NFFT / 2, stop=NFFT / 2) * fs / NFFT
        half_start = math.floor(len(fVals)/2)
        half_end = len(fVals)
        axs2.plot(fVals[half_start:half_end], np.abs(X[half_start:half_end]))



        # apply notch filter (60Hz)

        fs = math.ceil(len(val) / 60)
        print('Our frequency is', fs)
        #print(fs)
        w0 = 60
        Q0 = 5
        b, a = signal.iirnotch(w0, Q0, fs)
        #print(b)
        #print(a)
        filtered_data = signal.lfilter(b, a, val)
        #print(filtered_data)
        rectified_1 = filtered_data
        total_milli = total_micro / 1000.0
        BIN_SIZE = 200
        num_of_bins1 = math.floor(total_milli[-1] / BIN_SIZE)
        rectified_1_bins = []
        curr_val = 0  # curr milli second point

        for i in range(num_of_bins1):
            curr_sum = 0
            counter = 0
            while total_milli[curr_val] < (i + 1) * BIN_SIZE:
                curr_sum += rectified_1[curr_val]
                counter += 1
                curr_val += 1
            if counter != 0:
                curr_average = curr_sum / counter
                rectified_1_bins.append(curr_average)
        rectified1_zscore = stats.zscore(rectified_1_bins)
        N = len(val)
        # sample spacing

        fs = math.ceil(len(val) / 60)
        T = 1.0 / 800.0
        NFFT = len(val)
        # X = fft(x, N)  # compute X[k]
        # x = ifft(X, N)  # compute x[n]
        yf = fft(rectified1_zscore)
        X = fftshift(fft(rectified1_zscore, NFFT))
        fVals = np.arange(start=-NFFT / 2, stop=NFFT / 2) * fs / NFFT
        # freq = np.divide(np.fft.fftfreq(N),60)
        # ft = np.fft.fft(rectified1_zscore)
        # NFFT = len(val)
        # fVals = np.arange(start=-NFFT / 2, stop=NFFT / 2) * fs / NFFT
        # print(len(freq))
        # axs2[0].plot(fVals, np.divide(2.0, np.multiply(N, np.abs(yf[0:N // 2]))))
        axs2.plot(fVals, np.abs(X), color = 'red')

        plt.show()

