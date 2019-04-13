"""
Utility functions relating to handling time events
"""
import datetime as dt
import os
import json

from src import err
from src import const


def strTimeNow():
   """
   Returns a string with the current time in the standard format given
   in const.
   """
   return dt.datetime.strftime(dt.datetime.now(), const.timeFormat)


def isTime(lastTime, frequency):
    """
    Will calculate whether to do something based on how frequent the action
    should be. E.g. if something should happen every 6 seconds and the last
    time it was completed was 5 seconds ago this will return False.
    
    Inputs:
        * lastTime => The timestamp of the last time the action was completed.
                      [datetime.datetime object]
        * frequency => The frequency at which to do the action.
                      [datetime.timedelta]
    
    Outputs:
        * boolean (whether to do the action), (datetime.datetime)
                                              the last time the action
                                              was carried out.
    
    """
    if type(lastTime) != dt.datetime:
        err.printLog("ERROR:  Wrong Format of datetime")
        return False, False
    timeNow = dt.datetime.now()
    if lastTime > timeNow:
        err.printLog("ERROR:  lastTime more than current time!")
        return False, False
    
    timeDiff = timeNow - lastTime
    if timeDiff > frequency:
        return True, timeNow
    else:
        return False, lastTime


def getLastTimes(key=False):
   """
   Will read the lastTimes filepath. If it is not there then this will
   return a dictionary with all values set to the current time.

   Inputs:
      * key => the name of the lastTime variable to get

   Outputs:
      * dependent on the value of key, either dict of all lastTimes or
        single lastTime.
   """
   if os.path.isfile(const.lastTimeFilepath):
      with open(const.lastTimeFilepath, 'r') as f:
         try:
            data = json.load(f)
         except json.JSONDecodeError:
            err.printLog("WARN: Reseting lastTimes dict as json is corrupted.")
            timeNow = strTimeNow()
            data = {i: timeNow for i in const.allLastTimeVals}
            
   else:  # defaults to current time
      timeNow = strTimeNow()
      data = {i: timeNow for i in const.allLastTimeVals}

   if key:
      if key in data:
         return dt.datetime.strptime(data[key], const.timeFormat)
      else:
         err.printLog("ERROR: key `%s` not available in the lastTimes dictionary" % key)
         msg = "\n\tKeys are:\n\t* %s" % "\n\t* ".join(const.allLastTimeVals)
         err.printLog(msg)
         return False
   data = {i: dt.datetime.strptime(data[i], const.timeFormat)
           for i in data}
   return data


def setLastTimes(key, value):
   """
   Will set the lastTimes dictionaries

   Inputs:
      * key => the name of the last time to change
               [str]
      * value => the value to which the last time should be changed.
                 [datetime.datetime]

   Outputs:
      * exit_code
   """
   if type(value) != dt.datetime:
      err.printLog("ERROR: wrong type given for value in lastTimes")
      return False
   if key not in const.allLastTimeVals:
      err.printLog("ERROR: key `%s` not in the allLastTimeVals" % key)
      msg = "\n\tKeys are:\n\t* %s" % "\n\t* ".join(const.allLastTimeVals)
      err.printLog(msg)
      return False

   lastTimes = getLastTimes()
   if lastTimes[key] != value:
      lastTimes[key] = value  # set new val
      # Should be strings for writing
      lastTimes = {i: dt.datetime.strftime(lastTimes[i], const.timeFormat)
                   for i in lastTimes}
      with open(const.lastTimeFilepath, 'w') as f:
          json.dump(lastTimes, f)

   return True

