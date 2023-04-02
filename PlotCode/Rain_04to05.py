#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 17:26:03 2023

@author: guoding_chen
"""

import numpy as np

import pandas as pd 
import matplotlib

matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt



# set the family font 
font1={'family':'Arial',
     'style':'normal',
    'weight':'normal',
     'size':18}
font_xylable={'family':'Arial',
     'style':'normal',
    'weight':'normal',
     'size':40}
font_legend={'family':'Arial',
     'style':'normal',
    'weight':'normal',
     'size':14}



# read the rainfall data 
dataset = pd.read_csv('../PlotData/Outlet_Yuehe_Results.csv')

rain = dataset.Rain

rain = rain[47:72]

time = np.linspace(1, len(rain), num = len(rain))


fig, ax1 = plt.subplots(figsize=(12, 1.5))

ax1.bar(time, rain, width = 2, color = 'C0', alpha = 1, zorder=1)


ax1.set_xlim([1, 25])
ax1.set_xticks([1, 4, 7, 13, 25])
ax1.set_xticklabels(['0400', '0403', '0406', '0412', '0500'], fontsize=12)
# ax1.set_xlabel('Time', fontsize=15)

ax1.set_ylim([0, 30])
ax1.set_yticks([0, 10, 20, 30])
ax1.set_yticklabels([0, 10, 20, 30], fontsize=12)
ax1.set_ylabel('Rainfall ($ \mathrm{mm/h}$)', fontsize=12)


plt.tight_layout()
plt.show()















