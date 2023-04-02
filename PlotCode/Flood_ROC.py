# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 20:12:28 2022

@author: cgdwo
"""


import numpy as np
import pandas as pd 
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import xlrd


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


# read data 
dataset_HanZhong = pd.read_csv('../PlotData/Outlet_Yuehe_Results.csv')

#plt.style.use('seaborn')

#  displacement data

rain = dataset_HanZhong.Rain
R_simu = dataset_HanZhong.R
R_obs = dataset_HanZhong.RObs
time = np.linspace(1, len(rain), num = len(rain))


# read the ROC-AUC data
ROC_data = xlrd.open_workbook('../PlotData/ROC_AUC.xlsx')
ROC_data_table = ROC_data.sheets()[0]

FPR = [i for i in ROC_data_table.col_values(0) if isinstance(i, (int, float))]
TPR = [i for i in ROC_data_table.col_values(1) if isinstance(i, (int, float))]





fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4), gridspec_kw={'width_ratios': [1, 0.8]})


R_obs_mean = np.mean(R_obs)
Bias = (sum(R_simu) - sum(R_obs)) / sum(R_obs)
NSE = 1-sum( (R_obs- R_simu) * (R_obs - R_simu) ) / sum( (R_obs - R_obs_mean) *(R_obs - R_obs_mean) )
CC_array = np.corrcoef(R_simu, R_obs)
CC = CC_array[0,1]

print("NSCE = ", NSE)
print("CC = ", CC)
print("Bias = ", Bias)


ax1.plot(time, R_obs, color="black", linewidth = 2, linestyle='-', label="$Q_{obs}$", zorder=2)
ax1.plot(time, R_simu, color="red", linewidth = 2, linestyle='-',label = "$Q_{simu}$")

ax1.set_xlim([1, 150])
ax1.set_xticks([1, 48, 96, 145])
ax1.set_xticklabels(['07/02', '07/04', '07/06', '07/08'], fontsize=15)
ax1.set_xlabel('Time', fontsize=18)

ax1.set_ylim([0, 2000])
ax1.set_yticks([0, 500, 1000, 1500, 2000])
ax1.set_yticklabels([0, 500, 1000, 1500, 2000], fontsize=15)
# ax.text(210, 4500, "(a)", fontsize=20, weight = "light", color = "k")

ax1.text(90, 800, "NSEC = 0.72\nCC = 0.86\nBias = $4.0$%", fontsize = 14, weight = "light", color = "k", 
          bbox = dict(edgecolor='k', boxstyle='round', alpha = 0.2))



ax1.grid(linestyle='--')

ax1.set_ylabel('Discharge ($\mathrm{m^{3}/s}$)', font1)

ax1.legend(loc = 1, prop=font_legend, edgecolor="k", ncol=1, 
           handletextpad = 0.3, bbox_to_anchor=(0.85, 0.9))


ax1.text(5, 1700, "(a)", fontsize=20, weight = "light", color = "k")

twin = ax1.twinx()
twin.spines.right.set_position(("axes", 1))


twin_y_ticks = np.linspace(0, 100, 5)
plt.ylim(0,100)
plt.yticks(twin_y_ticks, fontproperties = "Arial", size = 15)
twin.invert_yaxis()

twin.bar(time, rain, width = 2, color = 'C0', alpha = 1, zorder=1)

twin.set_ylabel('Rainfall ($ \mathrm{mm/h}$)', font1)
twin.yaxis.label.set_color('C0')



x_diagonal = np.linspace(0, 1, num = 2)
y_diagonal = x_diagonal

ax2.plot(FPR, TPR, color="C1", 
        linewidth = 2, linestyle='-', label = "Bare")
ax2.plot(x_diagonal, y_diagonal, color="black", 
        linewidth = 1.5, linestyle='--')


ax2.set_xlim([0,1])
ax2.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1])
ax2.set_xticklabels([0, 0.2, 0.4, 0.6, 0.8, 1], fontsize=15)

ax2.set_ylim([0, 1])
ax2.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
ax2.set_yticklabels([0, 0.2, 0.4, 0.6, 0.8, 1], fontsize=15)

ax2.set_xlabel("FPR", font1)
ax2.set_ylabel("TPR", font1)
ax2.text(0.05, 0.85, "(b)", fontsize=20, weight = "light", color = "k")

ax2.text(0.6, 0.25, "$ AUC=0.74 $", fontsize = 16)

ax2.grid(linestyle='--')




plt.tight_layout()
plt.show()













