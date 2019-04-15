import os
import time

from src import time_utils as tutils
from src import err
from src import const
from src import light_utils as lights


class Picture(object):
   """
   Will handle all the picture taking options. This means it will:
      * take the pic
      * annotate it with the time
      * decide where to store it
      * save it

   Inputs:
      * camera => the camera object
   """
   def __init__(self, camera):
      self.cam = camera
      self.carryOn = True

   def lightsOn(self):
      "Will switch on the lights for a pic"
      lights.lightsOn(const.relayPins)
      time.sleep(2)

   def capture(self):
      """ Will handle taking the picture and annotating it"""

      self.lightsOn()
      
      self.cam.resolution = (2592, 1944)
      self.cam.rotation = 180
      #self.cam.annotate_text_size = 100
      #self.cam.annotate_text = tutils.strTimeNow()
      self.cam.start_preview()
      time.sleep(6)
      imgName = "%s.jpg" % (tutils.strTimeNow())
      imgName = imgName.replace(" ","_")
      imgName = imgName.replace(":","x")
      imgName = imgName.replace("/","-")
      imgFilePath = "%s/%s" % (const.imgFolder, imgName)
      self.cam.capture(imgFilePath)
      self.cam.stop_preview()
   
      self.imgFilePath = imgFilePath
      return True

