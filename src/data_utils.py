"""
Contains functions that aid in general data organisation like moving files around etc...
"""
import os
import shutil
import datetime as dt
import pandas as pd

from src import const
from src import err
from src import time_utils as tutils


def moveCSVData(currData):
   """
   Will move the current data file for permanent storage on the USB pen.

   Outputs:
      * returns new data object (or bad exit code)
   """
   currPath = const.dataFilepath

   # Let this error slide a couple of times
   if not os.path.isfile(currPath):
      const.badPathWarnings += 1
      return currData
   if const.badPathWarnings > 3:
      err.printLog("ERROR: The data file hasn't been created")
      return False

   # Format the date and time to make a filename
   timeNow = tutils.strTimeNow().replace(" ", "_")
   timeNow = tutils.strTimeNow().replace(":", "x")
   timeNow = timeNow.replace("/", "-")
   newPath = "%s/%s.csv" % (const.permDataStoragePath,
                            timeNow)
   carryOn = moveFile(currPath, newPath)
   if carryOn is False:
      return False

   return getCurrData()


def moveFile(currFile, newFile):
   """
   Will move a file to the USB.

   Inputs:
      * currFile => the current file that need moving
      * newFile => the new filepath for the file

   Outputs:
      exit_code
   """
   if not os.path.isfile(currFile):
      msg = "ERROR: Can't find file %s" % currFile
      err.printLog(msg)
      return False

   newFolder = newFile[ :newFile.rfind('/')]
   if not os.path.isdir(newFolder):
      msg = "ERROR: Can't find folder %s" % newFolder
      err.printLog(msg)
      return False

   try:
      shutil.move(currFile, newFile)
   except PermissionError as e:
      msg = "ERROR: you don't have permissions to move file "
      msg += "%s to %s" % (currFile, newFile)
      msg += "\n\terror = %s" % (str(e))
      err.printLog(msg)
      return False
   except Exception as e:
      msg = "ERROR: an error occured when trying to move"
      msg += " file %s to %s" % (currFile, newFile)
      msg += "\n\terror = %s" % (str(e))
      err.printLog(msg)
      return False
   finally:
      msg = "ERROR: Unknown in moveFile"
      err.printLog(msg + "\n\targ1 = '%s' arg2 = '%s'" % (currFile, newFile))
      return False

   return True


def movePics():
   """
   Will move all jpg files in the image folder to the USB pen
   """
   carryOn = True
   for fName in os.listdir(const.imgFolder):
      fileName = picFile[picFile.rfind('/')+1:]
      newFilePath = const.permDataStoragePath + '/' + fileName
      carryOn *= moveFile(picFile, newFilePath)

   return carryOn


def getCurrData():
   """
   Will get the current saved data. If there isn't any return an empty dataframe.
   """
   if not os.path.isfile(const.dataFilepath):
      return pd.DataFrame()
   else:
      return pd.read_csv(const.dataFilepath, index_col=0)
