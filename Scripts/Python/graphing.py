import numpy as np
from scipy import stats, signal
import math
import matplotlib.pyplot as plt
#import matplotlib.figure.SubplotParams

# reading in the data
#OK- in context.csv
#"Maureen_Participant 1_Part 1.csv"
id, total_micro, min, sec, val = np.loadtxt("CDP1_MM.csv",
                        skiprows=1, unpack=True, delimiter=",")
id2, total_micro2, min2, sec2, val2 = np.loadtxt("sfr1_MM.csv",
                        skiprows=1, unpack=True, delimiter=",")
sampling_rate = id[-1]/(min[-1]*60.0)
#plotting with pyplot
#data = hp.get_data('e0103.csv')
#TODO - Debug Data With Missing Graphs
#TODO - Preset Workspace Variabls
#TODO - Save all pictures for data
#plt.figure(figsize=(12,4))
#plt.plot(val)
#plt.show()
fig, axs = plt.subplots(3)
#plotting raw data
axs[0].plot(sec, val)
max_y = max(val)
markers_x = [5,17,29,41,53]

for i in range(len(markers_x)):
    axs[0].axvline(markers_x[i],color='r')
#print(rcParams.keys)
#plt.figure.SubplotParams(left=None, bottom=None, right=None, top=None, wspace=None, hspace=.67)
#params['fig.hspace'] = .67


#axs[0].plot([0,100,2000],[0,0,0])
#axs[1].plot(sec2, val2)
#plotting rectified data
rectified_1 = abs(val - sum(val)/len(val))
rectified_2 = abs(val2 - sum(val2)/len(val2))
fs = math.ceil(len(val)/60)
print(fs)
w0 = 60
Q0 = 30
b, a = signal.iirnotch(w0, Q0, fs)
print(b)
print(a)
#print("filter1", np.all(np.abs(np.roots(a))<1))
#wav = signal.filtfilt(b, a, val)
#print(wav)

#axs[1].plot(sec, wav)
#axs[1].plot(sec2, rectified_2)
total_milli = total_micro/1000.0
total_milli2 = total_micro2/1000.0

#print(*total_milli, sep = "\n")

num_of_bins1 = math.floor(total_milli[-1]/200)
num_of_bins2 = math.floor(total_milli2[-1]/200)
print("Bin Size", num_of_bins1)
rectified_1_bins = []
curr_val = 0
#print(num_of_bins1)
for i in range(num_of_bins1 - 1):
    #print(i)
    curr_sum = 0
    counter = 0
    print("WHile Condition Left", total_milli[curr_val])
    print("WHile Condition Right", (i + 1) * 200)
    while (total_milli[curr_val] < (i + 1) * 200):
        curr_sum += rectified_1[curr_val]
        counter += 1
        curr_val += 1
        #print(counter)
        #print(curr_sum)
    #print(i)
    print("i", i)
    print("Curr Sum", curr_sum)
    print("Curr Val in Time", total_milli[curr_val])
    curr_average = curr_sum / counter
    rectified_1_bins.append(curr_average)
    #print(curr_average)
#axs[1].plot(range(300), rectified_1_bins)
rectified1_zscore = stats.zscore(rectified_1_bins)
#print(*rectified1_zscore, sep = "\n")
axs[0].set(ylabel ="Raw Values (mV)", xlabel = "Seconds", title = "Raw EMG Recording")
axs[1].set(ylabel ="Rectified Values (mV)", xlabel = "Seconds", title = "Rectified EMG Recording")
axs[2].set(ylabel ="Z-Score Value", xlabel = "Bin Number (Window Size: 200ms)", title = "Facial Reactivity (Binned Z-Score) of Recording")
#plt.xlabel("Maureen First - Raw rectified & Second - Bin 200ms & Third - Bin-100ms")
axs[2].plot(range(num_of_bins1-1), rectified1_zscore)

#axs.legend()



#to bargraph the mean zscores
"""
print(len(rectified1_zscore))
base = []
happy = []
curr_bin = 0
for i in range(5):
    print("working on", i)
    curr_bin_end = curr_bin + 24
    print(curr_bin, "Base",i)
    print(curr_bin_end ,"Base",i)
    base_curr = sum(rectified1_zscore[curr_bin: curr_bin_end])/len(rectified1_zscore[curr_bin: curr_bin_end])
    base.append(base_curr)
    curr_bin = curr_bin + 24
    curr_bin_end = curr_bin + 35
    print(curr_bin,"Happy",i)
    print(curr_bin_end,"Happy",i)
    happy_curr = sum(rectified1_zscore[curr_bin: curr_bin_end]) / len(rectified1_zscore[curr_bin: curr_bin_end])
    happy.append(happy_curr)
    curr_bin = curr_bin + 35
print(*base, sep = "\n")
print("Now Happy")
print(*happy, sep = "\n")

#fig = plt.figure()
#ax = fig.add_axes([0,0,1,1])
#ax.bar("Baseline", base, color = 'b', width = 0.25)
#ax.bar("Happy", happy, color = 'g', width = 0.25)
#ax.bar(X + 0.50, data[2], color = 'r', width = 0.25)
"""
plt.show()
"""
BIN 100ms
num_of_bins1 = math.ceil(total_milli[-1]/100)
rectified_1_bins = []
curr_val = 0
print(num_of_bins1)
for i in range(num_of_bins1 - 1):
    #print(i)
    curr_sum = 0
    counter = 0
    while (total_milli[curr_val] < (i + 1) * 100):
        curr_sum += rectified_1[curr_val]
        counter += 1
        curr_val += 1
        #print(counter)
        #print(curr_sum)
    curr_average = curr_sum / counter
    rectified_1_bins.append(curr_average)
axs[2].plot(range(num_of_bins1-1), rectified_1_bins)
"""

#axs[3].ylabel("Mean Rectified Binned Value")
#axs[3].xlabel("Bin Number")
#axs[2].set(ylabel ="Mean Rectified Binned Value", xlabel = "Bin Number")



"""
bin it
    1) Split data into 200ms 
    2) average the data in those chunks 
    3) graphing bar graphs of the muscle activation for the second ranges 
TODO: Decide window frame 200ms

#z-score
"""
"""
plt.plot(id, sec)
plt.xlabel("Sample #")
plt.ylabel("Volt recorded")
plt.legend()
plt.gcf().autofmt_xdate()
plt.show()
"""


"""
Base1: 0 - 5 (24)
VHappy1: 5 (24) -12 (59) 
Base2: 5-17
VHappy2: 17- 24
Base3: 24 - 29
VHappy3: 29 - 36
Base4: 36 - 41
VHappy4: 41 - 48
Base5: 48 - 53
Vhappy5: 53- 60
"""
#print("starting rr calcs")
#wd, m = hp.process(val, sampling_rate)

#visualise in plot of custom size
#plt.figure(figsize=(12,4))
#hp.plotter(wd, m)

#display computed measures
#for measure in m.keys():
#    print('%s: %f' %(measure, m[measure]))