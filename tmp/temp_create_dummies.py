#!/bin/python


"""
Show how to set custom font properties.

For interactive users, you can also use kwargs to the text command,
which requires less typing.  See examples/fonts_demo_kw.py
"""
from matplotlib.font_manager import FontProperties
from pylab import *


import os
import shutil


cpu_frequencies = [2701000, 2700000, 2500000, 2400000, 2300000, 2200000, 2100000, 2000000, 1900000, 1800000, 1700000, 1600000, 1500000, 1400000, 1300000, 1200000]
num_physical_cores_total = 24

for i in range(len(cpu_frequencies)):
    cpu_frequencies[i] = float(float(cpu_frequencies[i])/float(1000000))


src = 'freq_proc_csv/src.csv'

def create_fake_files():
    for i, cpu_freq in enumerate(cpu_frequencies):
        for j in range(1, num_physical_cores_total):
            csv_path = 'freq_proc_csv/nodeperf_' + str(cpu_freq) + 'Ghz_' + str(num_physical_cores_total-j) + 'act_cores.csv'
            print i , cpu_freq
            #time, time_stamp, inst_per_cycle, energy, energy_incremental = read_csv.get_timeline_data(csv_path)
            #shutil.copyfile(src, csv_path)
    print 'Done'
   
    
   



subplot(111, axisbg='w')

font0 = FontProperties()
alignment = {'horizontalalignment':'center', 'verticalalignment':'baseline'}
###  Show family options

family = ['serif', 'sans-serif', 'monospace']

font1 = font0.copy()
font1.set_size('large')

t = text(-0.8, 0.9, 'family', fontproperties=font1,
         **alignment)

yp = [0.7, 0.5, 0.3, 0.1, -0.1, -0.3, -0.5]

for k in range(len(family)):
    font = font0.copy()
    font.set_family(family[k])
    if k == 2:
        None
        #font.set_name('Script MT')
    t = text(-0.8, yp[k], family[k], fontproperties=font,
             **alignment)

###  Show style options

style  = ['normal', 'italic', 'oblique']

t = text(-0.4, 0.9, 'style', fontproperties=font1,
         **alignment)

for k in range(3):
    font = font0.copy()
    font.set_family('sans-serif')
    font.set_style(style[k])
    t = text(-0.4, yp[k], style[k], fontproperties=font,
             **alignment)

###  Show variant options

variant= ['normal', 'small-caps']

t = text(0.0, 0.9, 'variant', fontproperties=font1,
         **alignment)

for k in range(2):
    font = font0.copy()
    font.set_family('serif')
    font.set_variant(variant[k])
    t = text( 0.0, yp[k], variant[k], fontproperties=font,
             **alignment)

###  Show weight options

weight = ['light', 'normal', 'medium', 'semibold', 'bold', 'heavy', 'black']

t = text( 0.4, 0.9, 'weight', fontproperties=font1,
         **alignment)

for k in range(7):
    font = font0.copy()
    font.set_weight(weight[k])
    t = text( 0.4, yp[k], weight[k], fontproperties=font,
             **alignment)

###  Show size options

size  = ['xx-small', 'x-small', 'small', 'medium', 'large',
         'x-large', 'xx-large']

t = text( 0.8, 0.9, 'size', fontproperties=font1,
         **alignment)

for k in range(7):
    font = font0.copy()
    font.set_size(size[k])
    t = text( 0.8, yp[k], size[k], fontproperties=font,
             **alignment)

###  Show bold italic

font = font0.copy()
font.set_style('italic')
font.set_weight('bold')
font.set_size('x-small')
t = text(0, 0.1, 'bold italic', fontproperties=font,
         **alignment)

font = font0.copy()
font.set_style('italic')
font.set_weight('bold')
font.set_size('medium')
t = text(0, 0.2, 'bold italic', fontproperties=font,
         **alignment)

font = font0.copy()
font.set_style('italic')
font.set_weight('bold')
font.set_size('x-large')
t = text(0, 0.3, 'bold italic', fontproperties=font,
         **alignment)

axis([-1,1,0,1])

show()