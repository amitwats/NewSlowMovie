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


class MenuBookList:

    def __init__(self, display_obj, image_obj, image_draw_obj=None):
        self.display = display_obj
        self.image_obj = image_obj
        if not image_draw_obj:
            self.image_draw = ImageDraw.Draw(self.image_obj)
        else:
            self.image_draw = image_draw_obj

        self.selection_index = 0
        self.selection_index_max = 0
        self.POINTER_SPACE_X_START = display.width - 20
        self.POINTER_SPACE_X_END = display.width - 50
        self.POINTER_SPACE_Y_START = 0
        self.POINTER_SPACE_Y_END = display.height

    def display_book_list(self):
        # clearing image to white
        display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))
        book_list = get_books_list()
        start_x_heading = 70
        start_y_heading = 50
        font_H1 = ImageFont.truetype(FONT_STANDARD, FONT_H1_SIZE)

        self.image_draw.text((start_x_heading, start_y_heading), 'Book List', font=font_H1, fill='black', )

        font_normal = ImageFont.truetype(FONT_STANDARD, FONT_NORMAL_SIZE)
        # ascent_normal, descent_normal = font_normal.getmetrics()
        # total_text_height_normal = ascent_normal + descent_normal
        # para_spacing_normal = 15
        # start_x_book_list = 70
        # start_y_book_list = 100
        # para_height_normal = total_text_height_normal + para_spacing_normal

        for index, book in enumerate(book_list):
            print(book)
            x_pos, y_pos, _ = self.get_position_of_text(index, font_normal)
            self.image_draw.text((x_pos, y_pos), book.folder,
                          font=font_normal, fill='black', )

        self.image_obj = ImageOps.mirror(self.image_obj)

        # TODO: this should be built-in
        dims = (display.width, display.height)
        print(f"Setting image dimensions to {dims}")
        paste_coords = [0, 0]
        display.frame_buf.paste(self.image_obj, paste_coords)
        display.draw_full(constants.DisplayModes.GC16)
        return self.image_obj
        # display.draw_partial(constants.DisplayModes.DU)

    def clear_pointer_space(self):
        paste_coords = [0, 0]
        # img_draw = ImageDraw.Draw(self.image_obj)
        # img_draw.regular_polygon((i, 280, 15), 5, fill='blue')
        # img_draw.rectangle((70, 50, 270, 200), outline=BACKGROUND_COLOR, fill=BACKGROUND_COLOR)
        clear_rect = (self.POINTER_SPACE_X_START, self.POINTER_SPACE_Y_START,
                      self.POINTER_SPACE_X_END, self.POINTER_SPACE_Y_END)
        # self.image_draw.rectangle(clear_rect, outline=BACKGROUND_COLOR, fill=BACKGROUND_COLOR)
        self.image_draw.rectangle(clear_rect, outline=BACKGROUND_COLOR, fill='black')

        # img_draw.regular_polygon((0, 0, 30), 5, fill='blue')
        display.frame_buf.paste(self.image_obj, paste_coords)
        display.draw_partial(constants.DisplayModes.GC16)

    def draw_selection_icon(self, selection_index):
        paste_coords = [0, 0]
        self.clear_pointer_space()
        text_x, text_y, text_height = self.get_position_of_text(selection_index,
                                                                ImageFont.truetype(FONT_STANDARD, FONT_NORMAL_SIZE))
        self.put_selection_icon(text_x, text_y + text_height * 0.4)
        display.frame_buf.paste(self.image_obj, paste_coords)
        display.draw_partial(constants.DisplayModes.GC16)

    def put_selection_icon(self, x, y):
        radius_icon = 9
        self.image_draw.regular_polygon((self.POINTER_SPACE_X_END + radius_icon, y, radius_icon),
                                      5, rotation=90, fill='blue')

    def get_position_of_text(self, text_position, font):
        ascent_normal, descent_normal = font.getmetrics()
        total_text_height_normal = ascent_normal + descent_normal
        para_spacing_normal = 15
        start_x_book_list = 70
        start_y_book_list = 100
        para_height_normal = total_text_height_normal + para_spacing_normal
        return start_x_book_list, start_y_book_list + para_height_normal * (text_position + 1), para_height_normal


if __name__ == '__main__':
    # display_custom_text()
    image = Image.new('RGBA', (display.width, display.height), BACKGROUND_COLOR)
    menu_book_list = MenuBookList(display, image)
    # display_custom_text()
    menu_book_list.display_book_list()
    print("Clearing selection space")
    menu_book_list.clear_pointer_space()
    print("Drawing icon 0")
    # menu_book_list.draw_selection_icon(0)
    time.sleep(2)
    print("Drawing icon 1")
    # menu_book_list.draw_selection_icon(1)
    # blank_image= move_icon(blank_image)
    exit()
