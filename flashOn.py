"""
This simple script will turn on the flash in the grow tent and turn off the grow light
in order to do some work in it. The main.py code will have to be stopped first though
"""
from src import light_utils as lUt

import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setup(4, gpio.OUT)
gpio.setup(17, gpio.OUT)

lUt.switchLight("GrowLight", "off")
lUt.switchLight("Flash", "on")

