


from PIL import Image, ImageDraw
#!/usr/bin/python
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
    # img = ImageOps.mirror(Image.open(img_path))#not sure why my image is mirrored so I'm mirroring it here
    # ImageDraw
    blank_image = Image.new('RGBA', (display.width, display.height), 'white')
    img_draw = ImageDraw.Draw(blank_image)
    img_draw.rectangle((70, 50, 270, 200), outline='red', fill='blue')
    img_draw.text((70, 250), 'Hello World', fill='green')
    # blank_image.save('drawn_image.jpg')
    img_draw=ImageOps.mirror(img_draw)

    # TODO: this should be built-in
    dims = (display.width, display.height)
    print(f"Setting image dimensions to {dims}")
    # img.thumbnail(dims)
    # paste_coords = [dims[i] - img.size[i] for i in (0, 1)]  # align image with bottom of display
    paste_coords= [0, 0]
    # display.frame_buf.paste(img, paste_coords)
    # display.frame_buf.paste(blank_image, paste_coords)
    display.frame_buf.paste(img_draw, paste_coords)

    display.draw_full(constants.DisplayModes.GC16)
    # display.draw_partial(constants.DisplayModes.DU)



def display_image_8bpp(display, img_path):
    print('Displaying "{}"...'.format(img_path))

    # clearing image to white
    display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))

    img = ImageOps.mirror(Image.open(img_path))#not sure why my image is mirrored so I'm mirroring it here
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

if __name__ == '__main__':

    #number of args passed
    # if len(sys.argv) > 1:
    #     for i in range(1, len(sys.argv)):
    #         print("Argument: {}".format(sys.argv[i]))
    #         display_image_8bpp(display, sys.argv[i])
    #         n = 2
    #         time.sleep(n)
    #
    #     display._set_rotate("CW")
    #     for i in range(1, len(sys.argv)):
    #         print("Argument: {}".format(sys.argv[i]))
    #         display_image_8bpp(display, sys.argv[i])
    #         n = 2
    #         time.sleep(n)
    display_custom_text()

    # for mode in rotate_list:
    #     display._set_rotate(mode)
    #     display_image_8bpp(display, sys.argv[1])

    # for i in range(5):
    #     # display._set_rotate(rotate_list[i])
    #     # display_image_8bpp(display, '/home/pi/NewSlowMovie/Sadhguru.png')
    #     if not sys.argv[1]:
    #         image_loc = "/home/pi/NewSlowMovie/indrajal/001.jpg"
    #     else:
    #         image_loc = sys.argv[1]
    #
    #     display_image_8bpp(display, image_loc)
    #
    #     # Wait for n seconds
    #     n = 2
    #     time.sleep(n)

    exit()




