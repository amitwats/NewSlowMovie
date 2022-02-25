# NewSlowMovie
Integrates two projects for one nice functional output of a slowmovie. Built for the 10.3 inch screen from WaveShare
https://www.waveshare.com/wiki/10.3inch_e-Paper_HAT_(D)

## IT8951 (https://github.com/GregDMeyer/IT8951)
This Python 3 module implements a driver for the IT8951 e-paper controller, via SPI.
The driver was developed using the 6-inch e-Paper HAT from Waveshare. It hopefully will work for
other (related) hardware too.

To install, clone the repository, enter the directory and run
```
pip install -r requirements.txt
export USE_CYTHON="True"
pip install --upgrade cython
pip install ./
```
Make sure that SPI is enabled in `raspi-config`. For some examples of usage, take a look at the integration tests.
### Notes on performance
#### VCOM value
You should try setting different VCOM values and seeing how that affects the performance of your display. Every
one is different. There might be a suggested VCOM value marked on the cable of your display.
#### Data transfer
You might be able to squeeze some extra performance out of the data transfer by increasing the SPI
clock frequency. The SPI frequency for transferring pixel data is by default set at 24 MHz, which is the maximum
stated in the IT8951 chip spec [here](https://www.waveshare.com/w/upload/1/18/IT8951_D_V0.2.4.3_20170728.pdf)
(page 41). But, you could try setting higher and seeing if it works anyway. It is set by passing the `spi_hz` argument to the Display or EPD classes (see example in `tests/integration/tests.py`).
### Updates for version 0.1.0
For this version the backend was rewritten, so that the SPI communication happens directly
by communicating with the Linux kernel through `/dev/spidev*`. This means:
 - `sudo` no longer required
 - requires neither the `bcm2835` C library nor the `spidev` Python module
 - data transfer is way faster than before!
### Hacking
If you modify `spi.pyx`, make sure to set the `USE_CYTHON` environment variable before building---otherwise your
changes will not be compiled into `spi.c`.

## SlowMovie (https://github.com/TomWhitwell/SlowMovie)
### Python / Raspberry Pi interpretation of Bryan Boyer's Very Slow Movie Player  
Full writeup of this project here:   
https://medium.com/@tomwhitwell/how-to-build-a-very-slow-movie-player-in-2020-c5745052e4e4

Bryan's original post here:  
https://medium.com/s/story/very-slow-movie-player-499f76c48b62 

## Important references
https://www.waveshare.com/wiki/10.3inch_e-Paper_HAT
https://github.com/dankarlin/NewSlowMovie


## Configure new Pi
Configure New RPi
1) install Raspbian lite

2) Create a file wpa_supplicant.conf  with the following config and put it in the location /boot to enable wifi. When in  this folder it will automatically be copied to /etc/wpa_supplicant/wpa_supplicant.conf on first boot.
```
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
  ssid="YOURSSID"
  scan_ssid=1
  psk="YOURPASSWORD"
  key_mgmt=WPA-PSK
}
```
ref: https://raspberrytips.com/raspberry-pi-wifi-setup/

3) Create an empty file called ssh in the  boot partition(root directory) to enable SSH

4) In /boot/config.txt uncomment the line or add the line 
```
dtparam=spi=on
```
5) using https://www.waveshare.com/wiki/10.3inch_e-Paper_HAT
