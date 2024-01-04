import sys
#sys.path.append('../cohface/cohface')

sys.path.append('./cohface')
import cf_hr
import em_hr

import openpyxl
import os

import inject_hr

gtdatapath = ''

def eval_data(data_path):
    #data_path should be equal to the path of the folder containing data.avi and data.hdf5
    
    ground_truth_hr = cf_hr.get_heart_rate(gtdatapath)
    eulerian_magnification_hr = em_hr.get_heart_rate(data_path+'.avi')
    
    return ground_truth_hr,eulerian_magnification_hr

db_path = '../cohface/cohface/'

values = [[],[],[],[]]

target_hr = 65

with open(db_path+'protocols/all/4h.txt', 'r') as file:
    # Iterate over each line in the file
    for line in file:
        
        # Process each line as needed
        file_path = db_path+line.strip()
        try:
            if file_path[-1:] == "a":
                gtdatapath=file_path+'.hdf5'
            
            #create injected video
            inject_hr.inject_heart_rate(file_path+'.avi', file_path+'_hacked.avi', target_hr)
            
            print("gtdatapath",gtdatapath,'|'+file_path[-1:]+'|')
            #gt,est=eval_data(file_path)
            #TODO remove when done skipping original videos
            gt,est=123,456
            gth,esth=eval_data(file_path+'_hacked')
            gth=target_hr
            diff=gt-est
        except Exception as e:
            print(f"Error with sample: {file_path}\nError: {str(e)}")
            values[0].append(file_path)
            values[1].append("Error")
            values[2].append("Error")
            values[3].append("Error")
        else:
            print(gt,est,esth)
            values[0].append(file_path)
            values[1].append(gt)
            values[2].append(est)
            values[3].append(diff)

