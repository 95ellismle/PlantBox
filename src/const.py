import os

# Declare variables here
gpioPins = {'Flash': 4, 'GrowLight': 17, 'Temperature': [22, 27]}
imgFolder = "./img"
permDataStoragePath = "/media/pi/Data/"  # permanent data storage
logFile = "logFile.txt"
timeFormat = "%d/%m/%y %H:%M:%S"  # format for datetime printing

finalLightHours = 10
seedlingLightHours = 17
rateOfChangeOfLight = 3.5

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
if not os.path.isdir(imgFolder):
   os.makedirs(imgFolder)
permDataStoragePath = os.path.abspath(permDataStoragePath)

if os.path.isfile(logFile):
   os.remove(logFile)


def calculateLightTimeOn(dayNum, numHoursSeedling, numHoursFinal, rateOfChange=4):
    """
    Will return how many hours a day the light should be on depending on the
    final amount of light and seedling stage.
    """
    tmp = (1 - np.tanh(dayNum / float(rateOfChange)))
    tmp *= (numHoursSeedling - numHoursFinal)
    tmp += numHoursFinal
    return tmp
