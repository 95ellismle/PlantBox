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
   with open(const.files['syslog'], 'a') as f:
      timeNow = dt.datetime.strftime(dt.datetime.now(),
                                     const.timeFormat)
      f.write(timeNow + "|  " + msg + "\n")


def typeCheck(var, types, varName):
   """
   Will check if the type of the variable var is the same as types

   Inputs:
      var => any variable 
             [any]
      types => the allowed types
               [tuple, list or single type]
      varName => The name of the variable
                 [str]
   
   Outputs:
      * check result, error message
   """
   if type(varName) != str:
      msg = "ERROR: The type of the varName in the typeCheck function"
      msg += " is not a string!"
      printLog(msg)
      return False, False
   
   if type(types) == list:
      types = tuple(types)

   check = isinstance(var, types)
   msg = ""
   if not check:
      msg += "the type of variable %s is %s" % (varName, type(var))
      msg += ". It should be one of: %s" % ', '.join(str(i) for i in types)

   return check, msg
      
