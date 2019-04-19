import RPi.GPIO as gpio
#import picamera as picam

import datetime as dt
import time
import os  # only for camera can move

from src import arduino_utils as arduino
from src import light_utils as lights
from src import test as testLib
from src import err
from src import const
from src import time_utils as tutils
from src import data_utils as dutils
#from src import camera_utils as mPiCam

carryOn = True  # The variable that decides to exit the loop

# Init everything (relay pins, camera and bluetooth)
gpio.setmode(gpio.BOARD)
for pin in const.relayPins:
   gpio.setup(pin, gpio.OUT)
sock = arduino.initBluetooth(const.macAddress, const.port)
# Init camera
#cam = picam.PiCamera()
#pic = mPiCam.Picture(cam)

# Tests the lightsOn and Off functions -They should flash on and off
testLib.testLightsFuncs(lights)
carryOn = testLib.testUSBAddress()

strs = ""
data = dutils.getCurrData()
err.printLog("INFO: Start Loop")
#picsTaken = []

try:
    count = 0
    while carryOn is not False:
       print("\n\t---\t\n")
       # Get the dict that stores when things were last done.
       lastTimes = tutils.getLastTimes()
       if lastTimes is False:
         carryOn = False

       # Control the lights          - every 5 sec
       doLights, newLastTime = tutils.isTime(lastTimes['lightCheck'],
                                             dt.timedelta(0, 2))
       if newLastTime is False:  # catch errors to exit safely
         carryOn = False
       if doLights:
          carryOn = lights.controlLights(const.relayPins)
          err.printLog("INFO: checking light state")
       tutils.setLastTimes('lightCheck', newLastTime)


       # Read data                   -every 2 sec
       doRead, newLastTime = tutils.isTime(lastTimes['dataGet'],
                                           dt.timedelta(0, 2))
       if newLastTime is False:  # catch errors to exit safely
         carryOn = False
       # Remember to save the time the thing was changed
       tutils.setLastTimes('dataGet', newLastTime)
       if doRead:
          strs, data = arduino.getData(sock, data, strs)
          err.printLog("INFO: getting data")


       # Move the data files       -every 0.5 days
       #    This is done every so often so we don't store the full
       #     dataframe in the very limited memory.
       doMove, newLastTime = tutils.isTime(lastTimes['dataMove'],
                                           dt.timedelta(0.5))
       if newLastTime is False:  # catch errors to exit safely
         carryOn = False
       tutils.setLastTimes('dataMove', newLastTime)
       if doMove:
          err.printLog("INFO: moving data files")
          data = dutils.moveCSVData(data)
       if data is False:
         carryOn = False


       # Take a picture           -every 0.1 days
       doTakePic, newLastTime = tutils.isTime(lastTimes['takePic'],
                                               dt.timedelta(0.1))
       if newLastTime is False:
         carryOn = False
       tutils.setLastTimes('takePic', newLastTime)
       if doTakePic:
         err.printLog("INFO: taking picture")
         count += 1
         os.system("raspistill -o ./Img/%i.jpg" % count)

       time.sleep(2)  # Needs to be < 3 second for timestamp on data to be accurate

except KeyboardInterrupt:
    err.printLog("INFO: Keyboard exit")
 
# Safely close bluetooth
sock.close()
lights.lightsOff(const.relayPins)
gpio.cleanup()
