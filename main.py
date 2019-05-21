import RPi.GPIO as gpio
import picamera as picam
import Adafruit_DHT

import datetime as dt
import time
import os

from src import const
from src import err
from src import light_utils as lUt

## Initialisation
gpio.setmode(gpio.BCM)
for pinType in ['Flash', 'GrowLight']:
    gpio.setup(const.gpioPins[pinType], gpio.OUT)
    lUt.switchLight(pinType, 'off')

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


def is_num(Str):
    """
    Checks whether a string can be a number
    """
    try:
        float(Str)
        return True
    except:
        return False


def takePic():
    """
    Will take a picture using the picamera and the picamera module.
    """
    # Turn off grow lights and turn on flash
    lUt.switchLight('GrowLight', 'off')
    lUt.switchLight('Flash', 'on')

    cam = picam.PiCamera()
    cam.start_preview()
    time.sleep(5)
    
    imgFiles = [i for i in os.listdir(const.imgFolder) if '.jpg' in i]
    imgNums = [i.strip('.jpg') for i in imgFiles]
    imgNums = [int(i) for i in imgNums if is_num(i)]
    newNum = 0
    if imgNums:
        newNum = max(imgNums) + 1
    fileName = "%s/%i.jpg" % (const.imgFolder, newNum)

    cam.capture(fileName)
    cam.stop_preview()
    
    lUt.switchLight('Flash', 'off')


def getTempHumid():
    """
    Will get the temperature and humidity from the DHT's in the grow tent. 
    """
    allHumid, allTemp = [], []
    failedPins = []
    for sensor, pin in const.sensorPins['DHT']:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        if humidity is None:
            failedPins.append((pin, sensor, 'humidity'))
        if temperature is None:
            failedPins.append((pin, sensor, 'temperature'))
        allHumid.append(humidity)
        allTemp.append(temperature)
    
    # Report any failed pins
    for pin, sensor, measurement in failedPins:
        msg = "WARNING | SENSOR BROKEN\n"
        msg += "\t Pin = %i\n" % pin
        msg += "\t Type = %s" % (str(sensor))
        msg += "\t Measurement = %s" % measurement
        err.PrintLog(msg)

    # Do some analysis (exclude outliers and average)
    tStd, hStd = np.std(allHumid) * 2, np.std(allTemp) * 2
    tMean, hMean = np.mean(allTemp), np.mean(allHumid)
    tBest = [t for t in allTemp if tMean - tStd < t < tMean + tStd]
    hBest = [h for h in allHumid if hMean - hStd < h < hMean + hStd]
    tBest = np.mean(tBest)
    hBest = np.mean(hBest)
    
    humidData = {'all': allHumid, 'mean': hMean, 'real': hBest}
    tempData = {'all': allTemp, 'mean': tMean, 'real': tBest}
    return humidData, tempData


def lightShouldBeOn():
    """
    Determine whether the light should be on or not based on the time, temperature,
    how long it has been on already and how long is left in the day.
    """

donePic = False
while True:
    
    try:
        # The camera
        if dt.datetime.now().minute % 30 == 0 and not donePic:
            takePic()
            donePic = True
        elif dt.datetime.now().minute % 30 != 0:
            donePic = False

        # The grow lights
        if 21 >= dt.datetime.now().hour >= 7:
            lUt.switchLight('GrowLight', 'on')
        else:
            lUt.switchLight('GrowLight', 'off')
        time.sleep(1)
    except KeyboardInterrupt:
        break


gpio.cleanup()

