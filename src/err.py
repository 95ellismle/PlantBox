"""
Functions that aren't specific to any particular part of the code but can be used in all of it.
"""
import datetime as dt

from src import const

def printLog(msg):
   """
   Will replace the print function and print things to a log file.

   Inputs:
      * msg => message to print
   """
   with open(const.logFile, 'a') as f:
      timeNow = dt.datetime.strftime(dt.datetime.now(),
                                     const.timeFormat)
      f.write(timeNow + "|  " + msg + "\n")
