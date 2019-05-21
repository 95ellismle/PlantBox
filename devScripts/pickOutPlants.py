import cv2
import numpy as np
import matplotlib.pyplot as plt
import imutils
from skimage.filters import threshold_local

imgFilePath = "../permImg/72.jpg"

img = cv2.imread(imgFilePath)
img = imutils.resize(img, height = 750)


def imgShow(img):
   """
   Will show the image with the blue and red color channels swapped.
   The image will be flipped 180. The image must be in the BGR format.

   Inputs:
      * img => the cv2 image to show (actually a numpy array)
   """
   f, a = plt.subplots()
   a.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
   
   # Flip image
   ylims = a.set_ylim()
   a.set_ylim([ylims[1], ylims[0]])

   a.grid(False)

   plt.show()


def makeColorMask(imgIn, whichRGB,
                  rgbTol={'r': 1, 'g': 1, 'b': 1}):
    """
    Will create an array that acts as a mask that picks out pixels
    that (within a tolerance) are mostly the specified color.

    Inputs:
        * imgIn => input image (doesn't change)
        * whichRGB => color that is to be picked out. A string
                      choices are 'r', 'g' or 'b'.
        * rgbTol => tolerance for each color channel. A dict with
                    keys that are the colors to be filtered out
                    and tolerance values associated.
    """
    # Create a new copy of the input image
    imgOut = imgIn.copy()

    if whichRGB in rgbTol:
       rgbTol.pop(whichRGB)
    rgbTranslator = {'r': 2, 'g': 1, 'b': 0}
    rgbInd = rgbTranslator[whichRGB]

    # loop over colors that should be masked away
    for badRGB in rgbTol:
       badInd = rgbTranslator[badRGB]
       # set pix where the whichRGB channel > rgbTol * other rgb channel to 0
       imgOut[imgOut[:, :, rgbInd] < rgbTol[badRGB]*imgOut[:, :, badInd]] = 255

    return imgOut


# To pick out the areas that probably plants I will:
#    * Find shapes in the image -still need to look into this. 
#       I've found using a bilateral blur (fairly strong) with canny edge detection 
#       is quite good at finding edges.
#
#    * Basil leaves have way more green than blue, the makeColorMask fairly
#       effectively picks out the leaves too. When the shapes have been found
#       then find the average color in the shape etc... (Will HSV be useful?)



#

imgGreen = makeColorMask(img, 'g', {'b':7, 'r': 1.1})
imgGreen = cv2.erode(imgGreen, np.ones((5,5)), 1)
imgGreen = cv2.dilate(imgGreen, np.ones((3,3)), 1)
imgBlur = cv2.GaussianBlur(imgGreen, (9, 9), 2)
edges = cv2.Canny(imgBlur, 30, 150)


cnts = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

allCnts = []
for c in cnts:
    if 16000 > len(c)  > 100:
        allCnts.append(c)


cv2.drawContours(img, allCnts, -1, (255, 0, 0), 1)
### Need to fill these contours to make a mask (fill vertically and horizontally? erode dilate?)
#
#
##gray = img[:, :, 1] / (img[:, :, 0] + 0.1)
#
##cv2.imshow("Gray", gray)
#cv2.imshow("Orig", img)
cv2.imshow("Edges", edges)
#cv2.imshow("Blurred", imgBlur)
cv2.imshow("Green", imgGreen)
cv2.imshow("Original", img)



cv2.waitKey(0)
cv2.destroyAllWindows()
