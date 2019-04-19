import bluetooth
import time
import datetime as dt
import os
import pandas as pd

from src import err
from src import const
from src import time_utils as tutils


def initBluetooth(macAddress, port):
    """
    Will initialise the bluetooth module.
    """
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    # no need for a try and except here as errors are already handled
    s.connect((macAddress, port))
    err.printLog("INFO: Bluetooth Connected")
    return s


def makeNum(string):
   """
   Will convert the string to a number if possible. If not then will return the
   string
   """
   try:
      return eval(string)
   except NameError:
      return string


def combineDataFrames(data, data1):
    """
    Will add data1 into data (both pandas dataframes)
    """
    return data.append(data1)



def getData(s, oldData, strs):
    """
    Will parse the data that is incoming from the bluetooth
    module.

    Inputs:
        * s => the connected socket class
        * oldData => the dictionary storing all the data to be updated.
    """
    strs += s.recv(10).decode('utf-8')
    ltxt = strs.split('\n')

    # This will handle finding full messages in the str
    clearBeginning = True  # remove any permanent useless strs
    relData = []  # relevant data
    for i, item in enumerate(ltxt):
        if '$S' in item and '$E' in item:

            if i > 0 and clearBeginning:  # remove sticky beginning strs
                ltxt = ltxt[i:]
                clearBeginning = False

            ltxt.remove(item)  # Once the data has been parsed remove it

            tmp = item[item.find('$S')+2:]
            tmp = tmp[:tmp.find('$E')]
            relData.append(tmp)
    retStrs = '\n'.join(ltxt)  # return the str without parsed data

    # Now put the data into the current dataframe
    newData = {}
    for item in relData:
        colName, value = item.split('=')
        newData[colName] = [value]
    newData = pd.DataFrame(newData)
    if len(newData) > 0:
       dateTime = tutils.strTimeNow()
       newData.index = [dateTime for i in range(len(newData))]
       newData = combineDataFrames(oldData, newData)
       newData.to_csv(const.dataFilepath)
       return retStrs, newData

    return retStrs, oldData
