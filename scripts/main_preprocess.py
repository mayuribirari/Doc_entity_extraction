# Driver logic here


import cv2
import scripts.preprocessing
import numpy as np
import scripts.background_removal
from pytesseract.pytesseract import TesseractError



def preprocess(PATH):
    print('='*40+'\tPreprocessing\t'+'='*40)
    image_org = cv2.imread(PATH)
    image = np.copy(image_org)
    flag = False
    try:
        image = scripts.preprocessing.detect_orientation(image)
    except TesseractError as e:
        # print('Exception handled')
        flag = True
    image = scripts.preprocessing.straighten(image)
    image = scripts.preprocessing.extract_image(image)  # GENERATES BINARY IMAGE
    # scripts.preprocessing.display(image,0.35,0.35)
    if flag:
        image = scripts.preprocessing.detect_orientation(image)
        image = scripts.preprocessing.straighten_thresh(image)

    ### EXTRA SPACE REMOVAL ###
    value = scripts.background_removal.detect_border_color(image)
    if value:
        image = scripts.background_removal.cropped(image, value)
    # scripts.preprocessing.plot_before_after(image_org, image)
    return image
#################### OCR ##############################
