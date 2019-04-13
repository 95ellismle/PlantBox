"""
Contains functions that aid in general data organisation like moving files around etc...
"""
import os
import shutil
import datetime as dt
import pandas as pd

from src import const
from src import err
from src import timeutils as tutils


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
   try:
      shutil.move(currPath, newPath)
   except PermissionError:
      err.printLog("ERROR: Can't move data to USB pen -permission error")
      return False

   return getCurrData()


def moveJPG(picFile):
   """
   Will move the picture file from the img folder to the USB pen

   Inputs:
      * picFile => the picture to move
   """
   if not os.path.isfile(picFile):
      return False
   else:
      fileName = picFile[picFile.rfind('/')+1:]
      newFilePath = const.permDataStoragePath + '/' + fileName
      shutil.move(picFile, newFilePath)
   return True


def getCurrData():
   """
   Will get the current saved data. If there isn't any return an empty dataframe.
   """
   if not os.path.isfile(const.dataFilepath):
      return pd.DataFrame()
   else:
      return pd.read_csv(const.dataFilepath, index_col=0)
