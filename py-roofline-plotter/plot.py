import numpy
from pylab import *
import read_csv

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import matplotlib.dates as mdates
from datetime import datetime

font = fm.FontProperties(
        family = 'Gill Sans', fname = 'wqy-zenhei.ttc')

def addPerfLine(peakPerf, label):
    #Peak performance line and text
    ax.axhline(y=peakPerf, linewidth=0.75, color='black')
    #ax.text(X_MAX/10.0, PEAK_PERF+(PEAK_PERF)/10, "Peak Performance ("+str(PEAK_PERF)+" F/C)", fontsize=8)
    label_string = label+" ("+str(peakPerf)+" Instr/Cycle)"
    yCoordinateTransformed = (log(peakPerf)-log(Y_MIN))/(log(Y_MAX/Y_MIN))
    ax.text(1 - len(label_string) / 100. - 0.01,yCoordinateTransformed+0.01, label_string, fontsize=8, transform=ax.transAxes)
    

def addBWLine(BW, label):
    x = np.linspace(X_MIN, X_MAX, 10)
    y = x*BW
    ax.plot(x, y, linewidth=0.75, color='black')
    yCoordinateTransformed = (log(X_MIN*BW)-log(Y_MIN))/(log(Y_MAX/Y_MIN))+0.16 #0.16 is the offset of the lower axis
    ax.text(X_MIN*1.1,(X_MIN*1.1*BW)*1.1, '            '+label+' ('+str(BW)+' Bytes/Cycle)',fontsize=8, rotation=np.arctan(INVERSE_GOLDEN_RATIO * 0.8) * 180 / np.pi, verticalalignment = 'bottom')
    # ax.text(0.01,yCoordinateTransformed+0.05+0.0075*(len(str(BW))-1), label+' ('+str(BW)+' B/C)',fontsize=8, rotation=45, transform=ax.transAxes)

#Filenames

#Plot only the rooflines
def plotRooflines_only():
    None
    

def plotRoofline():
    time, inst_per_cycle, op_intensity, energy_SKT0, energy_SKT1 = read_csv.get_roofline_data_system('csv/cores/nodeperf_1_2.7.csv')
    ax.plot(op_intensity, inst_per_cycle, 'r.', markersize=1.8, label='dgemm 1 core 2.7 Ghz') 
    time, inst_per_cycle, op_intensity, energy_SKT0, energy_SKT1 = read_csv.get_roofline_data_system('csv/cores/nodeperf_2_2.7.csv')
    ax.plot(op_intensity, inst_per_cycle, 'k.', markersize=1.8, label='dgemm 2 core 2.7 Ghz')
#     time, inst_per_cycle, op_intensity, energy_SKT0, energy_SKT1 = read_csv.get_roofline_data_system('csv/freq/dgemm1.4Ghz.csv')
#     ax.plot(op_intensity, inst_per_cycle, 'g.', markersize=1.8, label='dgemm 1.4 Ghz')
#     time, inst_per_cycle, op_intensity, energy_SKT0, energy_SKT1 = read_csv.get_roofline_data_system('csv/freq/dgemm1.2Ghz.csv')
#     ax.plot(op_intensity, inst_per_cycle, 'b.', markersize=1.8, label='dgemm 1.2 Ghz')
    
#     time, inst_per_cycle, op_intensity, energy_SKT0, energy_SKT1 = read_csv.get_roofline_data_system('csv/freq/ihpcg2.7Ghz.csv')
#     ax.plot(op_intensity, inst_per_cycle, 'r.', markersize=1.8, label='ihpcg 2.7 Ghz') 
#     time, inst_per_cycle, op_intensity, energy_SKT0, energy_SKT1 = read_csv.get_roofline_data_system('csv/freq/ihpcg2.2Ghz.csv')
#     ax.plot(op_intensity, inst_per_cycle, 'k.', markersize=1.8, label='ihpcg 2.2 Ghz')
#     time, inst_per_cycle, op_intensity, energy_SKT0, energy_SKT1 = read_csv.get_roofline_data_system('csv/freq/ihpcg1.4Ghz.csv')
#     ax.plot(op_intensity, inst_per_cycle, 'g.', markersize=1.8, label='ihpcg 1.4 Ghz')
#     time, inst_per_cycle, op_intensity, energy_SKT0, energy_SKT1 = read_csv.get_roofline_data_system('csv/freq/ihpcg1.2Ghz.csv')
#     ax.plot(op_intensity, inst_per_cycle, 'b.', markersize=1.8, label='ihpcg 1.2 Ghz')
#      
    
    legend = ax.legend(bbox_to_anchor=(1.35, 0),loc='lower right', shadow=True)
    
    #The frame is matplotlib.patches.Rectangle instance surrounding the legend.
    frame = legend.get_frame()
    frame.set_facecolor('0.90')
    
    # Set the fontsize
    for label in legend.get_texts():
        label.set_fontsize('8')
    
    for label in legend.get_lines():
        label.set_linewidth(1)  # the legend line width
    
    
    
    time_format = '%H:%M:%S.%f'
    
    times = []
    for i, val in enumerate(time):
        date_time = datetime.strptime(time[i], time_format)
        time_string = date_time.strftime(time_format)
        times.append(date_time)
         
    timex = matplotlib.dates.date2num(times) 
    
    #Plot Performance and Op_intensity vs time
    ax2.plot_date(timex, op_intensity, ls='-', marker='.', c='r', markersize=0.1)
    ax2.set_yscale('log',  basey=10)
    ax2.set_ylabel('Operational Intensity', fontproperties = font, fontsize=12, color='r')
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    ax2.axhline(y=balance_point, linewidth=0.75, ls='dotted', label="Balance Point line")   
    
    #ax2.set_xticks(timex+20) # Tickmark + label at every plotted point
    #ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    
    # Format the x-axis for dates (label formatting, rotation)
    # fig.autofmt_xdate(rotation=45)
    # fig.tight_layout()
    
    ax3 = ax2.twinx()    
    ax3.set_ylabel('Performance (Instr/Cycle)', color='b')
    for tl in ax3.get_yticklabels():
        tl.set_color('b')
    ax3 = plot_date(timex, inst_per_cycle, ls='-', marker='.', markersize=0.1)
    
    
    #Plot Energy for each socket vs time
    ax4.plot_date(timex, energy_SKT0, ls='-', marker='.', c='g', markersize=0.1)
    ax4.set_ylabel('Energy Socket 0 (Joules)', color='g')
    for tl in ax4.get_yticklabels():
        tl.set_color('g')
        
    ax5 = ax4.twinx()
    #ax5.set_ylim([0.1, 20])
    ax5.plot_date(timex, energy_SKT1, ls='-', marker='.', c='r', markersize=0.1)
    ax5.set_ylabel('Energy Socket 1 (Joules)', color='r')
    for tl in ax5.get_yticklabels():
        tl.set_color('r')   
    
    
def plotRoofline_socket0():
    x, y = read_csv.get_roofline_points_socket0()
    ax.plot(x, y, 'b.')
    
def plotRoofline_socket1():
    x, y = read_csv.get_roofline_points_socket1()
    ax.plot(x, y, 'g.')
    
   

    

X_MIN=0.01
X_MAX=10
Y_MIN=0.1
Y_MAX=6

PEAK_PERF=[4.0]
PEAK_PERF_LABELS=['Scalar Peak Performance']
PEAK_BW=[25.93]
PEAK_BW_LABELS = ['Bandwidth']

INVERSE_GOLDEN_RATIO=0.618
OUTPUT_FILE="data-rooflinePlot.pdf"
TITLE=""
X_LABEL="Operational Intensity [Instr/Byte]"
Y_LABEL="Performance [Instr/Cycle]"
ANNOTATE_POINTS=1
AXIS_ASPECT_RATIO=log10(X_MAX/X_MIN)/log10(Y_MAX/Y_MIN)

colors=[(0.6,0.011,0.043), (0.258, 0.282, 0.725),(0.2117, 0.467, 0.216),'#CC0033' ,'#FFFF00','green','cyan','yellow','brown','orange' ]

#fig = roofline plot only
fig = plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')
fig.canvas.set_window_title('Roofline models')

# Returns the Axes instance
ax = fig.add_subplot(311) #roofline plot
ax2 = fig.add_subplot(312) #op_intensity/time plot + perf/time plot
ax4 = fig.add_subplot(313) #Energy/time plot

#Log scale - Roofline is always log-log plot, so remove the condition if LOG_X
# ax.set_yscale('linear')
# ax.set_xscale('linear')

ax.set_yscale('log', basey=2)
ax.set_xscale('log', basex=2)

#formatting:
ax.set_title(TITLE,fontsize=14,fontweight='bold')
ax.set_xlabel(X_LABEL, fontproperties = font, fontsize=12)
ax.set_ylabel(Y_LABEL, fontproperties = font, fontsize=12)

ax2.set_title(TITLE,fontsize=14,fontweight='bold')
ax2.set_xlabel('Time', fontproperties = font, fontsize=12)
ax4.set_xlabel('Time', fontproperties = font, fontsize=12)


#ax2.set_aspect('auto')


#x-y range
ax.axis([X_MIN,X_MAX,Y_MIN,Y_MAX])
ax2.set_ylim([0.1, 100])
#ax4.set_ylim([0.1, 20])

# INVERSE_GOLDEN_RATIO*AXIS_ASPECT_RATIO
ax.set_aspect(0.5)

 
 
# Manually adjust xtick/ytick labels when log scale
# locs, labels = xticks()
# minloc =int(log10(X_MIN))
# maxloc =int(log10(X_MAX) +1)
# newlocs = []
# newlabels = []
# for i in range(minloc,maxloc):
#     newlocs.append(10**i)
#     # Do not plot the first label, it is ugly in the corner
#     if i==minloc:
#         newlabels.append('')
#     elif i==maxloc: #Do not plot the last label either
#         newlabels.append('')
#     elif 10**i <= 100:
#         newlabels.append(str(10**i))
#     else:
#         newlabels.append(r'$10^ %d$' %i)
# xticks(newlocs, newlabels)
#   
# locs, labels = yticks()
# minloc =int(log10(Y_MIN))
# maxloc =int(log10(Y_MAX) +1)
# newlocs = []
# newlabels = []
# for i in range(minloc,maxloc):
#     newlocs.append(10**i)
#     if i==minloc:
#         newlabels.append('')
#     elif 10**i <= 100:
#         newlabels.append(str(10**i))
#     else:
#         newlabels.append(r'$10^ %d$' %i)
# yticks(newlocs, newlabels)





#Peak performance line and text
for p,l in zip(PEAK_PERF, PEAK_PERF_LABELS):
    addPerfLine(p,l)

#BW line and text
for bw,l in zip(PEAK_BW, PEAK_BW_LABELS):
    addBWLine(bw,l)
    
#Add the Balance point line (Operational Intensity at ridge point)
balance_point = PEAK_PERF[0] / PEAK_BW[0]
ax.axvline(x=balance_point, linewidth=0.75, color='black', ls='dotted', label="Balance Point line")
    
plotRoofline()
#plotRoofline_socket0()
#plotRoofline_socket1()

#Plot the roofline graph and add the legend
#legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., prop={'size':9})

plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.3)

#subplots_adjust(left=10.1, right=20.9, top=10.9, bottom=10.1)
#matplotlib.pyplot.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
#fig.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
savefig('all.png')
show()

