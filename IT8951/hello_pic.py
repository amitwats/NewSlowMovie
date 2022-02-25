#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
from PIL import Image
from PIL import ImageEnhance
import ffmpeg
from working_test_functions import *



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
