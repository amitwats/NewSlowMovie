#!/usr/bin/python
# -*- coding:utf-8 -*-

import time

from IT8951.constants import Rotate, DEFAULT_VCOM
from IT8951.display import AutoEPDDisplay
# from working_test_functions import *
from IT8951 import constants
from PIL import Image, ImageOps
import sys

from my_display import MyDisplay
from book_manager_2_data_2_db_manager import get_book_data, get_books_list

import time
import RPi.GPIO as GPIO

from menu_book_list import MenuBookList

BTN_ON = 0
BTN_OFF = 1

gpio_buttons = [21, 20, 16, 26, 19, 13, 6, 12]
GPIO.setmode(GPIO.BCM)

# set GPIO buttons as pull down
for btn in gpio_buttons:
    GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

valid_modes = ["read", "menu_book_list"]
current_mode = "menu_book_list"


def handle_button_02(book_data):
    pass


def handle_button_03(book_data):
    pass


def handle_button_04(book_data):
    pass


def handle_button_05(book_data):
    pass


def handle_button_06(book_data):
    pass


def handle_button_07(book_data):
    book_list = get_books_list()
    menu_book_list = MenuBookList(book_list, display)

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


def handle_mode_read(states, book_data):
    has_changed = False

    if states[0] == BTN_ON:
        has_changed = book_data.move_next_page()
        print(f"Next Page : {book_data.last_read_page}")

    if states[1] == BTN_ON:
        has_changed = book_data.move_prev_page()

    if states[2] == BTN_ON:
        # handle_button_02(book_data)
        pass

    if states[3] == BTN_ON:
        # handle_button_03(book_data)
        pass

    if states[4] == BTN_ON:
        # handle_button_04(book_data)
        pass

    if states[5] == BTN_ON:
        # handle_button_05(book_data)
        pass

    if states[6] == BTN_ON:
        # handle_button_06(book_data)
        pass

    if states[7] == BTN_ON:
        global current_mode
        current_mode = "menu_book_list"
        print("Changing the mode to menu_book_list")
        return "CHANGE_MODE", "menu_book_list"

        # handle_button_07(book_data)

    if has_changed:
        display_image_8bpp(display, book_data.get_last_page_path())
        # has_changed = False

    return "CONTINUE", None


def handle_mode_menu_book_list(states, menu_book_list):
    if states[0] == BTN_ON:
        menu_book_list.select_previous()
        # return "CHANGE_MODE", f"read,{menu_book_list.get_current_selection().book_id}"

    if states[1] == BTN_ON:
        menu_book_list.select_next()

    if states[2] == BTN_ON:
        pass

    if states[3] == BTN_ON:
        pass

    if states[4] == BTN_ON:
        return "BOOK_SELECTED", 1

    if states[5] == BTN_ON:
        pass

    if states[6] == BTN_ON:
        pass

    if states[7] == BTN_ON:
        return "CONTINUE", None

    return "CONTINUE", None


def create_menu_book_list():
    book_list = get_books_list()
    menu_book_list = MenuBookList(book_list, display)
    menu_book_list.display_book_list()
    return menu_book_list


def read_book(book_id):
    print('Reading book "{}"...'.format(book_id))
    book_data = get_book_data(1)
    global current_mode
    menu_book_list = None

    while True:
        states = [GPIO.input(btn_no) for btn_no in gpio_buttons]
        if current_mode == "read":

            menu_book_list = None
            handle_type, handle_value = handle_mode_read(states, book_data)
            if handle_type == "CHANGE_MODE":
                current_mode = handle_value
                # print("Changing the mode to {}".format(handle_value))
                # handle_values_list=handle_value.split(",")
                # current_mode = handle_values_list[0]
                # book_data = get_book_data(int(handle_values_list[1]))
        elif current_mode == "menu_book_list":
            if not menu_book_list:
                menu_book_list = create_menu_book_list()
            handle_type, handle_value = handle_mode_menu_book_list(states, menu_book_list)
            if handle_type == "BOOK_SELECTED":
                # handle_values_list=handle_value.split(",")
                # current_mode = handle_values_list[0]
                # book_data = get_book_data(int(handle_values_list[1]))
                book_data = get_book_data(handle_value)
                menu_book_list = None
                # book_data = get_book_data(handle_value)
                # current_mode = "read"
                display_image_8bpp(display, book_data.get_last_page_path())

        print(f"Mode {current_mode} and {states}")
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
