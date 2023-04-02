#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 12:07:47 2022

@author: guoding_chen
"""

# this program is used to plot the evaluation of the parallel computation
# for hydrological and landslide processes
# for both speedup and efficiency



# plot the hydrology
# read the time file 


import numpy as np
import re
import matplotlib as mpl
mpl.use('Qt5Agg')
import matplotlib.pyplot as plt

font_legend={'family':'Arial',
     'style':'normal',
    'weight':'normal',
     'size':10}

# get the modeling threats number

# ----------------------------subbasins number = 6----------------------------
Thread_file = open('../PlotData/subbasin6.log','r')

Thread_contents = Thread_file.readlines()

# identify the Hydrological threads
Thread_str = [s for s in Thread_contents if "Thread for hydrology:" in s]


Thread_str = [re.sub(r'\D', '', s) for s in Thread_str]


CoreNum = [int(x) for x in Thread_str]



# file = open('../Runtime_test/De50Tile20.log','r')
# contents = file.readlines()
# time_str = [s for s in contents if "Landslide runtime (s)" in s]
# time_str = [re.findall( r'\d+\.*\d*', s ) for s in time_str]
# time = [float(x) for x in np.array(time_str)]

# Speedup = [time[0]/x for x in time]

# E_Hydro = np.array(Speedup) / np.array(CoreNum)
    
    
# print(sum(time))




# define the function that compute the Speedup and efficiency of the hydrological parallel
def readHydroRunTime_fromtxt(file_path):
    file = open(file_path,'r')
    contents = file.readlines()
    time_str = [s for s in contents if "Hydrological runtime (s)" in s]
    time_str = [re.findall( r'\d+\.*\d*', s ) for s in time_str]
    time = [float(x) for x in np.array(time_str)]

    Speedup = [time[0]/x for x in time]
   
    E_Hydro = np.array(Speedup) / np.array(CoreNum)
    
    return Speedup, E_Hydro


# define the function that compute the Speedup and efficiency of the slope stability modeling
def readLandRunTime_fromtxt(file_path):
    file = open(file_path,'r')
    contents = file.readlines()
    time_str = [s for s in contents if "Landslide runtime (s)" in s]
    time_str = [re.findall( r'\d+\.*\d*', s ) for s in time_str]
    time = [float(x) for x in np.array(time_str)]

    Speedup = [time[0]/x for x in time]

    E_Hydro = np.array(Speedup) / np.array(CoreNum)
    
    return Speedup, E_Hydro



[Speedup_Subbasin6, E_Hydro_Subbasin6] = readHydroRunTime_fromtxt('../PlotData/subbasin6.log')
[Speedup_Subbasin12, E_Hydro_Subbasin12] = readHydroRunTime_fromtxt('../PlotData/subbasin12.log')
[Speedup_Subbasin24, E_Hydro_Subbasin24] = readHydroRunTime_fromtxt('../PlotData/subbasin24.log')
[Speedup_Subbasin48, E_Hydro_Subbasin48] = readHydroRunTime_fromtxt('../PlotData/subbasin48.log')



[Speedup_De10Tile20, E_Land_De10Tile20] = readLandRunTime_fromtxt('../PlotData/De10Tile20.log')
[Speedup_De10Tile48, E_Land_De10Tile48] = readLandRunTime_fromtxt('../PlotData/De10Tile48.log')
[Speedup_De10Tile96, E_Land_De10Tile96] = readLandRunTime_fromtxt('../PlotData/De10Tile96.log')
[Speedup_De10Tile144, E_Land_De10Tile144] = readLandRunTime_fromtxt('../PlotData/De10Tile144.log')


[Speedup_De50Tile20, E_Land_De50Tile20] = readLandRunTime_fromtxt('../PlotData/De50Tile20.log')
[Speedup_De50Tile48, E_Land_De50Tile48] = readLandRunTime_fromtxt('../PlotData/De50Tile48.log')
[Speedup_De50Tile96, E_Land_De50Tile96] = readLandRunTime_fromtxt('../PlotData/De50Tile96.log')
[Speedup_De50Tile144, E_Land_De50Tile144] = readLandRunTime_fromtxt('../PlotData/De50Tile144.log')





# plot the hydrological parallel

plt.style.use("seaborn")
fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, sharex=False, figsize=(7, 9))


ax1.plot(CoreNum, Speedup_Subbasin6, color="k", linewidth = 2, 
         linestyle='-', marker='.', label="$N_{sub}=6$", alpha=0.25)

ax1.plot(CoreNum, Speedup_Subbasin12, color="k", linewidth = 2, 
         linestyle='-', marker='.', label="$N_{sub}=12$", alpha=0.5)

ax1.plot(CoreNum, Speedup_Subbasin24, color="k", linewidth = 2, 
          linestyle='-', marker='.', label="$N_{sub}=24$", alpha=0.75)


ax1.plot(CoreNum, Speedup_Subbasin48, color="k", linewidth = 2, 
         linestyle='-', marker='.', label="$N_{sub}=48$", alpha=1)


ax1.set_xlim([0, 49])
ax1.set_xticks([1, 8, 16, 24, 32, 40, 48])
ax1.set_xticklabels([1, 8, 16, 24, 32, 40, 48], fontsize=15)
ax1.set_xlabel('Number of processes (-)', fontsize=15)


ax1.set_ylim([0.9, 9])
ax1.set_yticks([1, 3, 5, 7, 9])
ax1.set_yticklabels([1, 3, 5, 7, 9], fontsize=15)
ax1.text(1, 8, "(a)", fontsize=15, weight = "light", color = "k")
ax1.set_ylabel('Speedup (-)', fontsize=15)

ax1.legend(loc = 1, prop=font_legend, edgecolor="k", ncol=1, 
           handletextpad = 0.3, bbox_to_anchor=(0.58, 1.05))



ax2.plot(CoreNum, E_Hydro_Subbasin6, color="black", linewidth = 2, 
         linestyle='-', marker='.', label="$N_{sub}=6$", alpha=0.25)

ax2.plot(CoreNum, E_Hydro_Subbasin12, color="black", linewidth = 2, 
          linestyle='-', marker='.', label="$N_{sub}=12$", alpha=0.5)

ax2.plot(CoreNum, E_Hydro_Subbasin24, color="black", linewidth = 2, 
          linestyle='-', marker='.', label="$N_{sub}=24$", alpha=0.75)


ax2.plot(CoreNum, E_Hydro_Subbasin48, color="black", linewidth = 2, 
          linestyle='-', marker='.', label="$N_{sub}=48$", alpha=1)

ax2.set_xlim([0, 49])
ax2.set_xticks([1, 8, 16, 24, 32, 40, 48])
ax2.set_xticklabels([1, 8, 16, 24, 32, 40, 48], fontsize=15)
ax2.set_xlabel('Number of processes (-)', fontsize=15)


ax2.set_ylim([0, 1])
ax2.set_yticks([0.2, 0.4, 0.6, 0.8, 1])
ax2.set_yticklabels([0.2, 0.4, 0.6, 0.8, 1], fontsize=15)
ax2.text(40, 0.88, "(b)", fontsize=15, weight = "light", color = "k")
ax2.set_ylabel('Efficiency (-)', fontsize=15)


# ax2.legend(loc = 1, prop=font_legend, edgecolor="k", ncol=1, 
#             handletextpad = 0.3, bbox_to_anchor=(0.58, 1.05))




ax3.plot(CoreNum, Speedup_De10Tile20, color="black", linewidth = 2, 
         linestyle='-', marker='.', label="$N_{tile}=20$", alpha=0.25)

ax3.plot(CoreNum, Speedup_De10Tile48, color="black", linewidth = 2, 
         linestyle='-', marker='.', label="$N_{tile}=48$", alpha=0.5)


ax3.plot(CoreNum, Speedup_De10Tile96, color="black", linewidth = 2, 
         linestyle='-', marker='.', label="$N_{tile}=96$", alpha=0.75)

ax3.plot(CoreNum, Speedup_De10Tile144, color="black", linewidth = 2, 
         linestyle='-', marker='.', label="$N_{tile}=144$", alpha=1)


ax3.set_xlim([0, 49])
ax3.set_xticks([1, 8, 16, 24, 32, 40, 48])
ax3.set_xticklabels([1, 8, 16, 24, 32, 40, 48], fontsize=15)
ax3.set_xlabel('Number of processes (-)', fontsize=15)


ax3.set_ylim([0, 35])
ax3.set_yticks([1, 10, 20, 30])
ax3.set_yticklabels([1, 10, 20, 30], fontsize=15)
ax3.text(1, 30, "(c)", fontsize=15, weight = "light", color = "k")
ax3.set_ylabel('Speedup (-)', fontsize=15)

ax3.legend(loc = 1, prop=font_legend, edgecolor="k", ncol=1, 
           handletextpad = 0.3, bbox_to_anchor=(0.58, 1.05))


ax3.text(32, 3, "$D_{e}=10$", fontsize=14, weight = "light", color = "k")





ax4.plot(CoreNum, E_Land_De10Tile20, color="black", linewidth = 2, 
         linestyle='-', marker='.', label="$N_{tile}=20$", alpha=0.25)

ax4.plot(CoreNum, E_Land_De10Tile48, color="black", linewidth = 2, 
          linestyle='-', marker='.', label="$N_{tile}=48$", alpha=0.5)

ax4.plot(CoreNum, E_Land_De10Tile96, color="black", linewidth = 2, 
          linestyle='-', marker='.', label="$N_{tile}=96$", alpha=0.75)


ax4.plot(CoreNum, E_Land_De10Tile144, color="black", linewidth = 2, 
          linestyle='-', marker='.', label="$N_{tile}=144$", alpha=1)

# ax4.legend(loc = 1, prop=font_legend, edgecolor="k", ncol=1, 
#             handletextpad = 0.3, bbox_to_anchor=(0.5, 0.5))


ax4.text(32, 0.06, "$D_{e}=10$", fontsize=14, weight = "light", color = "k")




ax4.set_xlim([0, 49])
ax4.set_xticks([1, 8, 16, 24, 32, 40, 48])
ax4.set_xticklabels([1, 8, 16, 24, 32, 40, 48], fontsize=15)
ax4.set_xlabel('Number of processes (-)', fontsize=15)


ax4.set_ylim([0, 1])
ax4.set_yticks([0.2, 0.4, 0.6, 0.8, 1])
ax4.set_yticklabels([0.2, 0.4, 0.6, 0.8, 1], fontsize=15)
ax4.text(40, 0.85, "(d)", fontsize=15, weight = "light", color = "k")


ax4.set_ylabel('Efficiency (-)', fontsize=15)







ax5.plot(CoreNum, Speedup_De50Tile20, color="black", linewidth = 2, 
         linestyle='-', marker='.', label="$N_{tile}=20$", alpha=0.25)


ax5.plot(CoreNum, Speedup_De50Tile48, color="black", linewidth = 2, 
         linestyle='-', marker='.', label="$N_{tile}=48$", alpha=0.5)
ax5.plot(CoreNum, Speedup_De50Tile96, color="black", linewidth = 2, 
         linestyle='-', marker='.', label="$N_{tile}=96$", alpha=0.75)

ax5.plot(CoreNum, Speedup_De50Tile144, color="black", linewidth = 2, 
         linestyle='-', marker='.', label="$N_{tile}=144$", alpha=1)


ax5.set_xlim([0, 49])
ax5.set_xticks([1, 8, 16, 24, 32, 40, 48])
ax5.set_xticklabels([1, 8, 16, 24, 32, 40, 48], fontsize=15)
ax5.set_xlabel('Number of processes (-)', fontsize=15)


ax5.set_ylim([0, 35])
ax5.set_yticks([1, 10, 20, 30])
ax5.set_yticklabels([1, 10, 20, 30], fontsize=15)
ax5.text(1, 30, "(e)", fontsize=15, weight = "light", color = "k")
ax5.set_ylabel('Speedup (-)', fontsize=15)

ax5.legend(loc = 1, prop=font_legend, edgecolor="k", ncol=1, 
           handletextpad = 0.3, bbox_to_anchor=(0.58, 1.05))


ax5.text(32, 3, "$D_{e}=50$", fontsize=14, weight = "light", color = "k")






ax6.plot(CoreNum, E_Land_De50Tile20, color="black", linewidth = 2, 
         linestyle='-', marker='.', label="$N_{tile}=20$", alpha=0.25)

ax6.plot(CoreNum, E_Land_De50Tile48, color="black", linewidth = 2, 
          linestyle='-', marker='.', label="$N_{tile}=48$", alpha=0.5)

ax6.plot(CoreNum, E_Land_De50Tile96, color="black", linewidth = 2, 
          linestyle='-', marker='.', label="$N_{tile}=96$", alpha=0.75)


ax6.plot(CoreNum, E_Land_De50Tile144, color="black", linewidth = 2, 
          linestyle='-', marker='.', label="$N_{tile}=144$", alpha=1)

# ax6.legend(loc = 1, prop=font_legend, edgecolor="k", ncol=1, 
#             handletextpad = 0.3, bbox_to_anchor=(0.5, 0.5))

ax6.set_xlim([0, 49])
ax6.set_xticks([1, 8, 16, 24, 32, 40, 48])
ax6.set_xticklabels([1, 8, 16, 24, 32, 40, 48], fontsize=15)
ax6.set_xlabel('Number of processes (-)', fontsize=15)


ax6.set_ylim([0, 1])
ax6.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
ax6.set_yticklabels([0, 0.2, 0.4, 0.6, 0.8, 1], fontsize=15)
ax6.text(40, 0.85, "(f)", fontsize=15, weight = "light", color = "k")
ax6.text(32, 0.06, "$D_{e}=50$", fontsize=14, weight = "light", color = "k")

ax6.set_ylabel('Efficiency (-)', fontsize=15)





plt.tight_layout()

# plt.savefig("Runtime_test.jpg", dpi = 400)













