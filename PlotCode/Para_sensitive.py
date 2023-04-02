#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 23:16:47 2022

@author: guoding_chen
"""

# this program is used to plot the sensitivity analysis


import numpy as np
import re
import matplotlib as mpl
mpl.use('Qt5Agg')
import matplotlib.pyplot as plt

font_legend={'family':'Arial',
     'style':'normal',
    'weight':'normal',
     'size':10}


# define the function that detect the character in a text file
def readvalue_fromtxt(file_path, symbol):
    file = open(file_path,'r')
    contents = file.readlines()
    
    value_str = [s for s in contents if symbol in s]
    
    # get the line number index of the string
    value_index = [contents.index(s) for s in contents if symbol in s]
    
    Runoff_total = []
    Unstale_area = []
    for line_index in value_index:
        
        
        Runoff_total.append(contents[line_index + 8].split(':', 1)[1])
        Unstale_area.append(contents[line_index + 2].split(':', 1)[1])
        
    Runoff_total = [float(x) for x in np.array(Runoff_total)]
    Unstale_area = [float(x) for x in np.array(Unstale_area)]
    
    # split each element in list and keep second part
    value_num = [item.split('=', 1)[1] for item in value_str]
    
    #value_str = [re.findall( r'\d+\.*\d*', s ) for s in value_str]
    value = [float(x) for x in np.array(value_num)]

    return value, Runoff_total, Unstale_area



# function for sensitive index
def sensitive_index(Various_Para, Various_output):
    S = []
    for i in range(1, len(Various_Para)-1):
        S_i = (Various_output[i+1] -  Various_output[i-1]) / \
                    (Various_Para[i+1] -  Various_Para[i-1]) \
                        * (Various_Para[i] / Various_output[i])
        S.append(abs(S_i))
        
                
    return sum(S) / len(S)




file_path = '../PlotData/sensitive_test.log'

# read the paramters sensitivity test results

# B
[B_value, B_Runoff_total, B_Unstale_area] = \
                    readvalue_fromtxt(file_path, "B =")

S_B_hydro = sensitive_index(B_value, B_Runoff_total)
S_B_land = sensitive_index(B_value, B_Unstale_area)

#  coeM
[coeM_value, coeM_Runoff_total, coeM_Unstale_area] = \
                    readvalue_fromtxt(file_path, "coeM =")

S_coeM_hydro = sensitive_index(coeM_value, coeM_Runoff_total)
S_coeM_land = sensitive_index(coeM_value, coeM_Unstale_area)

#  expM
[expM_value, expM_Runoff_total, expM_Unstale_area] = \
                    readvalue_fromtxt(file_path, "expM =")

S_expM_hydro = sensitive_index(expM_value, expM_Runoff_total)
S_expM_land = sensitive_index(expM_value, expM_Unstale_area)

# coeR

[coeR_value, coeR_Runoff_total, coeR_Unstale_area] = \
                    readvalue_fromtxt(file_path, "coeR =")

S_coeR_hydro = sensitive_index(coeR_value, coeR_Runoff_total)
S_coeR_land = sensitive_index(coeR_value, coeR_Unstale_area)


# coeS

[coeS_value, coeS_Runoff_total, coeS_Unstale_area] = \
                    readvalue_fromtxt(file_path, "coeS =")

S_coeS_hydro = sensitive_index(coeS_value, coeS_Runoff_total)
S_coeS_land = sensitive_index(coeS_value, coeS_Unstale_area)



# KS

[KS_value, KS_Runoff_total, KS_Unstale_area] = \
                    readvalue_fromtxt(file_path, "KS =")

S_KS_hydro = sensitive_index(KS_value, KS_Runoff_total)
S_KS_land = sensitive_index(KS_value, KS_Unstale_area)

# KI

[KI_value, KI_Runoff_total, KI_Unstale_area] = \
                    readvalue_fromtxt(file_path, "KI =")

S_KI_hydro = sensitive_index(KI_value, KI_Runoff_total)
S_KI_land = sensitive_index(KI_value, KI_Unstale_area)

# De

[De_value, De_Runoff_total, De_Unstale_area] = \
                    readvalue_fromtxt(file_path, "De =")

S_De_hydro = sensitive_index(De_value, De_Runoff_total)
S_De_land = sensitive_index(De_value, De_Unstale_area)


Sindex_hydro = [S_B_hydro, S_coeM_hydro, S_expM_hydro, S_coeR_hydro,
                S_coeS_hydro, S_KS_hydro, S_KI_hydro, S_De_hydro]

Sindex_land = [S_B_land, S_coeM_land, S_expM_land, S_coeR_land,
                S_coeS_land, S_KS_land, S_KI_land, S_De_land]


Para = ('$B$', '$coeM$', '$expM$', '$coeR$', '$coeS$', '$KS$', '$KI$', '$De$')

y_pos = np.arange(len(Para))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))




ax1.barh(y_pos, Sindex_hydro)

ax1.invert_yaxis()  # labels read top-to-bottom

ax1.set_yticks(y_pos, labels = Para, fontsize=15)

ax1.set_xlim([0,0.5])
ax1.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
ax1.set_xticklabels([0, 0.1, 0.2, 0.3, 0.4, 0.5], fontsize=15)

ax1.set_xlabel("$S_{I}$", fontsize=15)

ax1.set_title("(a) Total runoff volume at the outlet", fontsize=15)



ax2.barh(y_pos, Sindex_land)

ax2.invert_yaxis()  # labels read top-to-bottom

ax2.set_yticks(y_pos, labels = Para, fontsize=15)


ax2.set_xlim([0,0.15])
ax2.set_xticks([0, 0.03, 0.06, 0.09, 0.12, 0.15])
ax2.set_xticklabels([0, 0.03, 0.06, 0.09, 0.12, 0.15], fontsize=15)

ax2.set_xlabel("$S_{I}$", fontsize=15)
ax2.set_title("(b) Regional unstable area", fontsize=15)

plt.tight_layout()
plt.show()






