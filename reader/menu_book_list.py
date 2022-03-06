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
from book_manager_2_data_2_db_manager import get_books_list

print('Initializing EPD...')

# FONT_STANDARD="./fonts/arial.ttf"
FONT_STANDARD = "./fonts/typewriter.ttf"
BACKGROUND_COLOR = 'white'
FONT_H1_SIZE = 60
FONT_NORMAL_SIZE = 25

# here, spi_hz controls the rate of data transfer to the device, so a higher
# value means faster display refreshes. the documentation for the IT8951 device
# says the max is 24 MHz (24000000), but my device seems to still work as high as
# 80 MHz (80000000)
display = MyDisplay(vcom=DEFAULT_VCOM, rotate="CCW", spi_hz=24000000, flip=False)
POINTER_SPACE_X_START, POINTER_SPACE_X_END, POINTER_SPACE_Y_START, POINTER_SPACE_Y_END = display.width - 20, display.width - 40, 0, display.height


def display_custom_text():
    # clearing image to white
    display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))
    blank_image = Image.new('RGBA', (display.width, display.height), BACKGROUND_COLOR)
    img_draw = ImageDraw.Draw(blank_image)
    img_draw.rectangle((70, 50, 270, 200), outline='red', fill='blue')
    img_draw.regular_polygon((50, 280, 15), 5, fill='blue')
    font = ImageFont.truetype("./fonts/arial.ttf", 60)
    # font=ImageFont.truetype(size=30)

    img_draw.text((70, 250), 'Hello World', fill='green', font=font)
    # blank_image.save('drawn_image.jpg')
    blank_image = ImageOps.mirror(blank_image)

    # TODO: this should be built-in
    dims = (display.width, display.height)
    print(f"Setting image dimensions to {dims}")
    # img.thumbnail(dims)
    # paste_coords = [dims[i] - img.size[i] for i in (0, 1)]  # align image with bottom of display
    paste_coords = [0, 0]
    display.frame_buf.paste(blank_image, paste_coords)
    display.draw_full(constants.DisplayModes.GC16)
    # display.draw_partial(constants.DisplayModes.DU)


def get_position_of_text(text_position, font):
    ascent_normal, descent_normal = font.getmetrics()
    total_text_height_normal = ascent_normal + descent_normal
    para_spacing_normal = 15
    start_x_book_list = 70
    start_y_book_list = 100
    para_height_normal = total_text_height_normal + para_spacing_normal
    return start_x_book_list, start_y_book_list + para_height_normal * (text_position + 1), para_height_normal


def display_book_list(blank_image):
    # clearing image to white
    display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))
    img_draw = ImageDraw.Draw(blank_image)
    book_list = get_books_list()
    start_x_heading = 70
    start_y_heading = 50
    font_H1 = ImageFont.truetype(FONT_STANDARD, FONT_H1_SIZE)

    img_draw.text((start_x_heading, start_y_heading), 'Book List', font=font_H1, fill='black', )

    font_normal = ImageFont.truetype(FONT_STANDARD, FONT_NORMAL_SIZE)
    # ascent_normal, descent_normal = font_normal.getmetrics()
    # total_text_height_normal = ascent_normal + descent_normal
    # para_spacing_normal = 15
    # start_x_book_list = 70
    # start_y_book_list = 100
    # para_height_normal = total_text_height_normal + para_spacing_normal

    for index, book in enumerate(book_list):
        print(book)
        x_pos, y_pos, _ = get_position_of_text(index, font_normal)
        img_draw.text((x_pos, y_pos), book.folder,
                      font=font_normal, fill='black', )

    blank_image = ImageOps.mirror(blank_image)

    # TODO: this should be built-in
    dims = (display.width, display.height)
    print(f"Setting image dimensions to {dims}")
    paste_coords = [0, 0]
    display.frame_buf.paste(blank_image, paste_coords)
    display.draw_full(constants.DisplayModes.GC16)
    return blank_image
    # display.draw_partial(constants.DisplayModes.DU)


def move_icon(blank_image):
    display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))
    for i in range(0, display.width, 50):
        img_draw = ImageDraw.Draw(blank_image)
        img_draw.regular_polygon((i, 280, 15), 5, fill='blue')
        paste_coords = [0, 0]
        display.frame_buf.paste(blank_image, paste_coords)
        display.draw_partial(constants.DisplayModes.GC16)

    return blank_image


def clear_pointer_space(blank_image):
    paste_coords = [0, 0]
    img_draw = ImageDraw.Draw(blank_image)
    # img_draw.regular_polygon((i, 280, 15), 5, fill='blue')
    # img_draw.rectangle((70, 50, 270, 200), outline=BACKGROUND_COLOR, fill=BACKGROUND_COLOR)
    clear_rect = (POINTER_SPACE_X_START, POINTER_SPACE_Y_START, POINTER_SPACE_X_END, POINTER_SPACE_Y_END)
    img_draw.rectangle(clear_rect, outline=BACKGROUND_COLOR, fill=BACKGROUND_COLOR)
    img_draw.regular_polygon((0, 0, 30), 5, fill='blue')
    display.frame_buf.paste(blank_image, paste_coords)
    display.draw_partial(constants.DisplayModes.GC16)
    return blank_image


def put_selection_icon(img_draw, x, y):
    img_draw.regular_polygon((POINTER_SPACE_X_END, y, 7), 5, fill='blue')
    return img_draw


def draw_selection_icon(blank_image, selection_index):
    paste_coords = [0, 0]
    img_draw = ImageDraw.Draw(blank_image)
    text_x, text_y, text_height = get_position_of_text(selection_index, ImageFont.truetype(FONT_STANDARD, FONT_NORMAL_SIZE))
    put_selection_icon(img_draw, text_x, text_y+text_height/2)
    display.frame_buf.paste(blank_image, paste_coords)
    display.draw_partial(constants.DisplayModes.GC16)
    return blank_image


if __name__ == '__main__':
    # display_custom_text()
    blank_image = Image.new('RGBA', (display.width, display.height), BACKGROUND_COLOR)

    # display_custom_text()
    blank_image = display_book_list(blank_image)
    blank_image = clear_pointer_space(blank_image)
    blank_image = draw_selection_icon(blank_image, 0)
    # blank_image= move_icon(blank_image)
    exit()
