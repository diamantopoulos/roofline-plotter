import numpy
from pylab import *

import utilities
from itertools import islice
import csv 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import matplotlib.font_manager as fm


time_format = '%H:%M:%S.%f'

''' Return index in the CSV header file for Socket[index]
'''
def get_socket_index(reader):
    header = reader.next()
    for index, col_val in enumerate(header):
        if col_val == 'Socket0':
            socket0_index = index
        if col_val == 'Socket1':
            socket1_index = index
    return socket0_index, socket1_index #In Spreadsheet, we count from 1, in python from 0
    

''' Return index in the CSV header file for System
'''
def get_system_index(reader):
    header = reader.next()
    for index, col_val in enumerate(header):
        if col_val == 'System':
            return index #In Spreadsheet, we count from 1, in python from 0
        
''' Return index in the CSV header file for Proc Energy (Joules)
'''
def get_proc_energy_index(reader):
    header = reader.next()
    for index, col_val in enumerate(header):
        if col_val == 'Proc Energy (Joules)':
            return index #In Spreadsheet, we count from 1, in python from 0


def get_roofline_points_socket0():
    op_intensity = []
    inst_per_cycle = []
    with open('all.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        socket0_index, socket1_index = get_socket_index(reader)
        csvfile.seek(0) #reset iterator to top of file
        for row in islice(reader, 2, None):
            inst_per_cycle.append(float(row[3]))
            read_write_from_MC = float(row[socket0_index+10]) + float(row[socket0_index+11])
            op_intensity.append(float(row[14]) / read_write_from_MC)
        return op_intensity, inst_per_cycle
    
def get_roofline_points_socket1():
    op_intensity = []
    inst_per_cycle = []
    with open('all.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        socket0_index, socket1_index = get_socket_index(reader)
        csvfile.seek(0) #reset iterator to top of file
        for row in islice(reader, 2, None):
            inst_per_cycle.append(float(row[3]))
            read_write_from_MC = float(row[socket1_index+10]) + float(row[socket1_index+11])
            op_intensity.append(float(row[14]) / read_write_from_MC)
        return op_intensity, inst_per_cycle
        
   

""" Master function that opens the CSV file generated from PCM and returns arrays of information that are used to plot the graphs
    Arrays returned:
    time
    inst_per_cycle
    op_intensity
"""
def get_roofline_data_system(csv_filename):
    time = []
    inst_per_cycle = []
    op_intensity = []
    energy_SKT0 = []
    energy_SKT1 = []
    with open(csv_filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        header = reader.next()
        header = reader.next()
        for index, col_val in enumerate(header):
            if col_val == 'Time':
                time_index = index
                
        csvfile.seek(0) #reset iterator to top of file
        system_index = get_system_index(reader)
        csvfile.seek(0) #reset iterator to top of file
        proc_energy_index = get_proc_energy_index(reader)
        for row in islice(reader, 2, None):
            time.append(row[time_index]) #1
            inst_per_cycle.append(float(row[3]))
            read_write_from_MC = float(row[system_index+12]) +float(row[system_index+13])
            op_intensity.append(float(row[14]) / read_write_from_MC)
            energy_SKT0.append(float(row[proc_energy_index]))
            energy_SKT1.append(float(row[proc_energy_index+1]))
            
        return time, inst_per_cycle, op_intensity, energy_SKT0, energy_SKT1 


'''
Read_csv returns all the data necessary per CSV to plot RL, Energy vs core @ all freq etc.
'''
def read_csv(csv_filename):
    time = []
    inst_per_cycle = []
    time_stamp = []
    energy = []
    energy_incremental = []
    inst_per_cycle = []
    instr_intensity = []
    energy_SKT0 = []
    energy_SKT1 = []
    
    energy_inc = 0
    with open(csv_filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        
        header = reader.next() #First header
        for index, col_val in enumerate(header):
            if col_val == 'System Pack C-States':
                sys_pack_C_state = index
            
        header = reader.next() # second header
        for index, col_val in enumerate(header):
            if col_val == 'Time':
                time_index = index
                
        csvfile.seek(0) #reset iterator to top of file
        system_index = get_system_index(reader)
        csvfile.seek(0) #reset iterator to top of file
        proc_energy_index = get_proc_energy_index(reader)
        for row in islice(reader, 2, None):
            inst_per_cycle.append(float(row[3]))
            time.append(row[time_index]) #1
            energy.append(row[sys_pack_C_state+4]) #Proc Energy (Joules)
            
            #Get Instruction intensity
            read_write_from_MC = float(row[system_index+12]) +float(row[system_index+13])
            instr_intensity.append(float(row[14]) / read_write_from_MC)
            
            
            #Get Energy at SKT level
            energy_SKT0.append(float(row[proc_energy_index]))
            energy_SKT1.append(float(row[proc_energy_index+1]))
            
            #Get incremental Energy
            energy_inc += float(row[sys_pack_C_state+4]) 
            energy_incremental.append(energy_inc)

        
        #Get incremental time
        #time_stamp.append(0)
        initial_date_time = datetime.strptime(time[0], time_format)
        initial_time = initial_date_time.strftime(time_format)

        for i in range(len(time)):
            date_time = datetime.strptime(time[i], time_format)
            time_string = date_time.strftime(time_format)
            diff = date_time - initial_date_time
            time_stamp.append(diff.total_seconds())
            
        return time, time_stamp, inst_per_cycle, instr_intensity, energy, energy_incremental, energy_SKT0, energy_SKT1


