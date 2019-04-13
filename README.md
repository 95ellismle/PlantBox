# PlantBox

Making a device to look after my plants autonomously has been an ambition of mine for a while. This is the latest (and greatest) attempt to build such a device.

## Aims of the project
The project aims to create a cheap and highly modular system that is capable of looking after (productive) plants. The whole thing should eventually be very easy to install (place it down in a room and plug it in) and be very easy to maintain (just open the door and harvest when ready). However, this should not come at the cost of 'hackability', that is the whole thing should be easy to modify and improve for those who want to. In order to achieve this some key constraints need to be placed on the project from the start e.g:
  
  * Everything must be open-sourced. If a user wants to see the source code and change it (be it for good or bad) they should. Similarly for the hardware.
  * The code and hardware must be divided into discrete modules. These will be almost standalone devices. Inter-modular connections may be soldered but intra-modular should be easy to disconnect and reconnect.
  * The whole system should work with or without any individual module. These should be (were safe) replacable during run time, i.e. the full  system should not have to be shutdown everytime a new module is to be installed.
  * The code and hardware should be easy to understand and well documented (e.g. consistent code throughout, enough comments, OOP etc). 
  * To keep costs down, cheap microcontrollers should be used (i.e. arduino Nano, raspberry pi zero etc...). This also means very little computing power so things should be designed accordingly (i.e. code to be very lightweight).
  * The code will need a nice interface for a user (eventually). An android app would be ideal.
 

## Current setup

The project is very new and the current set up is very basic. The kit is comprised of:

* Rpi Zero W : This is the brains of the operation. It contols when things should happen and handles storing the data produced. It also takes pictures
* Arduino (genuino currently) : This recieves data from sensors (currently only light levels -in lux not PAR) it then broadcasts this info to the RPi via bluetooth every few seconds.
* Various sensors : At the moment only a camera and a light level sensor.
* Some grow lights : Fairly cheap, low powered grow lights. For testing on small plants.
* Some plants (pink kale and basil): These are grown under the grow light, the pink kale is grown hydroponically (using the Kratky method) and the basil in soil.

## TODO

### Generally
Nearly everything!

#### Interface
  * Create an app (android -as I have an android) that interfaces with the raspberry pi.
  * Make the app change things in how the code runs.
  
#### Environment -watch the costs, this should be kept cheap!
  ##### Sensing
  * Add temperature/humidity sensors (I have some DHT11 which should be sufficient)
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
  * Add some more error detection -permission errors with the writing of file to the USB pen, wrong gpio pins chosen, file not found etc...
  * Make variable names and file name consistent!
  * Change the way images are stored (just use a number in the filepath and store the corresponding datetime in a csv file)
  * Add user input for the frequency of various events (e.g. put in the const.py when to take pics, take data readings or check the lights)
  * Create an input file but still have defaults for all the settings.
  
