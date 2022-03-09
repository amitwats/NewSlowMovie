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
from book_manager_2_data_2_db_manager import get_books_list, get_book_data

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
# display = MyDisplay(vcom=DEFAULT_VCOM, rotate="CCW", spi_hz=24000000, flip=False)
MIN_RECT_BOX_WIDTH = 400
MIN_RECT_BOX_HEIGHT = 400
MAX_RECT_BOX_WIDTH = 600
MAX_RECT_BOX_HEIGHT = 600


class MenuPageSelector:

    def __init__(self, book_data, display_obj, image_obj=None):
        self.display = display_obj
        self.image_obj = image_obj if image_obj else \
            Image.new('RGB', (self.display.width, self.display.height), color=BACKGROUND_COLOR)
        self.book_data = book_data

        self.RECT_BOX_WIDTH = min(max(display_obj.width * 0.6, MIN_RECT_BOX_WIDTH), MAX_RECT_BOX_WIDTH)
        self.RECT_BOX_HEIGHT = min(max(display_obj.width * 0.6, MIN_RECT_BOX_HEIGHT), MAX_RECT_BOX_HEIGHT)

        self.RECT_BOX_X_START = (display_obj.width - self.RECT_BOX_WIDTH) / 2
        self.RECT_BOX_Y_START = (display_obj.height - self.RECT_BOX_HEIGHT) / 2
        self.RECT_BOX_X_END = self.RECT_BOX_X_START + self.RECT_BOX_WIDTH
        self.RECT_BOX_Y_END = self.RECT_BOX_Y_START + self.RECT_BOX_HEIGHT

        self.char_count = 4

        self.digit_selector = []
        digit_selector_width = self.RECT_BOX_WIDTH / self.char_count
        digit_selector_height = self.RECT_BOX_HEIGHT
        self.digit_selector_index = 0

        for digit_selector_index in range(self.char_count):
            focused = digit_selector_index == 1
            digit_selector_x_start = self.RECT_BOX_X_START + digit_selector_index * digit_selector_width
            digit_selector_y_start = self.RECT_BOX_Y_START

            self.digit_selector.append(
                MenuSelector("0123456789", self.display, digit_selector_width, digit_selector_height,
                             digit_selector_x_start, digit_selector_y_start,
                             image_obj=self.image_obj, selected_char="0", focused=focused,
                             font_name=FONT_STANDARD, font_size=120))
        self.digit_selector_index = len(self.digit_selector)-1


        self.display_start()
        # self.selection_index_max = 0
        # self.POINTER_SPACE_X_START = display.width - 20
        # self.POINTER_SPACE_X_END = display.width - 50
        # self.POINTER_SPACE_Y_START = 0
        # self.POINTER_SPACE_Y_END = display.height
    def _set_digit_selector_index(self, index):
        self.digit_selector_index = index
        for index, sel in enumerate(self.digit_selector):
            sel.focused = index == self.digit_selector_index

    def display_start(self):
        self.display.frame_buf.paste(0xFF, box=(0, 0, self.display.width, self.display.height))

        image_draw = ImageDraw.Draw(self.image_obj)
        image_draw.rectangle([self.RECT_BOX_X_START, self.RECT_BOX_Y_START, self.RECT_BOX_X_END, self.RECT_BOX_Y_END],
                             outline='black', fill='white')
        for dig_sel in self.digit_selector:
            dig_sel.draw_selection_icon(image_draw)
        self.image_obj = ImageOps.mirror(self.image_obj)
        paste_coords = [0, 0]
        self.display.frame_buf.paste(self.image_obj, paste_coords)
        self.display.draw_partial(constants.DisplayModes.GC16)

    def move_focus_to_next_selector(self):
        self.digit_selector_index += 1
        self.digit_selector_index %= len(self.digit_selector)
        self._set_digit_selector_index(self.digit_selector_index)
        self.display_start()


    def move_focus_to_prev_selector(self):
        self.digit_selector_index -= 1
        self.digit_selector_index %= len(self.digit_selector)
        self._set_digit_selector_index(self.digit_selector_index)
        self.display_start()

    def current_selector_up(self):
        self.digit_selector[self.digit_selector_index].select_next()
        self.display_start()

    def current_selector_down(self):
        self.digit_selector[self.digit_selector_index].select_prev()
        self.display_start()

    # def get_current_selection(self):
    #     return self.list_books[self.selection_index]
    #
    # def display_book_list(self):
    #     # clearing image to white
    #     display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))
    #     start_x_heading = 70
    #     start_y_heading = 50
    #     image_draw = ImageDraw.Draw(self.image_obj)
    #
    #     font_H1 = ImageFont.truetype(FONT_STANDARD, FONT_H1_SIZE)
    #
    #     image_draw.text((start_x_heading, start_y_heading), 'Book List', font=font_H1, fill='black', )
    #
    #     font_normal = ImageFont.truetype(FONT_STANDARD, FONT_NORMAL_SIZE)
    #
    #     for index, book in enumerate(self.list_books):
    #         print(book)
    #         x_pos, y_pos, _ = self.get_position_of_text(index, font_normal)
    #         image_draw.text((x_pos, y_pos), book.folder,
    #                         font=font_normal, fill='black', )
    #
    #     self.image_obj = ImageOps.mirror(self.image_obj)
    #
    #     # TODO: this should be built-in
    #     dims = (display.width, display.height)
    #     print(f"Setting image dimensions to {dims}")
    #     paste_coords = [0, 0]
    #     display.frame_buf.paste(self.image_obj, paste_coords)
    #     display.draw_full(constants.DisplayModes.GC16)
    #     # display.draw_partial(constants.DisplayModes.DU)
    #
    # def clear_pointer_space(self):
    #     paste_coords = [0, 0]
    #     img_draw = ImageDraw.Draw(self.image_obj)
    #     clear_rect = (self.POINTER_SPACE_X_START, self.POINTER_SPACE_Y_START,
    #                   self.POINTER_SPACE_X_END, self.POINTER_SPACE_Y_END)
    #     # img_draw.rectangle(clear_rect, outline=BACKGROUND_COLOR, fill=BACKGROUND_COLOR)
    #     img_draw.rectangle(clear_rect, outline=BACKGROUND_COLOR, fill=(200, 200, 200, 120))
    #
    #     display.frame_buf.paste(self.image_obj, paste_coords)
    #     display.draw_partial(constants.DisplayModes.GC16)
    #
    # def draw_selection_icon(self):
    #     paste_coords = [0, 0]
    #     self.clear_pointer_space()
    #     text_x, text_y, text_height = self.get_position_of_text(self.selection_index,
    #                                                             ImageFont.truetype(FONT_STANDARD, FONT_NORMAL_SIZE))
    #     self.put_selection_icon(text_x, text_y + text_height * 0.4)
    #     display.frame_buf.paste(self.image_obj, paste_coords)
    #     display.draw_partial(constants.DisplayModes.GC16)
    #
    # def put_selection_icon(self, x, y):
    #     radius_icon = 9
    #     img_draw = ImageDraw.Draw(self.image_obj)
    #     img_draw.regular_polygon((self.POINTER_SPACE_X_END + radius_icon + 5, y - 2, radius_icon),
    #                              5, rotation=90, fill='blue')
    #
    # def get_position_of_text(self, text_position, font):
    #     ascent_normal, descent_normal = font.getmetrics()
    #     total_text_height_normal = ascent_normal + descent_normal
    #     para_spacing_normal = 15
    #     start_x_book_list = 70
    #     start_y_book_list = 100
    #     para_height_normal = total_text_height_normal + para_spacing_normal
    #     return start_x_book_list, start_y_book_list + para_height_normal * (text_position + 1), para_height_normal
    #
    # def change_selection(self):
    #     if self.selection_index < self.selection_index_max:
    #         self.selection_index += 1
    #
    # def select_next(self):
    #     if self.selection_index < self.selection_index_max:
    #         self.selection_index += 1
    #         self.draw_selection_icon()
    #
    # def select_previous(self):
    #     if self.selection_index > 0:
    #         self.selection_index -= 1
    #         self.draw_selection_icon()


class MenuSelector:
    def __init__(self, allowed_chars, display_obj, width, height, start_x, start_y,
                 image_obj=None, selected_char=None, focused=False, font_name=FONT_STANDARD, font_size=120):
        self.display = display_obj
        self.image_obj = image_obj if image_obj else \
            Image.new('RGB', (self.display.width, self.display.height), color=BACKGROUND_COLOR)
        self.allowed_chars = allowed_chars
        try:
            self.selected_char_index = self.allowed_chars.index(selected_char)
        except Exception:
            self.selected_char_index = 0
        self.width = int(width)
        self.height = int(height)
        self.start_x = int(start_x)
        self.start_y = int(start_y)
        self.focused = focused
        self.x_padding = 30
        self.font = ImageFont.truetype(font_name, font_size)
        ascent_normal, descent_normal = self.font.getmetrics()
        total_text_height_normal = ascent_normal + descent_normal

        self.y_padding = (self.height - total_text_height_normal) / 2
        # self.draw_selection_icon()

    def max_selection_index(self):
        return len(self.allowed_chars) - 1

    def select_next(self):
        if self.selected_char_index < self.max_selection_index():
            self.selected_char_index += 1
        else:
            self.selected_char_index = 0
        self.draw_selection_icon()

    def select_previous(self):
        if self.selected_char_index > 0:
            self.selected_char_index -= 1
        else:
            self.selected_char_index = self.max_selection_index()
        self.draw_selection_icon()

    def get_selected_char(self):
        return self.allowed_chars[self.selected_char_index]

    def draw_selection_icon(self, image_draw=None):
        # self.display.frame_buf.paste(0xFF, box=(0, 0, self.width, self.height))
        if not image_draw:
            image_draw = ImageDraw.Draw(self.image_obj)
        image_draw.rectangle((self.start_x, self.start_y, self.start_x + self.width, self.start_y + self.height),
                             outline='black', fill='white')

        image_draw.text((self.start_x + self.x_padding, self.start_y + self.y_padding),
                        self.get_selected_char(), fill='black', font=self.font, align='center')
        self.draw_focused_elements(image_draw)

        # if self.focused:
        #     self.draw_focused_elements(image_draw)
        self.image_obj = ImageOps.mirror(self.image_obj)
        # paste_coords = [self.start_x, self.start_y]
        paste_coords = [0, 0]
        # self.display.frame_buf.paste(self.image_obj, paste_coords)
        # self.display.draw_partial(constants.DisplayModes.GC16)

        pass

    def draw_focused_elements(self, image_draw):
        # image_draw = ImageDraw.Draw(self.image_obj)

        fill_color = 'black' if self.focused else 'white'

        image_draw.regular_polygon((self.start_x + self.width / 2, self.start_y + 30, 15),
                                   3, rotation=0, fill=fill_color)
        #     img_draw.regular_polygon((self.POINTER_SPACE_X_END + radius_icon + 5, y - 2, radius_icon),
        #                              5, rotation=90, fill='blue')

        image_draw.regular_polygon((self.start_x + self.width / 2, self.start_y + self.height - 30, 15),
                                   3, rotation=180, fill=fill_color)
        # selection_rect = Image.open(os.path.join(constants.IMAGE_PATH, 'selection_rect.png'))


if __name__ == '__main__':
    # display_custom_text()
    display = MyDisplay(vcom=DEFAULT_VCOM, rotate="CCW", spi_hz=24000000, flip=False)

    image = Image.new('RGBA', (display.width, display.height), BACKGROUND_COLOR)

    # menu_book_list = MenuBookList(book_list, display, image)
    book_data = get_book_data(1)
    page_selector = MenuPageSelector(book_data, display)
    # page_selector.draw_selection_icon()
    time.sleep(2)
    page_selector.move_focus_to_next_selector()
    time.sleep(2)
    page_selector.move_focus_to_prev_selector()
    time.sleep(2)
    page_selector.move_focus_to_prev_selector()
    time.sleep(2)
    page_selector.move_focus_to_next_selector()
    time.sleep(2)
    page_selector.current_selector_up()
    time.sleep(2)
    page_selector.current_selector_down()


    # blank_image= move_icon(blank_image)
    exit()
