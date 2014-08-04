from itertools import islice
import csv 

''' Return index in the CSV header file for Socket[index]
'''
def get_socket_index(reader):
    header = reader.next()
    for index, col_val in enumerate(header):
        if col_val == 'Socket0':
            return index #In Spreadsheet, we count from 1, in python from 0
    #sub_header = reader.next()
    #print sub_header
    

def get_socket_sub_index(reader):
    return 1


''' Return index in the CSV header file for System
'''
def get_system_index(reader):
    header = reader.next()
    for index, col_val in enumerate(header):
        if col_val == 'System':
            return index #In Spreadsheet, we count from 1, in python from 0


with open('e.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    system_index = get_system_index(reader)
    csvfile.seek(0) #reset iterator to top of file
    for row in islice(reader, 2, None):
        IPC = row[3]
        read_write_from_MC = float(row[system_index+12]) +float(row[system_index+13])
        op_intensity = float(row[14]) / read_write_from_MC
        print IPC, '+' , op_intensity 