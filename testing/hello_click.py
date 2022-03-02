#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
import RPi.GPIO as GPIO

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

# Setting GPIO Pins
button_no = 21
run_butoon = 20
print(f"The Mode is {GPIO.getmode()}")
# GPIO.setmode(GPIO.BOARD)
GPIO.setup(button_no, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(run_butoon, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def display_image_8bpp(display, img_path):
    print('Displaying "{}"...'.format(img_path))

    # clearing image to white
    display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))

    img = ImageOps.mirror(Image.open(img_path))  # not sure why my image is mirrored so I'm mirroring it here
    # img=ImageOps.mirror(img)

    # TODO: this should be built-in
    dims = (display.width, display.height)
    print(f"Setting image dimensions to {dims}")
    img.thumbnail(dims)
    paste_coords = [dims[i] - img.size[i] for i in (0, 1)]  # align image with bottom of display
    display.frame_buf.paste(img, paste_coords)

    display.draw_full(constants.DisplayModes.GC16)
    # display.draw_partial(constants.DisplayModes.DU)


# display the image


print('VCOM set to', display.epd.get_vcom())

rotate_list = [None, 'CW', 'CCW', 'flip', None, ]

import sys

image_1 = "./indrajal/002.jpg"
image_2 = "./indrajal/page0.jpg"


def loop():
    # last_state_21=0
    # run_state=True
    # while run_state:
    #     state_21 = GPIO.input(button_no)
    #     state_20=GPIO.input(run_butoon)
    #     if state_20==1:
    #         run_state=False
    #         print("Exiting")
    #     if state_21 != last_state_21:
    #         last_state_21=state_21
    #         if state_21 == 1:
    #             display_image_8bpp(display, image_1)
    #         else:
    #             display_image_8bpp(display, image_2)
    #     else:
    #         print("Same STate")
    #

    while True:
        state_21 = GPIO.input(button_no)
        state_20=GPIO.input(run_butoon)
        print(f"State of 21 is {state_21}")
        print(f"State of 20 is {state_21}")
        time.sleep(0.1)

if __name__ == '__main__':

    # for _ in range(90):
    #     state = GPIO.input(button_no)
    #     print(f"State is {state}")
    #     if state == 1:
    #         display_image_8bpp(display, image_1)
    #     else:
    #         display_image_8bpp(display, image_2)
    #     # time.sleep(1)
    #     time.sleep(0.1)


    # run_state=True
    # while run_state:
    #     run_state = False if GPIO.input(run_butoon)==1 else True
    #     state = GPIO.input(button_no)
    #     print(f"State is {state}")
    #     if state == 1:
    #         display_image_8bpp(display, image_1)
    #     else:
    #         display_image_8bpp(display, image_2)
        # time.sleep(1)
        # time.sleep(0.1)
    loop()
    exit()
