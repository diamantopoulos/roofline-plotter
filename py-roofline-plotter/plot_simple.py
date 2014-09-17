import numpy as np
from pylab import *
import read_csv
import utilities 
from scipy import interpolate

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import matplotlib.dates as mdates
from datetime import datetime
import matplotlib.cm as cm
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

font = fm.FontProperties(
        family = 'Gill Sans', fname = 'wqy-zenhei.ttc')

num_physical_cores_total = 24
colors = cm.rainbow(np.linspace(0, 1, num_physical_cores_total))

def plot_all_graphs():
    energy_inc = []
    for i in range (1, num_physical_cores_total):
        time, time_stamp, inst_per_cycle, energy, energy_incremental = read_csv.get_timeline_data('csv/cores/nodeperf_' + str(i) + '_2.7.csv')
        
        var = 'line' + str(i)
        #Plot Energy vs Time
        var, = ax.plot(time_stamp, energy_incremental, '.', color = colors[i] , markersize=0.8, label= str(i) + ' cores')
        #Plot IPC vs Time
        var, = ax2.plot(time_stamp, inst_per_cycle, '.', color = colors[i] , markersize=0.8, label= str(i) + ' cores')
        #Plot total_energy vs cores
        var, = ax3.plot(i, energy_incremental[-1], '*', color = colors[i] , markersize=10, label= str(i) + ' cores')
        energy_inc.append(energy_incremental[-1])
    
    #Plot spline Energy vs cores
    x = range(1,num_physical_cores_total)
    tck = interpolate.splrep(x, energy_inc, s=0)
    xnew = np.arange(1,num_physical_cores_total,np.pi/150)
    ynew = interpolate.splev(xnew, tck, der=0)
    ax3.plot(xnew, ynew)
    
   
    #Add legends
    legends = []    
    legends.append(ax.legend(loc=2, shadow=True, numpoints=10, bbox_to_anchor=(1.01, 1.0)))
    legends.append(ax2.legend(loc=2, shadow=True, numpoints=10, bbox_to_anchor=(1.01, 1.0)))
    legends.append(ax3.legend(loc=2, shadow=True, numpoints=1, bbox_to_anchor=(1.01, 1.0)))
    
    for legend in legends:
        #The frame is matplotlib.patches.Rectangle instance surrounding the legend.
        frame = legend.get_frame()
        frame.set_facecolor('0.90')
        # Set the fontsize
        for label in legend.get_texts():
            label.set_fontsize('8')
             
        for label in legend.get_lines():
            label.set_linewidth(1)  # the legend line width     
        

#fig = Energy vs. Time graph
fig = plt.figure(num=None, figsize=(14, 7), dpi=80, facecolor='w', edgecolor='k')
fig.canvas.set_window_title('Energy usage, nodeperf -nompi, all active cores @ 2.7Ghz')

#fig2 = Instruction intensity vs Time graph
fig2 = plt.figure(num=None, figsize=(14, 7), dpi=80, facecolor='w', edgecolor='k')
fig2.canvas.set_window_title('Instruction intensity vs time for nodeperf; all active cores @ 2.7Ghz')

#fig3 = Max Energy vs Cores
fig3 = plt.figure(num=None, figsize=(14, 7), dpi=80, facecolor='w', edgecolor='k')
fig3.canvas.set_window_title('Energy vs cores; all active cores @ 2.7Ghz')


# Returns the Axes instance
ax = fig.add_subplot(111) #energy usage/time plot + perf/time plot
ax.set_title('Energy usage, nodeperf -nompi, all active cores @ 2.7Ghz',fontsize=14,fontweight='bold')
ax.set_xlabel('Timestamp (s)', fontproperties = font, fontsize=12)
ax.set_ylabel('Incremental energy usage (J)', fontproperties = font, fontsize=12)
ax.set_ylim([0, 30000])

ax2 = fig2.add_subplot(111) # inst_intensity/time plot + perf/time plot
ax2.set_title('Instruction intensity vs time for nodeperf; all active cores @ 2.7Ghz',fontsize=14,fontweight='bold')
ax2.set_xlabel('Timestamp (s)', fontproperties = font, fontsize=12)
ax2.set_ylabel('Instruction intensity (Inst/Byte)', fontproperties = font, fontsize=12)
ax2.set_ylim([0, 4.1])

ax3 = fig3.add_subplot(111) # energy vs cores
ax3.set_title('Energy consumed vs #active physical cores (HT=on) for nodeperf; all active cores @ 2.7Ghz',fontsize=14,fontweight='bold')
ax3.set_xlabel('#Active physical core(s)', fontproperties = font, fontsize=12)
ax3.set_ylabel('Total Energy consumed (J)', fontproperties = font, fontsize=12)
ax3.set_xlim(1, num_physical_cores_total)
ax3.xaxis.set_major_locator(MultipleLocator(1.0))


fig.subplots_adjust(left=0.07, bottom=0.10, right=0.89, top=0.95, wspace=0.86, hspace=0.27)
fig2.subplots_adjust(left=0.07, bottom=0.10, right=0.89, top=0.95, wspace=0.86, hspace=0.27)
fig3.subplots_adjust(left=0.07, bottom=0.10, right=0.89, top=0.95, wspace=0.86, hspace=0.27)
 

#plot_all_graphs()


xlim(xmin=0) # start at 0
#plt.tight_layout(pad, h_pad, w_pad, rect)



show()



