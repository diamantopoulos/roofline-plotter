import numpy
from pylab import *
import read_csv

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import matplotlib.dates as mdates
from datetime import datetime


'Method to format the time for plotting with MPL'
def format_time_for_plotting(time):
  
    time_format = '%H:%M:%S.%f'
    
    times = []
    for i, val in enumerate(time):
        date_time = datetime.strptime(time[i], time_format)
        time_string = date_time.strftime(time_format)
        times.append(date_time)
         
    return matplotlib.dates.date2num(times) 

'Method to add a bandwidth line to a roofline graph'
'Takes a bandwidth value'
def addBWLine(BW, label):
    x = np.linspace(X_MIN, X_MAX, 10)
    y = x*BW
    ax.plot(x, y, linewidth=0.75, color='black')
    yCoordinateTransformed = (log(X_MIN*BW)-log(Y_MIN))/(log(Y_MAX/Y_MIN))+0.16 #0.16 is the offset of the lower axis
    ax.text(X_MIN*1.1,(X_MIN*1.1*BW)*1.1, '            '+label+' ('+str(BW)+' Bytes/Cycle)',fontsize=8, rotation=np.arctan(INVERSE_GOLDEN_RATIO * 0.8) * 180 / np.pi, verticalalignment = 'bottom')
    # ax.text(0.01,yCoordinateTransformed+0.05+0.0075*(len(str(BW))-1), label+' ('+str(BW)+' B/C)',fontsize=8, rotation=45, transform=ax.transAxes)











