#!/usr/bin/python
# -*- coding:utf-8 -*-

import time

from IT8951.constants import Rotate, DEFAULT_VCOM
from IT8951.display import AutoEPDDisplay
# from working_test_functions import *
from IT8951 import constants
from PIL import Image, ImageOps
import sys

from testing.my_display import MyDisplay
from book_manager.data.db_manager import get_book_data

import time
import RPi.GPIO as GPIO

BTN_ON = 0
BTN_OFF = 1

gpio_buttons = [21, 20, 16, 26, 19, 13, 6, 12]
GPIO.setmode(GPIO.BCM)

# set GPIO buttons as pull down
for btn in gpio_buttons:
    GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def next_page(book_state):
    if book_state.last_read_page < book_state.book.num_pages:
        book_state.last_read_page += 1
    return book_state


def prev_page(book_state):
    if book_state.last_read_page > 1:
        book_state.last_read_page -= 1
    return book_state


def handle_button_02():
    pass


def handle_button_03():
    pass


def handle_button_04():
    pass


def handle_button_05():
    pass


def handle_button_06():
    pass


def handle_button_07():
    pass


print('Initializing EPD...')

# here, spi_hz controls the rate of data transfer to the device, so a higher
# value means faster display refreshes. the documentation for the IT8951 device
# says the max is 24 MHz (24000000), but my device seems to still work as high as
# 80 MHz (80000000)
display = MyDisplay(vcom=DEFAULT_VCOM, rotate="CCW", spi_hz=24000000, flip=False)


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





def read_book(book_id):
    print('Reading book "{}"...'.format(book_id))
    book_data = get_book_data(1)

    while True:
        states = [GPIO.input(btn) for btn in gpio_buttons]

        if states[0] == 1:
            book_data = next_page(book_data)  # book_data.prev_page()
            display_image_8bpp(display, book_data.get_page_path())

        if states[1] == 1:
            book_data = prev_page(book_data)  # book_data.next_page()

        if states[2] == 1:
            handle_button_02(book_data)

        if states[3] == 1:
            handle_button_03(book_data)

        if states[4] == 1:
            handle_button_04(book_data)

        if states[5] == 1:
            handle_button_05(book_data)

        if states[6] == 1:
            handle_button_06(book_data)

        if states[7] == 1:
            handle_button_07(book_data)

        print(states)
        time.sleep(0.1)


if __name__ == '__main__':
    # while True:
    #     states = [GPIO.input(btn) for btn in gpio_buttons]
    #     print(states)
    #     time.sleep(0.1)
    # 
    # exit()
    read_book(1)
    x = get_book_data(1)
    print(x)
