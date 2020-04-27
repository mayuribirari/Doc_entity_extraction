import cv2
import scripts.preprocessing
import numpy as np
import scripts.background_removal
from pytesseract.pytesseract import TesseractError


def preprocess(image_name):
    image_org = cv2.imread(image_name)
    image = np.copy(image_org)
    flag = False
    try:
        image = scripts.preprocessing.detect_orientation(image)
    except TesseractError as e:
        print('[DEBUG]: Tesseract Exception handled')
        flag = True
    image = scripts.preprocessing.straighten(image)
    image = scripts.preprocessing.extract_image(image)
    # print(image.shape)
    # scripts.preprocessing.display(image,0.35,0.35)
    # cv2.imwrite('output_rgb.jpg',image)
    if flag:
        image = scripts.preprocessing.detect_orientation(image)
        image = scripts.preprocessing.straighten(image)
    ### EXTRA SPACE REMOVAL ###
    value = scripts.background_removal.detect_border_color(image)
    if value:
        image = scripts.background_removal.cropped(image, value)
    scripts.preprocessing.plot_before_after(image_org, image,  image_title = image_name,save= False,show = True)


    image = cv2.resize(image,dsize=(1056,1425))

    import os
    print(os.getcwd())
    name = 'dump_output1.jpg'
    cv2.imwrite(name,image)
    print(image.shape) #(1736, 1286, 3),(1652, 1225, 3),
    return name
