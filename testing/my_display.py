from IT8951.constants import DEFAULT_VCOM, PixelModes
from IT8951.display import AutoDisplay
from IT8951.interface import EPD


class MyDisplay(AutoDisplay):
    '''
    This class initializes the EPD, and uses it to display the updates
    '''

    def __init__(self, epd=None, vcom=DEFAULT_VCOM,
                 bus=0, device=0, spi_hz=24000000,
                 **kwargs):

        if epd is None:
            if EPD is None:
                raise RuntimeError('Problem importing EPD interface. Did you build the '
                                   'backend with "pip install ./" or "python setup.py '
                                   'build_ext --inplace"?')

            epd = EPD(vcom=vcom, bus=bus, device=device, data_hz=spi_hz)

        self.epd = epd
        print(f"The width is  {self.epd.width} and the height is {self.epd.height}")

        AutoDisplay.__init__(self, self.epd.width, self.epd.height, **kwargs)

    def update(self, data, xy, dims, mode, pixel_format=PixelModes.M_4BPP):

        # these modes only use two pixels, so use a more dense packing for them
        # TODO: 2BPP doesn't seem to refresh correctly?
        # if mode in low_bpp_modes:
        #     pixel_format = PixelModes.M_2BPP
        # else:
        #     pixel_format = PixelModes.M_4BPP

        # send image to controller
        self.epd.wait_display_ready()
        self.epd.load_img_area(
            data,
            xy=xy,
            dims=dims,
            pixel_format=pixel_format
        )

        # display sent image
        self.epd.display_area(
            xy,
            dims,
            mode
        )

