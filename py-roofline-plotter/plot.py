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
    ax.text(X_MIN*1.1,(X_MIN*1.1*BW)*1.1, label+' ('+str(BW)+' Bytes/Cycle)',fontsize=8, rotation=np.arctan(INVERSE_GOLDEN_RATIO * AXIS_ASPECT_RATIO) * 180 / np.pi, verticalalignment = 'bottom')
    # ax.text(0.01,yCoordinateTransformed+0.05+0.0075*(len(str(BW))-1), label+' ('+str(BW)+' B/C)',fontsize=8, rotation=45, transform=ax.transAxes)


def plotRoofline():
    time, inst_per_cycle, op_intensity = read_csv.get_roofline_data_system()
    ax.plot(op_intensity, inst_per_cycle, 'r.')
    
    time_format = '%H:%M:%S.%f'
    
    times = []
    for i, val in enumerate(time):
        date_time = datetime.strptime(time[i], time_format)
        time_string = date_time.strftime(time_format)
        times.append(date_time)
         
    timex = matplotlib.dates.date2num(times) 
    ax2.plot_date(timex, op_intensity, ls='-', marker='.')
    ax2.axhline(y=balance_point, linewidth=0.75, ls='dotted', label="Balance Point line")   
    ax2.set_xticks(timex+20) # Tickmark + label at every plotted point
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    
    
    
        # Format the x-axis for dates (label formatting, rotation)
    # fig.autofmt_xdate(rotation=45)
    # fig.tight_layout() 
    
def plotRoofline_socket0():
    x, y = read_csv.get_roofline_points_socket0()
    ax.plot(x, y, 'b.')
    
def plotRoofline_socket1():
    x, y = read_csv.get_roofline_points_socket1()
    ax.plot(x, y, 'g.')
    
   

    

X_MIN=0.001
X_MAX=50
Y_MIN=0.001
Y_MAX=8

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
fig = plt.figure(num=None, figsize=(13, 6), dpi=80, facecolor='w', edgecolor='k')

# Returns the Axes instance
ax = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

#Log scale - Roofline is always log-log plot, so remove the condition if LOG_X
ax.set_yscale('log')
ax.set_xscale('log')

#formatting:
ax.set_title(TITLE,fontsize=14,fontweight='bold')
ax.set_xlabel(X_LABEL, fontproperties = font, fontsize=12)
ax.set_ylabel(Y_LABEL, fontproperties = font, fontsize=12)

ax2.set_title(TITLE,fontsize=14,fontweight='bold')
ax2.set_xlabel('Time', fontproperties = font, fontsize=12)
ax2.set_ylabel('Operational Intensity', fontproperties = font, fontsize=12)

ax2.set_aspect('auto')


#x-y range
ax.axis([X_MIN,X_MAX,Y_MIN,Y_MAX])
print INVERSE_GOLDEN_RATIO*AXIS_ASPECT_RATIO
ax.set_aspect(0.5)

 
 
# Manually adjust xtick/ytick labels when log scale
locs, labels = xticks()
minloc =int(log10(X_MIN))
maxloc =int(log10(X_MAX) +1)
newlocs = []
newlabels = []
for i in range(minloc,maxloc):
    newlocs.append(10**i)
    # Do not plot the first label, it is ugly in the corner
    if i==minloc:
        newlabels.append('')
    elif i==maxloc: #Do not plot the last label either
        newlabels.append('')
    elif 10**i <= 100:
        newlabels.append(str(10**i))
    else:
        newlabels.append(r'$10^ %d$' %i)
xticks(newlocs, newlabels)
  
locs, labels = yticks()
minloc =int(log10(Y_MIN))
maxloc =int(log10(Y_MAX) +1)
newlocs = []
newlabels = []
for i in range(minloc,maxloc):
    newlocs.append(10**i)
    if i==minloc:
        newlabels.append('')
    elif 10**i <= 100:
        newlabels.append(str(10**i))
    else:
        newlabels.append(r'$10^ %d$' %i)
yticks(newlocs, newlabels)





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
legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., prop={'size':9})

subplots_adjust(left=10.1, right=20.9, top=10.9, bottom=10.1)
fig.tight_layout()
show()
