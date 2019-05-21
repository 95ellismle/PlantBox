import RPi.GPIO as gpio
import picamera as picam

import datetime as dt
import time

from src import consts
from src import light_utils as lUt

## Initialisation
gpio.setmode(gpio.BCM)
for pinType in ['Flash', 'GrowLight']:
    gpio.setup(consts.gpioPins[pinType], gpio.OUT)
    lUt.switchLight(consts.gpioPins[pinType], 'off')

# Take a picture every 30 minutes
#   * Turn off grow lights
#   * Turn on flash
#   * take picture (use raspistill for now)
#   * Turn off flash (don't change grow lights)

# Check temperature every cycle
#   * Check temperature from both sensors
#   * If difference between sensors is very high (2C) then produce warning
#   * Warning should print to log file.

# Switch grow lights on if it is the right time
#   * Grow lights can be on for 14hrs a day 07:00 - 22:30
#   * Turn them off if temperature is too hot (need at least 12hrs)
#   * Turn them on at 07:00 and keep them on until the tent is above 20C
#   * Count the time they've been on and the time left in the day.
#   * If 12 - (totalTimeOn + lightTimeLeft) <= 0: keep grow lights on
#   * else: turn off grow lights for 10 mins
#   * If temperature > 17.5: turn on extractor fan
#   * Turn them off when taking a picture


def takePic():
    """
    Will take a picture using the picamera and the picamera module.
    """
    # Turn off grow lights and turn on flash
    lUt.switchLight(consts.gpioPins['GrowLight'], 'off')
    lUt.switchLight(consts.gpioPins['Flash'], 'on')

    cam = picam.PiCamera()
    cam.start_preview()
    time.sleep(5)
    fUt.getFileName('./Img')
    cam.capture(fileName)
    cam.stop_preview()
    
    lUt.switchLight(consts.gpioPins['Flash'], 'off')

gpio.cleanup()

