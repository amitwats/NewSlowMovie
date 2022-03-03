#!/usr/bin/python

import time
import RPi.GPIO as GPIO

gpio_buttons = [21, 20, 16, 26, 19, 13, 6, 12]
GPIO.setmode(GPIO.BCM)

# set GPIO buttons as pull down
for btn in gpio_buttons:
    GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    states = [GPIO.input(btn) for btn in gpio_buttons]
    print(states)
    time.sleep(0.1)
