# Driver logic here
import cv2
import scripts.preprocessing
import numpy as np

PATH = '..\\images\\j.jpg'
image_org = cv2.imread(PATH)

##################### PREPROCESSING ####################

image = np.copy(image_org)
image = scripts.preprocessing.detect_orientation(image)
image = scripts.preprocessing.straighten(image)
image = scripts.preprocessing.extract_image(image)
scripts.preprocessing.plot_before_after(image_org, image)

#################### OCR ##############################
