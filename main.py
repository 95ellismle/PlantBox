import RPi.GPIO as gpio
import picamera as picam
import Adafruit_DHT

import datetime as dt
import time
import os
import signal
import numpy as np

from src import const
from src import err
from src import light_utils as lUt

# Add a feature to turn off/on certain features


def finalise():
    """
    Will finalise the whole code (cleanup the gpio pins, handle anything else
    that needs to be cleaned up at the end of the code.
    """
    gpio.cleanup()


def handle_exit(signal, frame):
    """
    Will handle exitting the code safely after a SIGTERM (kill)
    signal has been passed to python.
    """
    finalise()
    raise SystemExit("Exitting Gracefully")


## Initialisation
print("Initialising.\n")
signal.signal(signal.SIGTERM, handle_exit)
gpio.setmode(gpio.BCM)
for pinType in ['Flash', 'GrowLight']:
    gpio.setup(const.gpioPins[pinType], gpio.OUT)
    lUt.switchLight(pinType, 'off')



# Check temperature every 5 minutes
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


def getNewFileNumber(directory, numZeros=5, extension="jpg"):
    """
    Will look into a directory and try to find any filenames with
    the given extension which is comprised solely of numbers. The
    function will then return a filename which is the maximum number
    + 1.  It will also add a number of zero characters in front of it
    to make it easier to stitch together the files with ffmpeg.
    """
    ext = extension
    if ext[0] != '.':
        ext = ".%s" % ext

    # Find the filename for the pic
    imgFiles = [i for i in os.listdir(directory) if ext in i]
    # Get all the current filenames (filenumbers)
    imgNums = [i.strip(ext) for i in imgFiles]
    imgNums = [int(i) for i in imgNums if is_num(i)]
    # Add 1 to the maximum number
    newNum, numZeros = 0, 5
    if imgNums:
        newNum = max(imgNums) + 1
    # Add some zeros behind it to make it easy to stitch together into a timelapse
    strNum = "0" * (numZeros - len(str(newNum)))
    strNum = "%s%i" % (strNum, newNum)

    fileName = "%s/%s%s" % (directory, strNum, ext)
    return fileName



def takePic(test=False):
    """
    Will take a picture using the picamera and the picamera module.
    This involves switching off the grow light, switching on the flash
    finding the correct filename and then taking the pic and storing it
    under that filename.
    """
    # Turn off grow lights and turn on flash
    lUt.switchLight('GrowLight', 'off')
    lUt.switchLight('Flash', 'on')

    # The with statement seems to work fine being called in a loop.
    # Memory leaks will be seen if picam is not properly closed and the
    # code will crash.
    with picam.PiCamera() as cam:
        cam.resolution = (1640, 1232)
        cam.start_preview()
        time.sleep(5)
        
        fileName = getNewFileNumber(const.imgFolder)
        if test:
            fileName = "testPic.jpg"
            if os.path.isfile(fileName): os.remove(fileName)

        # Actually take the picture
        cam.capture(fileName)
        cam.stop_preview()

    err.printLog("INFO: Taking pic `%s'" % fileName)
    lUt.switchLight('Flash', 'off')


def getTempHumid():
    """
    Will get the temperature and humidity from the DHT's in the grow tent. 
    """
    # Get readings
    allHumid, allTemp = [], []
    failedPins = []
    for sensor, pin in const.sensorPins['DHT']:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        if humidity is None or temperature is None:
            failedPins.append((pin, sensor, 'humidity'))
            failedPins.append((pin, sensor, 'temperature'))
        else:
            allHumid.append(humidity)
            allTemp.append(temperature)
    
    # Report any failed pins
    for pin, sensor, measurement in failedPins:
        msg = "WARNING | SENSOR BROKEN\n"
        msg += "\t Pin = %i\n" % pin
        msg += "\t Type = DHT%s" % (str(sensor))
        msg += "\t Measurement = %s" % measurement
        err.printLog(msg)

    # Do some analysis (exclude outliers and average)
    tMean, hMean = allTemp[0], allHumid[0]
    tBest, hBest = None, None
    if len(allHumid) > 1:
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
    dateT = dt.datetime.now()
    if 22 >= dateT.hour >= 7:
        if dateT.hour == 22 and dateT.minute <= 30:
            return True
        elif dateT.hour != 22:
            return True

    return False

# Testing the devices
try:
    # Test the Grow Light
    print("Testing the Grow Light")
    lUt.switchLight("GrowLight", 'on')
    time.sleep(5)
    lUt.switchLight("GrowLight", 'off')
   
    # Test the flash and the camera
    print("Testing the camera and the flash.")
    takePic(test=True)
   
    # Test the DHT sensors
    print("Testing the DHT sensors")
    Hdata, Tdata = getTempHumid()
    print("Temperatures = (%s)" % ', '.join([str(i) for i in Tdata['all']]))
    print("Humidities = (%s)" % ', '.join([str(i) for i in Hdata['all']]))
    print(Hdata)
    print(Tdata)
except KeyboardInterrupt:
    print("Exitting Gracefully")
    finalise()
    raise SystemExit()
print("Finished testing, if anything didn't work please stop the code and fix it")


# Actually do the loop
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
        if lightShouldBeOn():
            lUt.switchLight("GrowLight", "on")
        else:
            lUt.switchLight("GrowLight", "off")
        
        time.sleep(1)

    except KeyboardInterrupt:
        print("Exitting Loop")
        break


finalise()

