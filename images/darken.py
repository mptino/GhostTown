###########################################################################################
# Filename: darken.py
# Description: Darken a given image by halving the pixel intensity
###########################################################################################

## Imports ##
import numpy as np
import cv2
import os 

os.chdir('images')

###########################################################################################
# apply filter as a function
def apply_filter(img, filter):

    # get grayscale of image
    image  = cv2.imread(img)
    
    # get the filtered image 
    filtered = cv2.filter2D(src=image, ddepth=-1, kernel=filter)

    # rename window so doesn't go off screen
    cv2.namedWindow("rw", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("rw", 1000, 800)

    # combine old image with filtered (recall images are numpy arrays)
    conc = np.concatenate((image, filtered), axis = 1)
    
    # use cv2 to display the comparison!
    cv2.imwrite('./'+img[:-4]+'_main.jpg', filtered)
    cv2.imshow("rw", conc )
    cv2.waitKey(0)
    cv2.destroyAllWindows()

###########################################################################################

# image name
img = "grass.jpg"

# various kernels
darken = np.array([[0, 0, 0], 
                    [0, 0.9, 0], 
                    [0, 0, 0]])


# apply a filter (kernel)!
apply_filter(img, darken)