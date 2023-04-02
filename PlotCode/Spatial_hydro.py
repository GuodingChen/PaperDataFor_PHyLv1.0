#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 15:08:15 2022

@author: Guoding_Chen
this program is used to plot all the matrix 


"""


import cv2
import numpy as np
import re
import h5py
import matplotlib
import matplotlib as mpl
import shapefile as shp
from matplotlib import colors
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import os
import glob
font1={'family':'Arial',
     'style':'normal',
    'weight':'normal',
     'size':14}
font_xylable={'family':'Arial',
     'style':'normal',
    'weight':'normal',
     'size':40}
font_legend={'family':'Arial',       
     'style':'normal',
    'weight':'normal',
     'size':12}



# ----------------------------------start to plot figure----------------------
variable_list = ["R", "W","SM", "FS3D", "PF", "FVolume"]

# read the necessary information from the control file
Control_file = open('../PlotData/Control.Project','r')

ControlFile_contents = Control_file.readlines()

# identify the boundary information for hydrology
XLLCorner_line_hydro = re.sub(r'\s+', '', [s for s in ControlFile_contents if "XLLCorner_Hydro" in s][0])
XLLCorner_hydro = XLLCorner_line_hydro.split("#",1)[0]
XLLCorner_hydro = float(XLLCorner_hydro.split("=",1)[1])

YLLCorner_line_hydro = re.sub(r'\s+', '', [s for s in ControlFile_contents if "YLLCorner_Hydro" in s][0])
YLLCorner_hydro = YLLCorner_line_hydro.split("#",1)[0]
YLLCorner_hydro = float(YLLCorner_hydro.split("=",1)[1])

nCols_line_hydro = re.sub(r'\s+', '', [s for s in ControlFile_contents if "NCols_Hydro" in s][0])
nCols_hydro = nCols_line_hydro.split("#",1)[0]
nCols_hydro = float(nCols_hydro.split("=",1)[1])

nRows_line_hydro = re.sub(r'\s+', '', [s for s in ControlFile_contents if "NRows_Hydro" in s][0])
nRows_hydro = nRows_line_hydro.split("#",1)[0]
nRows_hydro = float(nRows_hydro.split("=",1)[1])

cellSize_line_hydro = re.sub(r'\s+', '', [s for s in ControlFile_contents if "CellSize_Hydro" in s][0])
cellSize_hydro = cellSize_line_hydro.split("#",1)[0]
cellSize_hydro = float(cellSize_hydro.split("=",1)[1])


# identify the boundary information for landslide
XLLCorner_line_land = re.sub(r'\s+', '', [s for s in ControlFile_contents if "XLLCorner_Land" in s][0])
XLLCorner_land = XLLCorner_line_land.split("#",1)[0]
XLLCorner_land = float(XLLCorner_land.split("=",1)[1])

YLLCorner_line_land = re.sub(r'\s+', '', [s for s in ControlFile_contents if "YLLCorner_Land" in s][0])
YLLCorner_land = YLLCorner_line_land.split("#",1)[0]
YLLCorner_land = float(YLLCorner_land.split("=",1)[1])

nCols_line_land = re.sub(r'\s+', '', [s for s in ControlFile_contents if "NCols_Land" in s][0])
nCols_land = nCols_line_land.split("#",1)[0]
nCols_land = float(nCols_land.split("=",1)[1])

nRows_line_land = re.sub(r'\s+', '', [s for s in ControlFile_contents if "NRows_Land" in s][0])
nRows_land = nRows_line_land.split("#",1)[0]
nRows_land = float(nRows_land.split("=",1)[1])

cellSize_line_land = re.sub(r'\s+', '', [s for s in ControlFile_contents if "CellSize_Land" in s][0])
cellSize_land = cellSize_line_land.split("#",1)[0]
cellSize_land = float(cellSize_land.split("=",1)[1])



# creat the extent for hydrological variables
extent_hydro = [XLLCorner_hydro, XLLCorner_hydro + nCols_hydro * cellSize_hydro,
                YLLCorner_hydro, YLLCorner_hydro + nRows_hydro * cellSize_hydro]

# creat the extent for landslide variables
extent_land = [XLLCorner_land, XLLCorner_land + nCols_land * cellSize_land,
                YLLCorner_land, YLLCorner_land + nRows_land * cellSize_land]



# read the boundary shp file
Boundary_shpfile = "../PlotData/Basin_boundary.shp"
sf = shp.Reader(Boundary_shpfile)
for shape in sf.shapeRecords():
    x = np.array([i[0] for i in shape.shape.points[:]])
    y = np.array([i[1] for i in shape.shape.points[:]])



NODATA_value = -9999

# prepare the colorbar
colorbar_R = 'YlGnBu'
colorbar_W = plt.get_cmap('GnBu', 8) 
colorbar_SM = plt.get_cmap('YlGnBu', 8) 




TimeList = ["2012070400", "2012070403", "2012070406", "2012070412", "2012070500"]


figure, axis = plt.subplots(3, 5, figsize=(12, 8))

# plt.subplots_adjust(top = 0.99, bottom=0.01, hspace=0.05, wspace=0.1)

plt.subplots_adjust(bottom=0.0, top=0.98,left = 0.01, right=0.9, hspace=0.01, wspace=0.1)

# read the HDF5 file name
filename = '../PlotData/Spatial_plot.h5'
data = h5py.File(filename, 'r')
for group in data.keys() :
    
    for dset in data[group].keys():      
        ds_data = data[group][dset] # returns HDF5 dataset object
        
        variable_tag = dset.split("_",2)[1]
        Time_moment = dset.split("_",2)[2]
        
        if variable_tag in variable_list :
            variable_matrix = data[group][dset][:] # adding [:] returns a numpy array
            variable_matrix = variable_matrix.astype(np.float32)
            variable_matrix[variable_matrix == NODATA_value] = np.nan
            # Convert scaled integer back to floating point
            variable_matrix = variable_matrix / 100
            # start to plot the figure
            
            if variable_tag == "R":
                variable_matrix[variable_matrix == 0] = 0.000001
                if Time_moment in TimeList :
                    column_place = TimeList.index(Time_moment)
                else:
                    continue

                im = axis[0, column_place].imshow(variable_matrix, extent = extent_hydro,
                            cmap = colorbar_R, norm = colors.LogNorm(vmin=10**-1, vmax=10**3))

                axis[0, column_place].plot(x, y, 'k', linewidth = 1)

                axis[0, column_place].set_xlim([XLLCorner_hydro+0.02, XLLCorner_hydro + nCols_hydro * cellSize_hydro-0.05])
                axis[0, column_place].set_ylim([YLLCorner_hydro+0.02, YLLCorner_hydro + nRows_hydro * cellSize_hydro-0.03])
                
                axis[0, column_place].set_xticks([108.4, 108.6])
                axis[0, column_place].set_xticklabels([108.4, 108.6], fontsize=7)
                
                axis[0, column_place].set_yticks([32.8, 33.0])
                axis[0, column_place].set_yticklabels([32.8, 33.0], fontsize=7)
                
                axis[0, column_place].axis('on')
                axis[0, column_place].grid(linestyle='--', linewidth = 0.5)
                axis[0, column_place].tick_params(axis="y",direction="in", pad=-20)
                axis[0, column_place].tick_params(axis="x",direction="in", pad=-10)
                # axis[0, column_place].set_xticks([])
                # axis[0, column_place].set_yticks([])
                
                if column_place == 4:
                    cbar_ax = figure.add_axes([0.93, 0.69, 0.015, 0.23])
                    cbar_ax.tick_params(labelsize=13)
                    cb = plt.colorbar(im, cax=cbar_ax)
                    cb.set_label('R ($\mathrm{m^3/s}$)', fontdict = font1, 
                                 rotation=0, labelpad=-35, y=1.20)


            if variable_tag == "W":
                
                if Time_moment in TimeList :
                    column_place = TimeList.index(Time_moment)
                else:
                    continue

                im = axis[1, column_place].imshow(variable_matrix, extent = extent_hydro,
                            cmap = colorbar_W, vmin = 0, vmax = 150)

                axis[1, column_place].plot(x, y, 'k', linewidth = 1)

                axis[1, column_place].set_xlim([XLLCorner_hydro+0.02, XLLCorner_hydro + nCols_hydro * cellSize_hydro-0.05])
                axis[1, column_place].set_ylim([YLLCorner_hydro+0.02, YLLCorner_hydro + nRows_hydro * cellSize_hydro-0.03])
                
                axis[1, column_place].set_xticks([108.4, 108.6])
                axis[1, column_place].set_xticklabels([108.4, 108.6], fontsize=7)
                
                axis[1, column_place].set_yticks([32.8, 33.0])
                axis[1, column_place].set_yticklabels([32.8, 33.0], fontsize=7)
                
                axis[1, column_place].axis('on')
                axis[1, column_place].grid(linestyle='--', linewidth = 0.5)
                axis[1, column_place].tick_params(axis="y",direction="in", pad=-20)
                axis[1, column_place].tick_params(axis="x",direction="in", pad=-10)
                
                if column_place == 4:
                    cbar_ax = figure.add_axes([0.93, 0.35, 0.015, 0.23])
                    cbar_ax.tick_params(labelsize=13)
                    cb = plt.colorbar(im, cax=cbar_ax)
                    cb.set_label('W ($\mathrm{mm}$)', fontdict = font1, 
                                 rotation=0, labelpad=-30, y=1.20)
                    cb.set_ticks([0,25,50,75,100,125,150])
                    
            if variable_tag == "SM":
                
                if Time_moment in TimeList :
                    column_place = TimeList.index(Time_moment)
                else:
                    continue

                


                im = axis[2, column_place].imshow(variable_matrix, extent = extent_hydro,
                            cmap=colorbar_SM, vmin = 0, vmax = 100)

                axis[2, column_place].plot(x, y, 'k', linewidth = 1)

                axis[2, column_place].set_xlim([XLLCorner_hydro+0.02, XLLCorner_hydro + nCols_hydro * cellSize_hydro-0.05])
                axis[2, column_place].set_ylim([YLLCorner_hydro+0.02, YLLCorner_hydro + nRows_hydro * cellSize_hydro-0.03])
                
                axis[2, column_place].set_xticks([108.4, 108.6])
                axis[2, column_place].set_xticklabels([108.4, 108.6], fontsize=7)
                
                axis[2, column_place].set_yticks([32.8, 33.0])
                axis[2, column_place].set_yticklabels([32.8, 33.0], fontsize=7)
                
                axis[2, column_place].axis('on')
                axis[2, column_place].grid(linestyle='--', linewidth = 0.5)
                axis[2, column_place].tick_params(axis="y",direction="in", pad=-20)
                axis[2, column_place].tick_params(axis="x",direction="in", pad=-10)
 
                if column_place == 4:
                    cbar_ax = figure.add_axes([0.93, 0.03, 0.015, 0.23])
                    cbar_ax.tick_params(labelsize=13)
                    cb = plt.colorbar(im, cax=cbar_ax)
                    cb.set_label('SM ($\%$)', fontdict = font1, 
                                 rotation=0, labelpad=-30, y=1.20)
                
        else:
            break   

axis[0, 0].text(108.47, 33.18, "2012070400", fontsize=12, 
                weight = "light", color = "k")

axis[0, 1].text(108.47, 33.18, "2012070403", fontsize=12, 
                weight = "light", color = "k")
axis[0, 2].text(108.47, 33.18, "2012070406", fontsize=12, 
                weight = "light", color = "k") 

axis[0, 3].text(108.47, 33.18, "2012070412", fontsize=12, 
                weight = "light", color = "k")
axis[0, 4].text(108.47, 33.18, "2012070500", fontsize=12, 
                weight = "light", color = "k")


data.close()

plt.show()

# plt.savefig("spatial_hydro.jpg" , dpi = 600)
# plt.close()  
print ('successfully plot ')
