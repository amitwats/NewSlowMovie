
from PIL import Image, ImageDraw, ImageFont
# !/usr/bin/python
# -*- coding:utf-8 -*-

import time

from IT8951.constants import Rotate, DEFAULT_VCOM
from IT8951.display import AutoEPDDisplay
# from working_test_functions import *
from IT8951 import constants
from PIL import Image, ImageOps

from my_display import MyDisplay

print('Initializing EPD...')

# here, spi_hz controls the rate of data transfer to the device, so a higher
# value means faster display refreshes. the documentation for the IT8951 device
# says the max is 24 MHz (24000000), but my device seems to still work as high as
# 80 MHz (80000000)
display = MyDisplay(vcom=DEFAULT_VCOM, rotate="CCW", spi_hz=24000000, flip=False)


def display_custom_text():
    # clearing image to white
    display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))
    blank_image = Image.new('RGBA', (display.width, display.height), 'white')
    img_draw = ImageDraw.Draw(blank_image)
    img_draw.rectangle((70, 50, 270, 200), outline='red', fill='blue')
    img_draw.circle((300, 300, 50), outline='red', fill='blue')
    font = ImageFont.truetype("./fonts/arial.ttf", 60)
    # font=ImageFont.truetype(size=30)

    img_draw.text((70, 250), 'Hello World', fill='green', font=font)
    # blank_image.save('drawn_image.jpg')
    blank_image =ImageOps.mirror(blank_image)

    # TODO: this should be built-in
    dims = (display.width, display.height)
    print(f"Setting image dimensions to {dims}")
    # img.thumbnail(dims)
    # paste_coords = [dims[i] - img.size[i] for i in (0, 1)]  # align image with bottom of display
    paste_coords= [0, 0]
    display.frame_buf.paste(blank_image, paste_coords)
    # display.draw_full(constants.DisplayModes.GC16)
    display.draw_partial(constants.DisplayModes.DU)




import sys

if __name__ == '__main__':

    display_custom_text()
    exit()




