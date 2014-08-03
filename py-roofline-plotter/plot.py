import numpy
from pylab import *

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

font = fm.FontProperties(
        family = 'Gill Sans', fname = 'wqy-zenhei.ttc')

def addPerfLine(peakPerf, label):
    #Peak performance line and text
    ax.axhline(y=peakPerf, linewidth=0.75, color='black')
    #ax.text(X_MAX/10.0, PEAK_PERF+(PEAK_PERF)/10, "Peak Performance ("+str(PEAK_PERF)+" F/C)", fontsize=8)
    label_string = label+" ("+str(peakPerf)+" F/C)"
    yCoordinateTransformed = (log(peakPerf)-log(Y_MIN))/(log(Y_MAX/Y_MIN))
    ax.text(1 - len(label_string) / 120. - 0.01,yCoordinateTransformed+0.01, label_string, fontsize=8, transform=ax.transAxes)
    

def addBWLine(BW, label):
    x = np.linspace(X_MIN, X_MAX, 10)
    y = x*BW
    ax.plot(x, y, linewidth=0.75, color='black')
    yCoordinateTransformed = (log(X_MIN*BW)-log(Y_MIN))/(log(Y_MAX/Y_MIN))+0.16 #0.16 is the offset of the lower axis
    ax.text(X_MIN*1.1,(X_MIN*1.1*BW)*1.1, label+' ('+str(BW)+' B/C)',fontsize=8, rotation=np.arctan(INVERSE_GOLDEN_RATIO * AXIS_ASPECT_RATIO) * 180 / np.pi, verticalalignment = 'bottom')
    #~ ax.text(0.01,yCoordinateTransformed+0.05+0.0075*(len(str(BW))-1), label+' ('+str(BW)+' B/C)',fontsize=8, rotation=45, transform=ax.transAxes)

X_MIN=0.01
X_MAX=100.0
Y_MIN=0.01
Y_MAX=50.0
#PEAK_PERF=8.0
#PEAK_BW=11.95

PEAK_PERF=[2.0, 2.0]
PEAK_PERF_LABELS=['Scalar Peak Performance']
PEAK_BW=[6.3]
PEAK_BW_LABELS = ['Bandwidth']

INVERSE_GOLDEN_RATIO=0.618
OUTPUT_FILE="data-rooflinePlot.pdf"
TITLE=""
X_LABEL="Operational Intensity [Flops/Byte]"
Y_LABEL="Performance [Flops/Cycle]"
ANNOTATE_POINTS=1
AXIS_ASPECT_RATIO=log10(X_MAX/X_MIN)/log10(Y_MAX/Y_MIN)


colors=[(0.6,0.011,0.043), (0.258, 0.282, 0.725),(0.2117, 0.467, 0.216),'#CC0033' ,'#FFFF00','green','cyan','yellow','brown','orange' ]
fig = plt.figure()
# Returns the Axes instance
ax = fig.add_subplot(111)

#Log scale - Roofline is always log-log plot, so remove the condition if LOG_X
ax.set_yscale('log')
ax.set_xscale('log')

#formatting:
ax.set_title(TITLE,fontsize=14,fontweight='bold')
ax.set_xlabel(X_LABEL, fontproperties = font, fontsize=12)
ax.set_ylabel(Y_LABEL, fontproperties = font, fontsize=12)


#x-y range
ax.axis([X_MIN,X_MAX,Y_MIN,Y_MAX])
ax.set_aspect(INVERSE_GOLDEN_RATIO*AXIS_ASPECT_RATIO)



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
    elif i==maxloc-1: #Do not plot the last label either
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



# Performance, measured in Instr/Cycle (PCM::IPC)
performance = [ 1,2 ]
op_intensity = [ 1,5 ]

#Peak performance line and text
for p,l in zip(PEAK_PERF, PEAK_PERF_LABELS):
    addPerfLine(p,l)

#BW line and text
for bw,l in zip(PEAK_BW, PEAK_BW_LABELS):
    addBWLine(bw,l)

#Plot the roofline graph.
plot (performance, op_intensity)

show()