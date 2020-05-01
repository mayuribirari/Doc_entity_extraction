import logging
import cv2
import scripts.preprocessing
import numpy as np
import scripts.background_removal
from pytesseract.pytesseract import TesseractError


def preprocess(image_name):
    print('-' * 40 + '\tPreprocessing Begins\t' + '-' * 40)
    image_org = cv2.imread(image_name)
    image = np.copy(image_org)
    flag = False
    try:
        image = scripts.preprocessing.detect_orientation(image)
    except TesseractError as e:
        logging.info('Tesseract Exception handled')
        flag = True
    image = scripts.preprocessing.straighten(image)
    image = scripts.preprocessing.extract_image(image)
    if flag:
        image = scripts.preprocessing.detect_orientation(image)
        image = scripts.preprocessing.straighten(image)
    image=scripts.preprocessing.sharpen_image(image)
    image=scripts.preprocessing.gamma_correction(image)
    ### EXTRA SPACE REMOVAL ###
    value = scripts.background_removal.detect_border_color(image)
    if value:
        image = scripts.background_removal.cropped(image, value)
    master_doc_shape = (1056,1425)
    image = cv2.resize(image,dsize=master_doc_shape)
    logging.info("Resizing to {0}, i.e. master image's aspect ratio".format(master_doc_shape))

    scripts.preprocessing.plot_before_after(image_org, image, image_title=image_name, save=False, show=True)

    # import os
    # print(os.getcwd())
    name = 'dump_output1.jpg'
    logging.info('Saving a local copy of the preprocessed image')
    cv2.imwrite(name,image)
    print('-' * 40 + '\tPreprocessing Ends\t' + '-' * 40)
    # print(image.shape) #(1736, 1286, 3),(1652, 1225, 3),
    return name
