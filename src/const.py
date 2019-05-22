import os
import Adafruit_DHT
import json

# Declare variables here
gpioPins = {'Flash': 4, 'GrowLight': 17}
sensorPins = {'DHT': [(Adafruit_DHT.DHT22, 22), (Adafruit_DHT.DHT11, 27)]}
imgFolder = "./img"
permDataStoragePath = "/media/pi/Data/"  # permanent data storage
timeFormat = "%d/%m/%y %H:%M:%S"  # format for datetime printing
files = {'mysqlCreateUserTemplate': '../mysql/create_user_TEMPLATE.sql',
         'dynamicSettings': './dynSett.json',
         'lastTimes': './lasttimes.json',
         'sysLog': './logFile.txt'}

mysql_user="plantBox3"
mysql_passwd=""

finalLightHours = 10
seedlingLightHours = 17
rateOfChangeOfLight = 3.5

allLastTimeVals = ['lightCheck', 
                   'takePic'] 

badPathWarnings = 0  # How many warning occured about a bad path

initialDynSettings = {'lightOnTime': 0,
                      'failedPins': []}
"""
Above this are settings to be set.






Below this is code to initialise the settings 
"""

# Carry out any code that is related only to the variables
#  set above
allGood = True

# Handle various folder paths
if not os.path.isdir(imgFolder):
   os.makedirs(imgFolder)
permDataStoragePath = os.path.abspath(permDataStoragePath)

with open(dynamicSettingsFile, 'w') as f:
    json.dump(initialDynSettings, f)

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
