import os

# Declare variables here
relayPins = [7, 11]
dataFilepath = "./Data/ArduinoSensorData.csv"  # Save Data path
imgFolder = "./Img"
permDataStoragePath = "/media/pi/Data/"  # permanent data storage
logFile = "logFile.txt"
macAddress = "98:D3:31:F7:22:36"  # mac address of bluetooth mod
port = 1  # port to connect to bluetooth on
timeFormat = "%d/%m/%y %H:%M:%S"  # format for datetime printing

lastTimeFilepath = "lasttimes.json"  # filepath for the lasttimes file
allLastTimeVals = ['dataGet',  # The names of the last time values
                   'dataMove',  # these are the last times that the name
                   'lightCheck',   # has been adjusted.
                   'movePics',
                   'takePic'] 

badPathWarnings = 0  # How many warning occured about a bad path



# Carry out any code that is related only to the variables
#  set above
allGood = True

# Handle various folder paths
dataFilepath = os.path.abspath(dataFilepath)
dataFolder = dataFilepath[ :dataFilepath.rfind('/')]
if not os.path.isdir(dataFolder):
    os.makedirs(dataFolder)
lastTimeFilepath = "%s/%s" % (dataFolder, lastTimeFilepath)

if not os.path.isdir(imgFolder):
   os.makedirs(imgFolder)
permDataStoragePath = os.path.abspath(permDataStoragePath)

if os.path.isfile(logFile):
   os.remove(logFile)
