#!/usr/bin/python
# -*- coding:utf-8 -*-

import os, sys, random, time
from PIL import Image
from PIL import ImageEnhance
import ffmpeg
from working_test_functions import *

def generate_frame(in_filename, out_filename, time, width, height):    
    (
        ffmpeg
        .input(in_filename, ss=time)
        .filter('scale', width, height, force_original_aspect_ratio=1)
        .filter('pad', width, height, -1, -1)
        .output(out_filename, vframes=1)              
        .overwrite_output()
        .run(capture_stdout=True, capture_stderr=True)
    )


viddir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '/home/pi/NewSlowMovieVideos/')

from IT8951.display import AutoEPDDisplay

print('Initializing EPD...')

# here, spi_hz controls the rate of data transfer to the device, so a higher
# value means faster display refreshes. the documentation for the IT8951 device
# says the max is 24 MHz (24000000), but my device seems to still work as high as
# 80 MHz (80000000)
display = AutoEPDDisplay(vcom=-1.17, rotate=None, spi_hz=24000000)
# display the image 


print('VCOM set to', display.epd.get_vcom())


display_image_8bpp(display, '/home/pi/NewSlowMovie/IT8951/grab.jpg')
print('Diplaying frame %d of %s' %(frame,currentVideo))

# Wait for 10 seconds 
time.sleep(10)

    
exit()
