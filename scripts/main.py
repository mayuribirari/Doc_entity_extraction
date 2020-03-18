# Driver logic here
import cv2
import scripts.preprocessing
import numpy as np
import scripts.background_removal
from pytesseract.pytesseract import TesseractError
PATH = '..\\images\\v2\\Lightroom\\out1.pdf_scaled_80.jpg'
# PATH = '..\\images\\v1\\h.jpg'
image_org = cv2.imread(PATH)

##################### PREPROCESSING ####################

image = np.copy(image_org)
flag = False
try:
    image = scripts.preprocessing.detect_orientation(image)
except TesseractError as e:
    print('Exception raised ',e.message)
    flag = True


image = scripts.preprocessing.straighten(image)
image = scripts.preprocessing.extract_image(image) # GENERATES BINARY IMAGE
# scripts.preprocessing.display(image,0.35,0.35)
if flag:
    image = scripts.preprocessing.detect_orientation(image)
    image = scripts.preprocessing.straighten_thresh(image)

### EXTRA SPACE ###
value = scripts.background_removal.detect_border_color(image)
if value:
    image = scripts.background_removal.cropped(image,value)
scripts.preprocessing.plot_before_after(image_org, image)
#################### OCR ##############################
