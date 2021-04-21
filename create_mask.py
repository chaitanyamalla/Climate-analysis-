#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################################

#!/usr/bin/env python
from __future__ import print_function
import numpy as np
import ufz   as ufz
# uses package in_poly from ufz library
from pyproj import Proj,transform
import optparse

# ---------------------------------------------------------------------
# --------------------parse Arguments ---------------------------------

parser = optparse.OptionParser(
    usage='%prog -s [shapefile] -o [outfile] -l [latlon] -m [mask]' ,
    description="Mask creation."
)
parser.add_option(
    '-s', '--shape_file', action='store', dest='shape_file', type=str,
    help='shapefile name.'
)
parser.add_option(
    '-o', '--outname', action='store', dest='outname', type=str,
    help='Name of the outputfile.'
)

parser.add_option(
    '-l', '--latlon', action='store', dest='latlon_file', type=str,
    help='nc file with latlon variables.'
)
parser.add_option(
    '-m', '--mask', action='store', dest='mask', type=str,
    help='mask of model domain.'
)
(opts, args) = parser.parse_args()
shape_file   = opts.shape_file
outname  = opts.outname
latlon_file   = opts.latlon_file
mask_modeldomain_file = opts.mask
### load point raster ###########################################################################


# read latitude and longitude
# file containing latitude and longitude grid
# latlon_file   = '/data/hicam/data/processed/mhm_input/de_hicam/latlon/latlon_0p015625.nc'

lons          = ufz.readnc(latlon_file, var='lon') 
lats          = ufz.readnc(latlon_file, var='lat')
cellsize      = 0.015625
th            = cellsize *2
#europe_mask   = ufz.readnc(latlon_file, var='mask')
y_len = lons.shape[0]
x_len = lons.shape[1]

# mask_modeldomain_file   = '/data/hicam/data/processed/dem_OR/mask_hicam_1km_ghw_inv.nc'
mask_domain          = ufz.readnc(mask_modeldomain_file, var='mask')

# latlon_file_GDM   = '/home/boeing/GDM/mask_ger_gdm/latlon_4000.nc'
# lons_GDM          = ufz.readnc(latlon_file_GDM, var='lon') 
# lats_GDM          = ufz.readnc(latlon_file_GDM, var='lat')
# x1, y1 = lats_GDM[0,0], lons_GDM[0,0]
# x2, y2 = lats_GDM[-1,-1], lons_GDM[-1,-1] 

# #epsg_31468= Proj("+proj=tmerc +lat_0=0 +lon_0=12 +k=1 +x_0=4500000 +y_0=0 +ellps=bessel +datum=potsdam +units=m +no_defs")

# inProj = Proj(init='epsg:31468')
# outProj = Proj(init='epsg:4326')

# x1_proj,y1_proj = transform(inProj,outProj,inProj(x1,y1)[0],inProj(x1,y1)[1])
# x2_proj,y2_proj = transform(inProj,outProj,inProj(x2,y2)[0],inProj(x2,y2)[1])



# length 950  -y
# length 1000 -x


############## load shapefiles ##################################################################
# load package for shapefiles
import cartopy.io.shapereader as shpreader
import shapefile

# read shapefile of federal states: 
# shapefile = './WA_Versorgungsgebiet_epsg4326.shp'
# shapefile = './Abfragerahmen33N_epsg4326.shp'
# outname="versorgungsgebiet"
# outname="untersuchungsgebiet"
reader    = shpreader.Reader(shape_file)
reader_shapefile = shapefile.Reader(shape_file)


geomet_fedstates = reader.records() #will store the geometry separately

# check epsg

#bw = geomet_fedstates[0] #will extract the first polygon to a new object
#first.shape.points #will show you the points of the polygon
#first.record #will show you the attributes

##### extracting the federal state names #######################################################
namelist = []
for k in geomet_fedstates: 
    #print(k.attributes["NUTS"][2]) 
    k_att = k.attributes 
    namelist.append(k_att)


name_att=[]
for c, value in enumerate(namelist, 1):
    name_att.append("{:}: {:}".format(c, value))



#################################################################################################



# create solution matrix:

erg    = np.zeros((y_len,x_len))
#erg[:] = -9999


##### in_poly for Loop ###########################################################################

print('in_poly calculating')


for k in range(0,len(reader_shapefile.shapes())):

    #shapedata = geomet_fedstates[k] # loop over selection of federal states
    shapedata = reader_shapefile.shapes()[k]
    # selects the greatest distance within the polygon to avoid cutting out parts of the polygon (...island e.g. Berlin inside Brandenburg)
    parts_array = np.append(shapedata.parts,len(shapedata.points))
    parts_diff = np.zeros((len(parts_array)-1))
    for x in range(0, (len(parts_array) -1)):
        diff = parts_array[x+1] - parts_array[x]
        parts_diff[x] = diff
        print(x)
    location = np.where(parts_diff == np.max(parts_diff))
    part_min = parts_array[location[0]]
    part_max = parts_array[location[0] + 1]

    #print(k)
    #print(part_min)
    #print(part_max)

    #shapedata.shape.parts # groesster Abstand
    # [354:2090]
    # 
    #coord_lons = np.array(shapedata.shape.points)[part_min[0]:part_max[0],0] # lons - Längenkreise
    #coord_lats = np.array(shapedata.shape.points)[part_min[0]:part_max[0],1] # lats - Breitenkreise

    for i in range(0,len(parts_array)-1):
        #print(parts_array[i])
        #print(parts_array[i+1])
        coord_lons = np.array(shapedata.points)[parts_array[i]:parts_array[i+1],0] # lons - Längenkreise
        coord_lats = np.array(shapedata.points)[parts_array[i]:parts_array[i+1],1] # lats - Breitenkreise
        # shapedata.shape.parts[0]:shapedata.shape.parts[-1]
        x_range=np.where((lons[0,:] > coord_lons.min() - th) & (lons[0,:] < coord_lons.max() +th))[0]
        y_range=np.where((lats[:,0] > coord_lats.min() - th) & (lats[:,0] < coord_lats.max() +th))[0]
        coord_range=[coord_lons.min() - th,coord_lons.max() +th,coord_lats.min() - th,coord_lats.max() +th]
        table_file="extent_{:}".format(outname)
        th = open(table_file, 'w')

        th.write('lon_min, lon_max, lat_min, lat_max \n')
        th.write(','.join(map(str,coord_range)))
        th.close()
        # for i in range(y_len): # range(ymin, ymax):
        #     for j in range(x_len): # range(xmin, xmax):
        for i in y_range: # range(ymin, ymax):
            for j in x_range: # range(xmin, xmax):
                # if np.logical_or(lons[i,j] < coord_lons.min()-th, lons[i,j] > coord_lons.max()+th):
                #     continue
                # if np.logical_or(lats[i,j] < coord_lats.min()-th, lats[i,j] > coord_lats.max()+th):
                #     continue
                # print(i, j)
            
                value_1 = ufz.in_poly([lons[i,j]-cellsize/2, lats[i,j]-cellsize/2], coord_lons, coord_lats)
                value_2 = ufz.in_poly([lons[i,j]+cellsize/2, lats[i,j]+cellsize/2], coord_lons, coord_lats)
                value_3 = ufz.in_poly([lons[i,j]-cellsize/2, lats[i,j]+cellsize/2], coord_lons, coord_lats)
                value_4 = ufz.in_poly([lons[i,j]+cellsize/2, lats[i,j]-cellsize/2], coord_lons, coord_lats)
                # if clause to create unique values for each shape data
                values=[value_1,value_2,value_3,value_4]
                if 0 or 1 in values:     # 0 or 1 means point is in polygon
                    # print(i)
                    if mask_domain[i,j] == 1: # has to be inside model domain
                        erg[i,j] = 1    # assigns number k+ 1 to each federal state 
                # print("main extraction done.")
                # print("..testing now for parts where the only edges of gridcells to not ly in polygon.")
                for x,y in zip(coord_lons,coord_lats):
                    value = ufz.in_poly([x,y],np.array([lons[i,j]-cellsize/2,lons[i,j]-cellsize/2,lons[i,j]+cellsize/2,lons[i,j]+cellsize/2]),
                                              np.array([lats[i,j]-cellsize/2,lats[i,j]+cellsize/2,lats[i,j]+cellsize/2,lats[i,j]-cellsize/2]))
                    # print(value)
                    if value == 1 or value == 0:     # 0 or 1 means point is in polygon
                        print(i,j)
                        if mask_domain[i,j] == 1: # has to be inside model domain
                            erg[i,j] = 1    # assigns number k+ 1 to each federal state 

##### write in netcdf data ######################################################################

from ufz import netcdf4 as nc
outputfile="mask_{:}.nc".format(outname)
with nc.NcDataset(outputfile, "w") as nc:
    nc.createDimension("y",  y_len)
    nc.createDimension("x", x_len)

    # add metadata:
    nc.createAttributes({"contact": "Friedrich Boeing",
                         })
    var = nc.createVariable("mask", "f8", ("y","x")) # f8 defines data type float
    var[:] = erg
    var = nc.createVariable("lons", "f8", ("y","x")) # f8 defines data type float
    var[:] = lons
    var = nc.createVariable("lats", "f8", ("y","x")) # f8 defines data type float
    var[:] = lats



