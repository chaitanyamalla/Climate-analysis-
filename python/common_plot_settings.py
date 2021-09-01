#!/usr/bin/env python

import pandas as pd
import numpy as np
from ufz import fread,readnc, position, get_brewer, abc2plot, astr  #dumpnetcdf, 
#  COMMAND LINE ARGUMENTS ###################
pdffile  = ''
pngbase  = ''
eval_period= ''
ncvarname=''
var_type=''
mask_region=''
import optparse
parser  = optparse.OptionParser(usage='%prog [options]',
                               description="Plotting of SMI for drought monitor.")
parser.add_option('-p', '--pdffile', action='store', dest='pdffile', type='string',
                  default=pdffile, metavar='File',
                  help='Name of pdf output file (default: open X-window).')
parser.add_option('-g', '--pngbase', action='store',
                    default=pngbase, dest='pngbase', metavar='pngbase',
                    help='Name basis for png output files (default: open screen window).')
parser.add_option('-e', '--eval_period', action='store',
                    default=eval_period, dest='eval_period', metavar='eval_period',
                    help='evaluation period (spring, winter, summer, autumn, fullyears)')
parser.add_option('-v', '--ncvarname', action='store',
                    default=ncvarname, dest='ncvarname', metavar='ncvarname',
                    help='evaluation period (spring, winter, summer, autumn, fullyears)')
parser.add_option('-t', '--var_type', action='store',
                    default=var_type, dest='var_type', metavar='var_type',
                    help='evaluation period (spring, winter, summer, autumn, fullyears)')
parser.add_option('-r', '--eval_rcp', action='store',
                    default=ncvarname, dest='eval_rcp', metavar='eval_rcp',
                    help='type of indicator')
parser.add_option('-i', '--indicator', action='store',
                    default=ncvarname, dest='indicator', metavar='indicator',
                    help='type of indicator')
parser.add_option('-m', '--mask_region', action='store',
                    default=ncvarname, dest='mask_region', metavar='mask_region',
                    help='mask of region.')

(opts, args) = parser.parse_args()

pdffile     = opts.pdffile
pngbase     = opts.pngbase
eval_period = opts.eval_period
eval_rcp    = opts.eval_rcp
ncvarname   = opts.ncvarname
var_type    = opts.var_type
indicator   = opts.indicator
mask_region        = opts.mask_region
del parser, opts, args

if (pdffile != '') & (pngbase != ''):
    raise ValueError('PDF and PNG are mutually exclusive. Only either -p or -g possible.')

if (pdffile == ''):
    if (pngbase == ''):
        outtype = 'x'
    else:
        outtype = 'png'
else:
    outtype = 'pdf'
var_options =['pre', 'tmax','recharge_adjust']
if ncvarname not in var_options:
    raise IOError('***ERROR: define ncvarname by setting -v to: {:}'.format(str(var_options)) )
var_type_options =['rel_change', 'abs_change', 'abs']
if var_type not in var_type_options:
    raise IOError('***ERROR: define var_type by setting -t to: {:}'.format(str(var_type_options)) )
eval_options=["summer", "winter", "spring", "autumn", "year"]
if eval_period not in eval_options:
    raise IOError('***ERROR: define eval_period by setting -e to: {:}'.format(str(eval_options)) )
rcp_options =['rcp26', 'rcp45', 'rcp85','rcpall']
if eval_rcp not in rcp_options:
    raise IOError('***ERROR: define rcp_eval by setting -v to: {:}'.format(str(rcp_options)) )
region_options =['de_hicam', 'germany', 'MDR','TH','BY',"ww_leipzig_ug"]
if mask_region not in region_options:
    raise IOError('***ERROR: define mask_region by setting -m to: {:}'.format(str(region_options)) )




# Main plot
nrow       = 1
ncol       = 4
textsize   = 12          # standard text size
hspace     = 0.01        # x-space between subplots
wspace     = 0.15       # y-space between subplots
dxabc      = 0.05        # % of (max-min) shift to the right from left y-axis for a,b,c,... labels
dyabc      = 0.90        # % of (max-min) shift up from lower x-axis for a,b,c,... labels

lwidth     = 0.5         # linewidth
elwidth    = 1.0         # errorbar line width
alwidth    = 1.0         # axis line width
msize      = 1.0         # marker size
mwidth     = 0.5         # marker edge width
# color: 'b'|'g'|'r'|'c'|'m'|'y'|'k'|'w'
#        'blue'|'green'|'red'|'cyan'|'magenta'|'yellow'|'black'|'white'
#        hex string '#eeefff' | RGB tuple (1,0.5,1) | html names 'burlywod', 'chartreuse', ...
#        grayscale intensity, e.g. '0.7', 'k'='0.0'
myBlue          = '#00589C'
myLightBlue     = '#E5F4FF'
FigLightBlue    = '#6FA6B9'
otherBlue       = '#6FA6FF'     # rgb = 111,166,255
myRed           = '#CA373B'
myOrange        = '#FDAE61'
mcol1      = (202/255.,0/255.,32/255.)     # primary marker colour
mcol2      = '0.0'       # color of second markers
mcol3      = '0.0'       # color of third markers
lcol1      = (5/255.,113/255.,176/255.)       # primary line colour
lcol2      = '0.0'       # color of second lines
lcol3      = '0.0'       # color of third lines

# Legend
llxbbox    = -0.01       # y-anchor legend bounding box
llybbox    = 0.04        # y-anchor legend bounding box
llrspace   = 0.          # spacing between rows in legend
llcspace   = 1.0         # spacing between columns in legend
llhtextpad = 0.4         # the pad between the legend handle and text
llhlength  = 1.5         # the length of the legend handles
frameon    = False       # if True, draw a frame around the legend. If None, use rc
llxbbox2    = 0.60       # Tight bounding of symbol and text (w/o lines)
llhtextpad2 = 0.         #                   "
llhlength2  = 1.0        #                   "

# PNG
dpi         = 300
transparent = False
bbox_inches = 'tight'
pad_inches  = 0
import matplotlib as mpl
import matplotlib.pyplot as plt

if (outtype == 'pdf'):
    mpl.use('PDF') # set directly after import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    # Customize: http://matplotlib.sourceforge.net/users/customizing.html
    mpl.rc('ps', papersize='a4', usedistiller='xpdf') # ps2pdf
elif (outtype == 'png'):
    mpl.use('Agg') # set directly after import matplotlib
    import matplotlib.pyplot as plt
    # mpl.rc('text.latex', unicode=True)
    mpl.rc('savefig', dpi=dpi, format='png')
else:
    import matplotlib.pyplot as plt

#mpl.rc('font',       **{'family':'serif','serif':['times']})
mpl.rcParams['text.latex.preamble']=r'\usepackage{wasysym}' 
mpl.rc('font',       size=textsize)
mpl.rc('lines',      linewidth=lwidth, color='black')
mpl.rc('axes',       linewidth=alwidth, labelcolor='black')
mpl.rc('path',       simplify=False) # do not remove
#mpl.rc('figure',      figsize=(11.69,8.27)) # a4 landscape
mpl.rc('figure',      figsize=(8.27,11.69/2.75))
mpl.rc('legend',     fontsize=textsize)
#mpl.rc('text',       usetex=True)
#mpl.rc('text.latex', unicode=True)

# -----------------------------------------------------------------------------
# PLOT natural features
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# geographical features
ocean         = cfeature.NaturalEarthFeature(category='physical', name='ocean',
                                             scale='50m',
                                             facecolor=cfeature.COLORS['water'])
state_borders = cfeature.NaturalEarthFeature(category='cultural', name='admin_0_countries',
                                             scale='10m',
                                             edgecolor='0.2',
                                             facecolor=cfeature.COLORS['land'])


import cartopy.feature as cfeature
from cartopy.feature import ShapelyFeature
import cartopy.io.shapereader as shpreader

shpf_fedcon = '/data/hydmet/WIS_D/shapes/BuLaender.shp'
reader    = shpreader.Reader(shpf_fedcon)
fed_count = ShapelyFeature(reader.geometries(), ccrs.PlateCarree())

# create coordinate system
#from pyproj import Proj
# projAim = Proj('+proj=laea +lat_0=52 +lon_0=10 +x_0=4321000 +y_0=3210000 +a=6378137 +f=0.0033528 +units=m')
# projection = ccrs.LambertAzimuthalEqualArea(central_latitude=52, central_longitude=10,
#                                             false_easting=4321000, false_northing=3210000)
crs_latlon = ccrs.PlateCarree()
projection = ccrs.Miller(central_longitude=10.0)
        
# read xx and yy coordinates
from ufz import readnc
# fname_mask    = "../../python/facc_mhm_derived_5km.nc"
# facc          = readnc(fname_mask, 'facc') * 25
# facc_mask     = (facc < 1000)
# xx            = readnc(fname_mask, 'x')
# yy            = readnc(fname_mask, 'y')

# read latitude and longitude
# file containing latitude and longitude grid
latlon_file   = '/data/hicam/data/processed/mhm_input/de_hicam/latlon/latlon_0p015625.nc'
# latlon_file   = './latlon_0p015625.nc'
lats          = readnc(latlon_file, var='lat')
lons          = readnc(latlon_file, var='lon')

# map_extent    = [-10, 28, 34.5, 70] # for LambertAzimuthalEqualArea
map_extent    = [5.7, 15.1, 47.2, 55]
BL = {
    'HH' : ('Hamburg'),
    'NI' : ('Niedersachsen'),
    'HB' : ('Bremen'),
    'NRW' : ('Nordrhein-Westfalen'),
    'HE' : ('Hessen'),
    'RP' : ('Rheinland-Pfalz'),
    'BW' : ('Baden-Württemberg'),
    'BY' : ('Bayern'),
    'SL' : ('Saarland'),
    'BE' : ('Berlin'),
    'BB' : ('Brandenburg'),
    'MV' : ('Mecklenburg-Vorpommern'),
    'SN' : ('Sachsen'),
    'ST' : ('Sachsen-Anhalt'),
    'TH' : ('Thüringen'),
    'SH' : ('Schleswig-Holstein'),
    'NDR' : ('Hamburg','Niedersachsen','Bremen','Mecklenburg-Vorpommern','Schleswig-Holstein'),
    'MDR' :  ('Sachsen','Sachsen-Anhalt','Thüringen'),
    'BE-BB' : ('Berlin', 'Brandenburg'),
    'SH-HH' : ('Schleswig-Holstein', 'Hamburg'),
    'NI-HB' : ('Niedersachsen', 'Bremen'),
    'RP-SL' : ('Rheinland-Pfalz', 'Saarland'),
    }

# region                  = "germany"
# region                  = "de_hicam"
# region                  = "MDR"
if mask_region == "germany":
    mask_path               = "/data/hicam/data/processed/dem_OR/mask_hicam_1km_g_inv.nc"
    extent                  = [5.7, 15.1, 47.2, 55]
elif mask_region == "de_hicam":
    mask_path               = "/data/hicam/data/processed/dem_OR/mask_hicam_1km_ghw_inv.nc"
    extent                  = [5.0, 20.0, 46.0, 56.0]

elif mask_region == "ww_leipzig_ug":
    mask_path               = "/data/hydmet/WIS_D/ww_leipzig/masks/mask_untersuchungsgebiet_grid.nc"
    extent                  = pd.read_csv("/data/hydmet/WIS_D/ww_leipzig/masks/extent_untersuchungsgebiet",header=1,
                                          )
    extent                  =[np.float(ex) for ex in extent]
    print(extent)
else:
    mask_path  = "/data/hydmet/WIS_D/masks/mask_ger_{:}.nc".format(mask_region)
    def sel_region(x):
        """Subregion selection for printing: ax.set_extent """
        return{
            'BRD': [5.75, 15.25, 47.25, 55],
            'TH': [9.7, 12.8, 50.1, 51.7],
            'ST': [10, 13.7, 50.8, 53.2],
            'BB': [11, 15, 51.3, 53.6],
            'HE': [7, 11, 49, 52],
            'SN': [11.8, 15.1, 50.15, 51.72],
            'MDR': [9.7, 15.1, 50, 53.3],
            'SH': [7.5, 12, 53.3, 55.2],
            'NRW': [5.75, 9.5, 50.3, 52.55],
            'NDR': [5.75, 15.25, 51.2, 55.2],
            'NI': [6.5, 11.75, 51.2, 54],
            'HH' : [8.27, 10.47, 53.29, 54.06],
            'HB' : [8.33, 9.13, 52.91, 53.71],
            'MV': [10.44, 14.56, 53.02, 54.78],
            'NRW' : [5.72, 9.6, 50.22, 52.63],
            'RP' : [5.97, 8.66, 48.87, 51.04],
            'SL': [6.21, 7.55, 49.01, 49.74],
            'BW' : [7.36, 10.64, 47.43, 49.89],
            'BY' : [8.83, 13.99, 47.17, 50.66],
            'ST' : [10.41, 13.34, 50.84, 53.14],
            'BE' : [12.94, 13.91, 52.24, 52.77],
            'BE-BB': [11, 15, 51.3, 53.6],
            'SH-HH': [7.5, 12, 53.3, 55.2],
            'NI-HB': [6.5, 11.75, 51.2, 54],
            'RP-SL': [5.97, 8.66, 48.87, 51.04]
        }.get(x, [5.75, 15.25, 47.25, 55])
    extent = sel_region(mask_region)
#  -- colormaps ------------------------------------

if var_type == 'rel_change':
    cmap_1 = get_brewer('Blues9',rgb=True)
    cmap_2 = get_brewer('Reds9',rgb=True)
    levels        = np.arange(-30,33,3)
    colorbarlabel = 'Relative Change [%]'
    if ncvarname == 'tmax':
        cmap = mpl.colors.ListedColormap(cmap_1[::-1] + [(1.0,1.0,1.0),(1.0,1.0,1.0) ] + cmap_2)
        if indicator == "n_heatdays":
            levels        = np.arange(-100,110,10)
            colorbarlabel = 'relative Änderung mittl. Anzahl Hitzetage/Jahr [%]'
        if indicator == "n_summerdays":
            levels        = np.arange(-100,110,10)
            colorbarlabel = 'relative Änderung  mittl. Anzahl Sommertage/Jahr [%]'

    if ncvarname == 'pre':
        cmap = mpl.colors.ListedColormap(cmap_2[::-1] + [(1.0,1.0,1.0),(1.0,1.0,1.0) ] + cmap_1)
    if ncvarname == 'recharge_adjust':
        levels        = np.arange(-100,110,10)
        cmap = mpl.colors.ListedColormap(cmap_2[::-1] + [(1.0,1.0,1.0),(1.0,1.0,1.0) ] + cmap_1)
    if ncvarname == 'recharge':
        cmap = mpl.colors.ListedColormap(cmap_2[::-1] + [(1.0,1.0,1.0),(1.0,1.0,1.0) ] + cmap_1)
        colorbarlabel = 'Relative Change [%]'
        if indicator == 'sum':
            levels    = np.arange(-100,110,10)
        if indicator == '20perc':
            levels    = np.arange(-100,110,10)

if var_type == 'abs_change':
    cmap_1 = get_brewer('PuBuGn9',rgb=True)
    cmap_2 = get_brewer('YlOrRd9',rgb=True)
    if ncvarname == 'tmax':
        cmap = mpl.colors.ListedColormap(cmap_1[::-1] + [(1.0,1.0,1.0),(1.0,1.0,1.0) ] + cmap_2)
        colorbarlabel = 'Absolute Change [°C]'
        levels        = np.arange(-5,5.5,0.5)
        if indicator == "n_heatdays":
            levels        = np.arange(-30,33,3)
            colorbarlabel = 'abs. Änderung mittl. Anzahl Hitzetage/Jahr'
        if indicator == "n_summerdays":
            levels        = np.arange(-50,55,5)
            colorbarlabel = 'abs. Änderung mittl. Anzahl Sommertage/Jahr'
    if ncvarname == 'pre':
        cmap = mpl.colors.ListedColormap(cmap_2[::-1] + [(1.0,1.0,1.0),(1.0,1.0,1.0) ] + cmap_1)
        colorbarlabel = 'Absolute Change [mm]'
        levels        = np.arange(-200,320,20)
    if ncvarname == 'recharge_adjust':
        cmap = mpl.colors.ListedColormap(cmap_2[::-1] + [(1.0,1.0,1.0),(1.0,1.0,1.0) ] + cmap_1)
        colorbarlabel = 'Absolute Change [mm]'
        levels        = np.arange(-50,60,10)
    if ncvarname == 'tavg':
        cmap = mpl.colors.ListedColormap([(1.0,1.0,1.0)] + cmap_2)
        colorbarlabel = 'Absolute Change [°C]'
        if indicator == 't_mean':
            levels        = np.arange(0,6,0.6)
    if ncvarname == 'recharge':
        cmap = mpl.colors.ListedColormap(cmap_2[::-1] + [(1.0,1.0,1.0),(1.0,1.0,1.0) ] + cmap_1)
        #cmap = mpl.colors.ListedColormap([(1.0,1.0,1.0)] + cmap_2)
        colorbarlabel = 'Absolute Change [mm]'
        if indicator == 'sum':
            levels    = np.arange(-30,33,3)
        if indicator == '20perc':
            levels    = np.arange(-10,11,1)

if var_type == 'abs':
    cmap_1 = get_brewer('PuRd9',rgb=True)[3:6][::-1]
    cmap_2 = get_brewer('Spectral11',rgb=True)[:8:][::-1]
    cmap_3 = get_brewer('Blues9',rgb= True)[::2]
    cmap = mpl.colors.ListedColormap(cmap_3 + cmap_2 + cmap_1)
    if ncvarname == 'pre':
        colorbarlabel = 'Precipitation [mm]'
        levels        = np.arange(100,560,50)
    if ncvarname == 'recharge_adjust':
        colorbarlabel = 'Recharge [mm]'
        levels        = np.array([0,25,50,75,100,150,200,300,350,500,10000])
        colors        = ["#fb8144","#ffb976" ,"#ffd57f","#fff157","#bbd67a", "#8eca94", "#78cbbe", "#55bac8","#32a9b8", "#009eab"  ]
        cmap = mpl.colors.ListedColormap(colors)
    if ncvarname == 'tavg':
        colorbarlabel = 'Temperature [°C]'
        levels        = np.arange(-3,30,3)
    if ncvarname == 'recharge':
        colorbarlabel = 'Recharge [mm/year]'
        if indicator == 'sum':
            levels    = np.arange(0,275,25)
        if indicator == '20perc':
            levels    = np.arange(1,12,1)

    if ncvarname == 'tmax':
        colorbarlabel = 'Temperature [°C]'
        levels        = np.arange(12,34.5,2)
        levels        = np.arange(10,42.5,2)
        if indicator == "n_summerdays":
            levels        = np.arange(0,74,5)
            colorbarlabel = 'mittl. Anzahl Sommertage [tmax >25°C] pro Jahr'
        if indicator == "n_heatdays":
            levels        = np.arange(0,30,2)
            colorbarlabel = 'mittl. Anzahl Hitzetage [tmax >30°C] pro Jahr'
