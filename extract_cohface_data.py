import h5py

# Replace 'your_file.hdf5' with the actual filename
hdf5_file = 'data.hdf5'

datasets_names = ['pulse','respiration','time']
values = [[],[],[]]

with h5py.File(hdf5_file, 'r') as file:
    for i in range(len(datasets_names)):
        dataset = file[datasets_names[i]]  
        values[i].append(dataset[:])

pulse,respiration,time=values[0],values[1],values[2]

