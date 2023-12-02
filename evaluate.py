import sys
#sys.path.append('../cohface/cohface')

sys.path.append('./cohface')
import cf_hr
import em_hr

import openpyxl
import os

def eval_data(data_path):
    #data_path should be equal to the path of the folder containing data.avi and data.hdf5
    
    ground_truth_hr = cf_hr.get_heart_rate(data_path+'.hdf5')
    eulerian_magnification_hr = em_hr.get_heart_rate(data_path+'.avi')
    
    return ground_truth_hr,eulerian_magnification_hr

def find_next_filename(base_filename):
    i = 1
    while os.path.exists(f"{base_filename}{i}.xlsx"):
        i += 1
    return f"{base_filename}{i}.xlsx"

def write_excel_file(array0,array1,array2,array3):
    # Create a new Excel workbook and select the active sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    sheet.cell(row=1, column=1, value="sample")
    for index, value in enumerate(array0, start=1):
        sheet.cell(row=index+1, column=1, value=value)

    sheet.cell(row=1, column=2, value="ground_truth")
    for index, value in enumerate(array1, start=1):
        sheet.cell(row=index+1, column=2, value=value)

    sheet.cell(row=1, column=3, value="estimation")
    for index, value in enumerate(array2, start=1):
        sheet.cell(row=index+1, column=3, value=value)
    
    sheet.cell(row=1, column=4, value="difference")
    for index, value in enumerate(array3, start=1):
        sheet.cell(row=index+1, column=4, value=value)

    # Save the workbook to a file
    workbook.save(find_next_filename("output"))

db_path = '../cohface/cohface/'

values = [[],[],[],[]]

with open(db_path+'protocols/all/all.txt', 'r') as file:
    # Iterate over each line in the file
    for line in file:
        
        # Process each line as needed
        file_path = db_path+line.strip()
        try:
            gt,est=eval_data(file_path)
            diff=gt-est
        except Exception as e:
            print(f"Error with sample: {file_path}\nError: {str(e)}")
            values[0].append(file_path)
            values[1].append("Error")
            values[2].append("Error")
            values[3].append("Error")
        else:
            print(gt,est,diff)
            values[0].append(file_path)
            values[1].append(gt)
            values[2].append(est)
            values[3].append(diff)
    
    write_excel_file(values[0],values[1],values[2],values[3])
