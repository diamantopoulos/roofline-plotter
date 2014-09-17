import numpy as np
import math
from pylab import *
import read_csv
import utilities 
from scipy import interpolate

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.font_manager import FontProperties


import matplotlib.dates as mdates
from datetime import datetime
import matplotlib.cm as cm
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

# font = fm.FontProperties(family = 'sans-serif', fname = 'default.ttc')

num_physical_cores_total = 2
#Xeon PC CPU details
cpu_frequencies = [2701000, 2700000, 2500000, 2400000, 2300000, 2200000, 2100000, 2000000, 1900000, 1800000, 1700000, 1600000, 1500000, 1400000, 1300000, 1200000]

for i in range(len(cpu_frequencies)):
    cpu_frequencies[i] = float(float(cpu_frequencies[i])/float(1000000))

#Font properties
font_family = ['serif', 'sans-serif', 'monospace']
font_style  = ['normal', 'italic', 'oblique']
font = FontProperties()
font.set_family(font_family[1])

colors = cm.rainbow(np.linspace(0, 1, len(cpu_frequencies)))

def addPerfLine(peakPerf, label, axis, balance_point, graph_lims):
    #Peak performance line and text
    ax.axhline(y=peakPerf, xmin=balance_point/graph_lims[1], xmax=1, linewidth=1.75, color='black')
    #ax.text(X_MAX/10.0, PEAK_PERF+(PEAK_PERF)/10, "Peak Performance ("+str(PEAK_PERF)+" F/C)", fontsize=8)
    label_string = label+" ("+str(peakPerf)+" Instr/Cycle)"
    yCoordinateTransformed = (log(peakPerf)-log(graph_lims[2]))/(log(graph_lims[3]/graph_lims[2]))
    axis.text(1 - len(label_string) / 100. - 0.01, peakPerf + 0.04 , label_string, fontproperties = font, fontsize=10, weight='light')
    

def addBWLine(BW, label, graph_lims):
    x = np.linspace(graph_lims[0], graph_lims[1], 10)
    y = x*BW
    ax.plot(x, y, linewidth=0.75, color='black')
    yCoordinateTransformed = (log(graph_lims[0]*BW)-log(graph_lims[2]))/(log(graph_lims[3]/graph_lims[2]))+0.16 #0.16 is the offset of the lower axis
    #ax.text(X_MIN*1.1,(X_MIN*1.1*BW)*1.1, '            '+label+' ('+str(BW)+' Bytes/Cycle)',fontsize=8, rotation=np.arctan(INVERSE_GOLDEN_RATIO * 0.8) * 180 / np.pi, verticalalignment = 'bottom')
    # ax.text(0.01,yCoordinateTransformed+0.05+0.0075*(len(str(BW))-1), label+' ('+str(BW)+' B/C)',fontsize=8, rotation=45, transform=ax.transAxes)
  

def plot_Energy_vs_cores_all_freq():
    
    #Loop all freqs for each number of active cores
    for i, cpu_freq in enumerate(cpu_frequencies):
        energy_inc = []
        for j in range(1, num_physical_cores_total):
            var = 'line' + str(i)
            csv_path = 'freq_proc_csv/nodeperf_' + str(cpu_freq) + 'Ghz_' + str(num_physical_cores_total-j) + 'act_cores.csv' 
            time, time_stamp, inst_per_cycle, instr_intensity, energy, energy_incremental, energy_SKT0, energy_SKT1 = read_csv.read_csv(csv_path)
            
            #Plot total_energy vs cores, for all frequencies
            var, = ax2.plot(i, energy_incremental[-1], '*', color = colors[i] , markersize=10, label= str(cpu_freq) + ' Ghz')
            energy_inc.append(energy_incremental[-1])
    
        #Plot spline Energy vs cores
        x = range(1,num_physical_cores_total)
        tck = interpolate.splrep(x, energy_inc, s=0)
        xnew = np.arange(1,num_physical_cores_total,np.pi/150)
        ynew = interpolate.splev(xnew, tck, der=0)
        ax2.plot(xnew, ynew)
    
    #Add legends
    legends = []
    legends.append(ax2.legend(loc=2, shadow=True, numpoints=1, bbox_to_anchor=(1.01, 1.0)))
    
    for legend in legends:
        #The frame is matplotlib.patches.Rectangle instance surrounding the legend.
        frame = legend.get_frame()
        frame.set_facecolor('0.90')
        # Set the fontsize
        for label in legend.get_texts():
            label.set_fontsize('8')
             
        for label in legend.get_lines():
            label.set_linewidth(1)  # the legend line width   
            


'''
Plot a Roofline model for all the frequencies at a given number of active cores
'''
def plot_RL_all_freq(num_active_cores): 
    #Set graph properties
    ax.set_title('Roofline for ' + str(num_active_cores) + ' active cores',fontsize=14,fontweight='bold')
    
    #Set the axes properties
    ax.set_yscale('log', basey=2)
    ax.set_xscale('log', basex=2)
    X_MIN=0.01
    X_MAX=900
    Y_MIN=0.1
    Y_MAX=8
    graph_lims = [X_MIN,X_MAX,Y_MIN,Y_MAX]
    ax.axis([X_MIN,X_MAX,Y_MIN,Y_MAX])
    
    #Get balance points for each frequency and add compute-bound RL
    PEAK_PERF=[4.0]
    PEAK_PERF_LABELS=['Scalar Peak Performance']
    PEAK_BW_LABELS = ['Bandwidth']
    
    balance_points = []
    for i, cpu_freq in enumerate(cpu_frequencies):
        balance_points.append(20/(cpu_freq*num_active_cores)) #70GBps = Mem_BW
        for p,l in zip(PEAK_PERF, PEAK_PERF_LABELS):
            addPerfLine(p,l, ax, float(balance_points[i]), graph_lims)
        for bw,l in zip([balance_points[i]], PEAK_BW_LABELS):
            addBWLine(bw,l, graph_lims)
    
    
    #Loop all freqs for each number of active cores
    for i, cpu_freq in enumerate(cpu_frequencies):
        var = 'line' + str(i)
        csv_path = 'freq_proc_csv/nodeperf_' + str(cpu_freq) + 'Ghz_' + str(num_active_cores) + 'act_cores.csv' 
        time, time_stamp, inst_per_cycle, instr_intensity, energy, energy_incremental, energy_SKT0, energy_SKT1 = read_csv.read_csv(csv_path)
        var, = ax.plot(instr_intensity, inst_per_cycle, '.', color = colors[i], markersize=0.8, label= str(cpu_freq) + 'Ghz')
       
    #Add legends
    legend = ax.legend(loc=2, shadow=True, numpoints=10, bbox_to_anchor=(1.01, 1.0))
    
    #The frame is matplotlib.patches.Rectangle instance surrounding the legend.
    frame = legend.get_frame()
    frame.set_facecolor('0.90')
    
    # Set the fontsize
    for label in legend.get_texts():
        label.set_fontsize('8')
    
    for label in legend.get_lines():
        label.set_linewidth(1)  # the legend line width
    

#fig = Roofline graph
fig = plt.figure(num=None, figsize=(14, 7), dpi=80, facecolor='w', edgecolor='k')
fig.canvas.set_window_title('Roofline graph')

#fig2 = Max Energy vs Cores at all freqs
fig2 = plt.figure(num=None, figsize=(14, 7), dpi=80, facecolor='w', edgecolor='k')
fig2.canvas.set_window_title('Energy vs cores; all active cores @ 2.7Ghz')


# Returns the Axes instance
ax = fig.add_subplot(111) #Roofline plot
ax.set_xlabel('Instruction Intensity (Instr/Byte)', fontproperties = font, fontsize=12)
ax.set_ylabel('Performance, IPC (Instr/Cycle)', fontproperties = font, fontsize=12)

ax2 = fig2.add_subplot(111) # Energy vs Cores @ all freq
ax2.set_title('Energy consumed vs #active physical cores (HT=on) for nodeperf; all active cores',fontsize=14,fontweight='bold')
ax2.set_xlabel('#Active physical core(s)', fontproperties = font, fontsize=12)
ax2.set_ylabel('Total Energy consumed (J)', fontproperties = font, fontsize=12)
ax2.set_xlim(1, num_physical_cores_total)
ax2.xaxis.set_major_locator(MultipleLocator(1.0))


fig.subplots_adjust(left=0.07, bottom=0.10, right=0.89, top=0.95, wspace=0.86, hspace=0.27)
fig2.subplots_adjust(left=0.07, bottom=0.10, right=0.89, top=0.95, wspace=0.86, hspace=0.27)
 

# plot_Energy_vs_cores_all_freq()
plot_RL_all_freq(22)

xlim(xmin=0) # start at 0

show()



