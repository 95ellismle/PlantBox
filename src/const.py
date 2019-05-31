import os
import Adafruit_DHT
import json

# Declare variables here
gpioPins = {'Flash': 4, 'GrowLight': 17}
sensorPins = {'DHT': [(Adafruit_DHT.DHT22, 22),
                      (Adafruit_DHT.DHT22, 27),
                      (Adafruit_DHT.DHT22, 16)]}
imgFolder = "./img"
permDataStoragePath = "/media/pi/Data/"  # permanent data storage
timeFormat = "%d/%m/%y %H:%M:%S"  # format for datetime printing
files = {'mysqlCreateUserTemplate': './mysql/create_user_TEMPLATE.sql',
         'mysqlCreateUser': './mysql/create_user.sql',
         'mysqlCreateUserSH': './mysql/create_user.sh',
         'mysqlCreateUserSHTemplate': './mysql/create_user_TEMPLATE.sh',
         'dynamicSettings': './dynSett.json',
         'lastTimes': './lasttimes.json',
         'syslog': './logFile.txt'}

mysql_user="plantBox"
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

for fileName in files:
    files[fileName] = os.path.abspath(files[fileName])

with open(files['dynamicSettings'], 'w') as f:
    json.dump(initialDynSettings, f)

if os.path.isfile(files['syslog']):
   os.remove(files['syslog'])


def calculateLightTimeOn(dayNum, numHoursSeedling, numHoursFinal, rateOfChange=4):
    """
    Will return how many hours a day the light should be on depending on the
    final amount of light and seedling stage.
    """
    tmp = (1 - np.tanh(dayNum / float(rateOfChange)))
    tmp *= (numHoursSeedling - numHoursFinal)
    tmp += numHoursFinal
    return tmp
