#!/usr/bin/python
# -*- coding:utf-8 -*-

import time

from IT8951.constants import Rotate, DEFAULT_VCOM
from IT8951 import constants
from PIL import Image, ImageOps, features

from IT8951.constants import Rotate, DEFAULT_VCOM
from IT8951.display import AutoEPDDisplay
from IT8951 import constants
from PIL import Image, ImageOps

from my_display import MyDisplay

from my_display import MyDisplay

print('Initializing EPD...')
display = MyDisplay(vcom=DEFAULT_VCOM, rotate="CCW", spi_hz=24000000, flip=False)


def display_image_8bpp(display, img_path):
    print('Displaying "{}"...'.format(img_path))

    # clearing image to white
    display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))

    img = ImageOps.mirror(Image.open(img_path))  # not sure why my image is mirrored so I'm mirroring it here

    # TODO: this should be built-in
    dims = (display.width, display.height)
    print(f"Setting image dimensions to {dims}")
    img.thumbnail(dims)
    paste_coords = [dims[i] - img.size[i] for i in (0, 1)]  # align image with bottom of display
    display.frame_buf.paste(img, paste_coords)

    display.draw_full(constants.DisplayModes.GC16)


import sys

if __name__ == '__main__':

    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            print("Argument: {}".format(sys.argv[i]))
            display_image_8bpp(display, sys.argv[i])
            n = 2
            time.sleep(n)

    exit()
