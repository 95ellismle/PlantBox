import cv2

imgFilePath = "../"

img = cv2.imread(imgFilePath)

def maskImg(img, tol): 
    img[img[:, :, 0] > img[:, :, 1]*tol] = 0 
    img[img[:, :, 2] > img[:, :, 1]*tol] = 0 
     
    return img

plt.imshow(img, 
