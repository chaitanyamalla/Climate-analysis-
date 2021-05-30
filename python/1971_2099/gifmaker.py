#! /usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------
#  File:        gif_maker.py
#
#  Created:     Mi 14-05-2021
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: making GIF from the 88 MET data for each indicator. 
#
#  Modified by: 
#  Modified date: 
#
# --------------------------------------------------





import PIL
from PIL import Image
import numpy as np


inpath="/work/malla/ww_leipzig/data_1971_2099/output_1971_2099/"
met_start=1
met_end=88

# ### PRE GIF######
# image_frames = []
# for met in range(met_start, met_end+1):
#     met_id="met"+'_'+ str(met).zfill(3)
    
#     newframe = PIL.Image.open(inpath + "pre/" + met_id + ".png")
#     image_frames.append(newframe)

# #    print(image_frames)
# image_frames[0].save(inpath+"pre/"+"pre.gif",
#                      format = 'GIF',
#                      append_images = image_frames[1:],
#                      save_all = True,
#                      duration = 400,
#                      loop = 0)


# ### tmax30 GIF ######
# image_frames1 = []
# for met in range(met_start, met_end+1):
#     met_id="met"+'_'+ str(met).zfill(3)
    
#     newframe = PIL.Image.open(inpath + "tmax/" + met_id + ".png")
#     image_frames1.append(newframe)

# image_frames1[0].save(inpath+"tmax/"+"tmax.gif",
#                      format = 'GIF',
#                      append_images = image_frames1[1:],
#                      save_all = True,
#                      duration = 400,
#                      loop = 0)

# ###recahrge Gif   #####
# image_frames2 = []
# for met in range(met_start, met_end+1):
#     met_id="met"+'_'+ str(met).zfill(3)
    
#     newframe = PIL.Image.open(inpath + "recharge/" + met_id + ".png")
#     image_frames2.append(newframe)
    
# image_frames2[0].save(inpath+"recharge/"+"recharge_1971_2099.gif",
#                      format = 'GIF',
#                      append_images = image_frames2[1:],
#                      save_all = True,
#                      duration = 400,
#                      loop = 0)

###aET and pet ####
image_frames3 = []
for met in range(met_start, met_end+1):
    met_id="met"+'_'+ str(met).zfill(3)
    
    newframe = PIL.Image.open(inpath + "pet_aET/" + met_id + "_aET_pet_ysum_1971_2099_ts.png")
    image_frames3.append(newframe)
    
image_frames3[0].save(inpath+"pet_aET/"+"pet_aET_ysum_METfiles_1971_2099.gif",
                     format = 'GIF',
                     append_images = image_frames3[1:],
                     save_all = True,
                     duration = 400,
                     loop = 0)
