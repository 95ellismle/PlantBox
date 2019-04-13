import RPi.GPIO as gpio
import datetime as dt

from src import err 

OnValue = False  # False turns lights on 
OffValue = True  # True turns lights off


def lightShouldBeOn(relayPins):
    """
    Determines if any of the lights should be on.

    If so return True; else return False. This function
    returns a list where each element corresponds to a
    grow light. E.g. [True, True] for 2 grow lights
    would turn all grow lights on. [True, False] would
    turn light 1 on and light 2 off.

    Inputs:
        * relayPins => the pin numbers of the relays
    """
    timeNow = dt.datetime.now()
    minsOffInHour = 5
    lightsOffMin = [(i % (60/minsOffInHour)) * minsOffInHour for i in range(len(relayPins))]
    if ( 9 <= timeNow.hour <= 24):
         returner = [True] * len(relayPins)
         for i in range(len(relayPins)):
             if (lightsOffMin[i] < timeNow.minute <= lightsOffMin[i] + minsOffInHour):
                 returner[i] = False
         return returner

    return [False]*len(relayPins)


def lightsOn(pins):
   """
   Will turn the lights associated with inputted pins on.
   """
   if isinstance(pins, (list, tuple)):
      for pin in pins:
         gpio.output(pin, OnValue)
   elif type(pins) == int:
      gpio.output(pins, OnValue)
   else:
      err.printLog("pins type = %s [should be int or list]" % type(pins))
      err.printLog("Wrong type inputted for pins")
      return False
   return True


def lightsOff(pins):
   """
   Will turn the lights associated with inputted pins on.
   """
   if isinstance(pins, (list, tuple)):
      for pin in pins:
         gpio.output(pin, OffValue)
   elif type(pins) == int:
      gpio.output(pins, OffValue)
   else:
      err.printLog("pins type = %s [should be int or list]" % type(pins))
      err.printLog("Wrong type inputted for pins")
      return False
   return True


def controlLights(relayPins):
    """
    Will actually handle the lights switching on and off.
    """
    whichLightsOn = lightShouldBeOn(relayPins)
    # Turn lights on first before turning lights off
    #  to make the transition smoother.
    returner = True
    for lightNum, isOn in enumerate(whichLightsOn):
        if isOn:
            returner *= lightsOn(relayPins[lightNum])
    for lightNum, isOn in enumerate(whichLightsOn):
        if not isOn:
            returner *= lightsOff(relayPins[lightNum])
    return returner
