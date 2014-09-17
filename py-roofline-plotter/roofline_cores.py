import numpy
from pylab import *
import read_csv

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.font_manager import FontProperties

import matplotlib.dates as mdates
from datetime import datetime

#Font properties
font_family = ['serif', 'sans-serif', 'monospace']
font_style  = ['normal', 'italic', 'oblique']
font = FontProperties()
font.set_family(font_family[1])

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
    #ax.text(X_MIN*1.1,(X_MIN*1.1*BW)*1.1, '            '+label+' ('+str(BW)+' Bytes/Cycle)',fontsize=8, rotation=np.arctan(INVERSE_GOLDEN_RATIO * 0.8) * 180 / np.pi, verticalalignment = 'bottom')
    # ax.text(0.01,yCoordinateTransformed+0.05+0.0075*(len(str(BW))-1), label+' ('+str(BW)+' B/C)',fontsize=8, rotation=45, transform=ax.transAxes)

#Filenames

#Plot only the rooflines
def plotRooflines_only():
    None
    

def plotRoofline():
    
    for i in range (1, 24):
        
        #time, time_stamp, inst_per_cycle, energy, energy_incremental = read_csv.get_timeline_data('csv/cores/nodeperf_' + str(i) + '_2.7.csv')
        time, inst_per_cycle, op_intensity, energy_SKT0, energy_SKT1 = read_csv.get_roofline_data_system('csv/cores/nodeperf_' + str(i) + '_2.7.csv')
        var = 'line' + str(i)
        colors = cm.rainbow(np.linspace(0, 1, 24))
        var, = ax.plot(op_intensity, inst_per_cycle, '.', color = colors[i], markersize=0.8, label='dgemm ' + str(i) + ' core 2.7 Ghz') 
        

     

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
    
    legend = ax.legend(loc=2, shadow=True, numpoints=10, bbox_to_anchor=(1.01, 1.0))
    
    #The frame is matplotlib.patches.Rectangle instance surrounding the legend.
    frame = legend.get_frame()
    frame.set_facecolor('0.90')
    
    # Set the fontsize
    for label in legend.get_texts():
        label.set_fontsize('8')
    
    for label in legend.get_lines():
        label.set_linewidth(1)  # the legend line width
    
    
    

X_MIN=0.01
X_MAX=100
Y_MIN=0.1
Y_MAX=4.2

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
ax = fig.add_subplot(111) #roofline plot




ax.set_yscale('log', basey=2)
ax.set_xscale('log', basex=2)

#formatting:
ax.set_title(TITLE,fontsize=14,fontweight='bold')
ax.set_xlabel(X_LABEL, fontproperties = font, fontsize=12)
ax.set_ylabel(Y_LABEL, fontproperties = font, fontsize=12)



#ax2.set_aspect('auto')


#x-y range
ax.axis([X_MIN,X_MAX,Y_MIN,Y_MAX])

# INVERSE_GOLDEN_RATIO*AXIS_ASPECT_RATIO
ax.set_aspect(0.5)



#Peak performance line and text
for p,l in zip(PEAK_PERF, PEAK_PERF_LABELS):
    addPerfLine(p,l)

#BW line and text
for i in range(2,24):
    val = [70/(2.7*i)]
    print val[0]
    
    for bw,l in zip(val, PEAK_BW_LABELS):
         addBWLine(bw,l)
    
    #Add the Balance point line (Operational Intensity at ridge point)
    #balance_point = PEAK_PERF[0] / val[0]
    #ax.axvline(x=balance_point, linewidth=0.75, color='black', ls='dotted', label="Balance Point line")
    
plotRoofline()

plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.3)

#subplots_adjust(left=10.1, right=20.9, top=10.9, bottom=10.1)
#matplotlib.pyplot.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
#fig.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
savefig('all.png')
show()

