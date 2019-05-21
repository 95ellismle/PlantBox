# PlantBox

Making a device to look after my plants autonomously has been an ambition of mine for a while. This is the latest (and greatest) attempt to build such a device. The device is basically a grow tent kitted out with LED lighting, some sensors, a camera and of course some plants.

## Aims of the project
The original project was quite ambitious so I thought I would tone it down slightly and create something more managable. The project is going to be a serious foray into the world of hobby hydroponics and a way to get some knowledge on vertical farms. Hopefully, I will also get some fruit and veg from it!

## Equipment List
1 80x80x180 Grow Tent
...

## TODO

### Generally
Nearly everything!

#### Interface
  * Create an app (android -as I have an android) that interfaces with the raspberry pi.
  * Make the app change things in how the code runs.
  
#### Environment -watch the costs, this should be kept cheap!
  ##### Sensing
  Basically code everything up... There are a few sensors I don't have at the moment and I'm trying to get by without them. Those high up on my wish list are pH sensor (needed), EC sensor (needed for nutrients), CO2 sensor (nice to have but not necessary), PAR sensor (nice to have), dissolved oxygen (nice to have)
  * Create database to store data
  * Add temperature/humidity sensors 
  * Get PAR readings (the photosynthetically active radiation, basically light that plants like)
  * Get pH reading (for hydroponics)
  * Get dissolved oxygen reading (for hydroponics)
  * Get CO2 readings.
  
  ##### Controlling
  * Adjust light position (ideally mount the lights on a moveable rack, move up and down with motors)
  * Adjust temperature (close off the system, insulate and install heaters/coolers and fans)
  * Adjust hummidity (maybe have a mister or maybe just have a tray at the bottom of the device that can fill and drain water)

#### Data
  * Write some code to detect the size of the plants (maybe identify where the plants are and measure the amount of mostly green pixels?)
  * Write some code to detect signs of an unhealthy plant (identify where the leaves are and pick out spots, how do I detect dryness/wilting?)
  * Stitch the images together into a timelapse (should be trivial with ffmpeg -maybe need to change the filenaming system)
  * With the amount of plant growth as a metric automatically analyse the various enviromental factors that affect the plants growth.

### Current Tasks:
  * Create a kill file that has a variable in it and if that variable is set to stop then stop the code.
  * Fix the data reading (doEvent function only returns an exit code atm)
  * Add some more error detection -permission errors with the writing of file to the USB pen, wrong gpio pins chosen, file not found etc...
  * Make variable names and file name consistent!
  * Change the way images are stored (just use a number in the filepath and store the corresponding datetime in a csv file)
  * Add user input for the frequency of various events (e.g. put in the const.py when to take pics, take data readings or check the lights)
  * Create an input file but still have defaults for all the settings.
  * Automatically scp data to a laptop, if available, else wait until available and scp.
  * Check which parts are available and use them if they are. E.g. if the USB is connected then get the data, if not don't save the data. If the camera is connected take pics, if not don't.
  * Send some feedback to the RPi to determine whether the lights are connected? Pull up resistor?
  
