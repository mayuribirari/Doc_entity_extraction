# Driver logic here
import cv2
import scripts.preprocessing

PATH = '..\images\h_90.jpg'
image = cv2.imread(PATH)
scripts.preprocessing.display(image, 0.25, 0.25)
image = scripts.preprocessing.detect_orientation(image)
image = scripts.preprocessing.straighten(image)
scripts.preprocessing.display(image, 0.25, 0.25)