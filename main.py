import RPi.GPIO as gpio
import picamera as picam

import datetime as dt
import time

from src import arduino_utils as arduino
from src import light_utils as lights
from src import test as testLib
from src import err
from src import const
from src import time_utils as tutils
from src import data_utils as dutils
from src import camera_utils as mPiCam

carryOn = True  # The variable that decides to exit the loop

## Initialisation

# Init gpio
gpio.setmode(gpio.BOARD)
for pin in const.relayPins:
   gpio.setup(pin, gpio.OUT)
# Init bluetooth
sock = arduino.initBluetooth(const.macAddress, const.port)
# Init camera
cam = picam.PiCamera()
pic = mPiCam.Picture(cam)

####

# Tests the lightsOn and Off functions -They should flash on and off
testLib.testLightsFuncs(lights)
carryOn = testLib.testUSBAddress()

strs = ""
data = dutils.getCurrData()
err.printLog("INFO: Start Loop")

try:
    while carryOn is not False:
       # Get the dict that stores when things were last done.
       lastTimes = tutils.getLastTimes()
       if lastTimes is False:
         carryOn = False
       
       # Check if the lights should be on every second
       carryOn = tutils.doEvent("lightCheck", lights.controlLights,
                                dt.timedelta(0, 1), const.relayPins)

       ## Read data                   -every 2 sec
       #carryOn = tutils.doEvent("dataGet", arduino.getData,
       #                         dt.timedelta(0, 2), *(sock, data, strs))

       ## Move the data files       -every 0.5 days
       ##    This is done every so often so we don't store the full
       ##     dataframe in the very limited memory.
       #carryOn = tutils.doEvent("dataMove", dutils.moveCSVData,
       #                         dt.timedelta(0.5), data)

       ## Take a picture           -every 0.1 days
       #carryOn = tutils.doEvent("takePic", pic.capture,
       #                         dt.timedelta(0.1))
      
       ### Move pics to USB
       ##carryOn = tutils.doEvent("movePics", dutils.movePics,
       ##                         dt.timedelta(1))

       time.sleep(2)  # Needs to be < 3 second for timestamp to be accurate

except KeyboardInterrupt:
    err.printLog("INFO: Keyboard exit")
 
# Safely close bluetooth
sock.close()
lights.lightsOff(const.relayPins)
gpio.cleanup()
