import RPi.GPIO as gpio
import picamera as picam

import datetime as dt
import time

from src import getDataFromArduino as arduino
from src import lightControl as lights
from src import test as testLib
from src import err
from src import const
from src import timeutils as tutils
from src import datautils as dutils
from src import piCamStuff as mPiCam

carryOn = True  # The variable that decides to exit the loop

# Init everything (relay pins, camera and bluetooth)
gpio.setmode(gpio.BOARD)
for pin in const.relayPins:
   gpio.setup(pin, gpio.OUT)
s = arduino.initBluetooth(const.macAddress, const.port)
# Init camera
cam = picam.PiCamera()
pic = mPiCam.Picture(cam)

# Tests the lightsOn and Off functions -They should flash on and off
testLib.testLightsFuncs(lights)
carryOn = testLib.testUSBAddress()

strs = ""
data = dutils.getCurrData()
err.printLog("INFO: Start Loop")
#picsTaken = []

try:
    while carryOn is not False:
       # Get the dict that stores when things were last done.
       lastTimes = tutils.getLastTimes()
       if lastTimes is False:
         carryOn = False

       # Control the lights          - every 5 sec
       doLights, newLastTime = tutils.isTime(lastTimes['lightCheck'],
                                             dt.timedelta(0, 1))
       if newLastTime is False:  # catch errors to exit safely
         carryOn = False
       if doLights:
          carryOn = lights.controlLights(const.relayPins)
       tutils.setLastTimes('lightCheck', newLastTime)


       # Read data                   -every 2 sec
       doRead, newLastTime = tutils.isTime(lastTimes['dataGet'],
                                           dt.timedelta(0, 2))
       if newLastTime is False:  # catch errors to exit safely
         carryOn = False
       # Remember to save the time the thing was changed
       tutils.setLastTimes('dataGet', newLastTime)
       if doRead:
          strs += s.recv(10).decode('utf-8')
          strs, data = arduino.parseStr(strs, data)


       # Move the data files       -every 0.5 days
       #    This is done every so often so we don't store the full
       #     dataframe in the very limited memory.
       doMove, newLastTime = tutils.isTime(lastTimes['dataMove'],
                                           dt.timedelta(0.5))
       if newLastTime is False:  # catch errors to exit safely
         carryOn = False
       tutils.setLastTimes('dataMove', newLastTime)
       if doMove:
          data = dutils.moveCSVData(data)
       if data is False:
         carryOn = False

       # Take a picture           -every 0.1 days
       doTakePic, newLastTime = tutils.isTime(lastTimes['takePic'],
                                              dt.timedelta(0.1))
       if newLastTime is False:
         carryOn = False
       if doTakePic:
          pic.capture()
          carryOn = pic.carryOn  # Can improve this by checking for filepaths etc...
          err.printLog("INFO: Taking Pic")
          carryOn = dutils.moveJPG(pic.imgFilePath)
       tutils.setLastTimes('takePic', newLastTime)

       time.sleep(2)  # Needs to be < 3 second for timestamp to be accurate

except KeyboardInterrupt:
    err.printLog("INFO: Keyboard exit")
 
# Safely close bluetooth
s.close()
lights.lightsOff(const.relayPins)
gpio.cleanup()
