#!/usr/bin/python
# -*- coding:utf-8 -*-

import time

from IT8951.constants import Rotate
from IT8951.display import AutoEPDDisplay
from working_test_functions import *

print('Initializing EPD...')

# here, spi_hz controls the rate of data transfer to the device, so a higher
# value means faster display refreshes. the documentation for the IT8951 device
# says the max is 24 MHz (24000000), but my device seems to still work as high as
# 80 MHz (80000000)
display = AutoEPDDisplay(vcom=-1.17, rotate=None, spi_hz=24000000)
# display the image 


print('VCOM set to', display.epd.get_vcom())

rotate_list=[Rotate.NONE,Rotate.CW, Rotate.CCW,Rotate.FLIP,Rotate.NONE, ]

for i in range(5):
    display._set_rotate(rotate_list[i])
    display_image_8bpp(display, '/home/pi/NewSlowMovie/Sadhguru.png')

    # Wait for 10 seconds
    time.sleep(2)

    
exit()
