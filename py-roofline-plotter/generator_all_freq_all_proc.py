#!/usr/bin/python
import math
import subprocess
import os
import time

sleep_delay = 0 #seconds

number_of_active_sockets_cmd = r'cat /proc/cpuinfo | grep "physical id" | sort | uniq | wc -l'
number_of_physical_cores_cmd = r'cat /proc/cpuinfo | egrep "core id|physical id" | tr -d "\n" | sed -e s/physical/\\n\nphysical/g | grep -v ^$ | sort | uniq | wc -l'
number_of_active_sockets = int(subprocess.Popen(number_of_active_sockets_cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=False).communicate()[0])
number_of_physical_cores_total = int(subprocess.Popen(number_of_physical_cores_cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=False).communicate()[0])

'''Method to get all the available CPU frequencies
'''
def get_available_cpu_freqs():
    #more /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies
#3066000 2933000 2667000 2400000 2133000 1867000 1600000 800000
    cpu_frequencies = []
    list = '3066000 2933000 '
    cpu_frequencies = [int(i) for i in list.split()]
    return cpu_frequencies

number_of_active_sockets =2
number_of_physical_cores_total = 24

number_of_physical_cores_per_socket = number_of_physical_cores_total/number_of_active_sockets

# IF HT is on, then num_logical_cores = 2 * num_phys_cores
HT = 1;
if HT == 1:
    number_of_logical_cores_total = 2 * number_of_physical_cores_total
else:
    number_of_logical_cores_total = number_of_physical_cores_total



counter = -1
bins = [] #size of bins = num_sockets * 2, since HT
temp = []

'Create the processor bins, each = num of phy procs per core'
'Loop through all logical cores'
for i in range(number_of_logical_cores_total):
    if int(math.fmod(i, number_of_physical_cores_per_socket)) == 0:
        counter += 1
        temp = []
        bins.append(temp)
    temp.append(i)

'Create the node composition as given by Cluster Studios cpuinfo'
node_composition = []
for i in range(0, len(bins)/2):
        node_composition.append(zip(bins[i], bins[i+2]))
        
    

#Enable all logical cores
def enable_all_logical_cores():
    for i in range(1, number_of_logical_cores_total):
        cmd = r'echo 1 > /sys/devices/system/cpu/cpu' + str(i) + '/online'
        try:
            subprocess.check_call(cmd, shell=True, stdout=open(os.devnull, 'wb')) # , stderr=subprocess.PIPE
        except subprocess.CalledProcessError as e:
            print 'Execution error on command:', e.cmd 
            

'''
Disable physical cores
To disable the right physical cores, we consult the node composition
'''
def disable_cores(number_of_physical_cores_to_disable):
    #Merge the list
    out =[]
    logical_proc_pairs =''
    for i in range(0, len(node_composition)):
        out += node_composition[i]
    print_command = 'Disabling ' + str(number_of_physical_cores_to_disable) + ' cores [' 
    for i in range(number_of_physical_cores_total-number_of_physical_cores_to_disable,number_of_physical_cores_total):
        for j in [0,1]:
            cmd = r'echo 0 > /sys/devices/system/cpu/cpu' + str(out[i][j]) + '/online'
#             print cmd
#             try:
#                 subprocess.check_call(cmd, shell=True, stdout=open(os.devnull, 'wb')) # , stderr=subprocess.PIPE
            
#             except subprocess.CalledProcessError as e:
#                 print 'Execution error on command:', e.cmd 
        logical_proc_pairs += str(out[i]) + ','
    print_command += logical_proc_pairs
    print print_command[:-1]+']'
         
    


'''
Disable a whole socket. You cannot disable socket Id 0 because core0 is always active.
Loop through all the cores on socket_id and disable them
'''
def disable_socket(socket_id):
    None #TODO



#Loop through all CPU frequencies and execute a benchmark software 
#For each CPU freq, loop through all cores
cpu_frequencies = get_available_cpu_freqs()
for i in range(1,number_of_physical_cores_total): #First physical core is always on
#     print i
    disable_cores(i)
    time.sleep(sleep_delay) # Stabilize the system
    for j in range(0, len(cpu_frequencies)):
        cmd = r'cpupower frequency-set -f '+ str(cpu_frequencies[j])
#         subprocess.check_call(cmd, shell=True, stdout=open(os.devnull, 'wb')) 
        time.sleep(sleep_delay) # Stabilize the system
        print 'Executing nodeperf @freq=' + str(cpu_frequencies[j]) + ' with ' + str(number_of_physical_cores_total-i) + ' cores active'
        execute_benchmark_cmd = r'sleep 2'
        subprocess.check_call(execute_benchmark_cmd, shell=True, stdout=open(os.devnull, 'wb')) 



