#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 23:16:47 2022

@author: guoding_chen
"""

# this program is used to plot the sensitivity analysis


import numpy as np

import matplotlib as mpl
mpl.use('Qt5Agg')
import matplotlib.pyplot as plt

font_legend={'family':'Arial',
     'style':'normal',
    'weight':'normal',
     'size':10}


# define the function that detect the character in a text file
def readvalue_fromtxt_de(file_path, symbol):
    file = open(file_path,'r')
    contents = file.readlines()
    
    value_str = [s for s in contents if symbol in s]
    
    # split each element in list and keep second part
    value_num = [item.split('=', 1)[1] for item in value_str]
    
    #value_str = [re.findall( r'\d+\.*\d*', s ) for s in value_str]
    value = [float(x) for x in np.array(value_num)]

    return value


def readvalue_fromtxt_percentage(file_path, symbol):
    file = open(file_path,'r')
    contents = file.readlines()
    
    value_str = [s for s in contents if symbol in s]
    
    # split each element in list and keep second part
    value_num = [item.split(':', 1)[1] for item in value_str]
    
    #value_str = [re.findall( r'\d+\.*\d*', s ) for s in value_str]
    value = [float(x) for x in np.array(value_num)]

    return value





file_path = '../PlotData/De_max1200.log'

# read the landslide density value

De_value = readvalue_fromtxt_de(file_path, "De =")

unstable_area = readvalue_fromtxt_percentage(file_path, "Unstable_percentage")

runtime = readvalue_fromtxt_percentage(file_path, "Landslide runtime")


fig, (ax1,ax2) = plt.subplots(1, 2, figsize=(11, 4), gridspec_kw={'width_ratios': [1, 0.6]})


ax1.plot(De_value, unstable_area, color="black", linewidth = 2, 
          linestyle='-', marker='o', mfc='none', 
          markersize = 7,label="$Q_{obs}$")

ax1.set_xlim([10, 1200])
ax1.set_xticks([200, 400, 600, 800, 1000])
ax1.set_xticklabels([200, 400, 600, 800, 1000], fontsize=16)
ax1.set_xlabel('$De$', fontsize=15)

ax1.set_ylim([0, 0.2])
ax1.set_yticks([0, 0.05, 0.1, 0.15, 0.2])
ax1.set_yticklabels(["0", "5", "10", "15", "20"], fontsize=15)

ax1.set_ylabel('Unstable area percentage (%)', fontsize = 15)

ax1.grid(linestyle='--')




ax2.plot(De_value, runtime, color="black", linewidth = 2, 
          linestyle='-', marker='o', label="$Q_{obs}$", mfc='none', 
          markersize = 7)

ax2.set_xlim([10, 1200])
ax2.set_xticks([200, 400, 600, 800, 1000])
ax2.set_xticklabels([200, 400, 600, 800, 1000], fontsize=16)
ax2.set_xlabel('$De$', fontsize=15)

ax2.set_ylabel('Runtime (s)', fontsize = 15)
ax2.set_ylim([0, 4000])
ax2.set_yticks([0, 1000, 2000, 3000, 4000])
ax2.set_yticklabels([0, 1000, 2000, 3000, 4000], fontsize=15)

ax2.grid(linestyle='--')





plt.tight_layout()
plt.show()






