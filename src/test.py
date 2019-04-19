import time
import os

from src import err
from src import const

def testLightsFuncs(lightsMod):
    """
    Will try using the lightsOn and lightsOff functions and give feedback.

    Inputs:
        *relayPins => the pins which the relay mods are plugged into
        * lightsMod => the lights Module that has switching on and off funcs
    """
    # Test the lights turning on
    working = lightsMod.lightsOn(const.relayPins)
    if not working:
        raise SystemExit("Lights not turning on!")
    time.sleep(5)

    # Test the lights turning off
    working = lightsMod.lightsOff(const.relayPins)
    if not working:
        raise SystemExit("Lights not turning off!")
    time.sleep(1)


def testUSBAddress():
   """
   Will check if the USB drive is recognised and mounted. It must be
   mounted at const.permDataStoragePath.
   """
   if not os.path.isdir(const.permDataStoragePath):
      err.printLog("ERROR: USB drive not mounted at %s" % const.permDataStoragePath)
      return False
   else:
      err.printLog("INFO: USB drive found at %s" % const.permDataStoragePath)
      return True
