#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
import RPi.GPIO as GPIO

# from IT8951.constants import Rotate, DEFAULT_VCOM
from IT8951.display import AutoEPDDisplay
# from working_test_functions import *
# from IT8951 import constants
# from PIL import Image, ImageOps
#
# from my_display import MyDisplay
#
# print('Initializing EPD...')

# here, spi_hz controls the rate of data transfer to the device, so a higher
# value means faster display refreshes. the documentation for the IT8951 device
# says the max is 24 MHz (24000000), but my device seems to still work as high as
# 80 MHz (80000000)
# display = MyDisplay(vcom=DEFAULT_VCOM, rotate="CCW", spi_hz=24000000, flip=False)

# Setting GPIO Pins
button_no_21 = 21
button_np_20 = 20
GPIO.setmode(GPIO.BCM)
# GPIO.setup(button_no_21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.setup(button_np_40, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button_np_20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.setup(button_np_40, GPIO.IN)
for _ in range(9):
    state_21 = GPIO.input(button_no_21)
    state_20 = GPIO.input(button_np_20)
    print(f"State of 21 is is {state_21}")
    print(f"State of 20 is is {state_20}")
    time.sleep(1)

GPIO.cleanup()

# def display_image_8bpp(display, img_path):
#     print('Displaying "{}"...'.format(img_path))
#
#     # clearing image to white
#     display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))
#
#     img = ImageOps.mirror(Image.open(img_path))  # not sure why my image is mirrored so I'm mirroring it here
#     # img=ImageOps.mirror(img)
#
#     # TODO: this should be built-in
#     dims = (display.width, display.height)
#     print(f"Setting image dimensions to {dims}")
#     img.thumbnail(dims)
#     paste_coords = [dims[i] - img.size[i] for i in (0, 1)]  # align image with bottom of display
#     display.frame_buf.paste(img, paste_coords)
#
#     display.draw_full(constants.DisplayModes.GC16)
#     # display.draw_partial(constants.DisplayModes.DU)
#
#
# # display the image
#
#
# print('VCOM set to', display.epd.get_vcom())
#
# rotate_list = [None, 'CW', 'CCW', 'flip', None, ]
#
# import sys
#
# image_1 = "./indrajal/002.jpg"
# image_2 = "./indrajal/page0.jpg"
#
# if __name__ == '__main__':
#
#     for _ in range(9):
#         state = GPIO.input(button_no)
#         print(f"State is {state}")
#         if state == 1:
#             display_image_8bpp(display, image_1)
#         else:
#             display_image_8bpp(display, image_2)
#         time.sleep(1)
#
#     exit()
