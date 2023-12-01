import h5py
import numpy as np
from scipy.signal import find_peaks

def real_heartrate(hdf5_file):
    #hdf5_file = 'data.hdf5'

    datasets_names = ['pulse','time']
    values = []

    with h5py.File(hdf5_file, 'r') as file:
        for i in range(len(datasets_names)):
            dataset = file[datasets_names[i]]  
            values.append(np.array(dataset))

    pulse,time=values[0],values[1]

    sensor_freq = 256
    peaks, _ = find_peaks(pulse, distance=sensor_freq/2)
    heart_rate = len(peaks) / (time[-1] - time[0]) * 60

    return heart_rate