import cv2
import logging
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

from pytesseract.pytesseract import image_to_osd

import re
import numpy as np
f = image_to_osd

def display(image, fx=1, fy=1):
    """Function to display image

    :param image: Input image
    :param fx: Scale factor of x-axis
    :param fy: Scale factor of y-axis
    """
    image = cv2.resize(image, (0, 0), fx=fx, fy=fy)
    cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def detect_orientation(image):
    """
    Returns correct oriented image

    :param image: Input image
    :return value of rotation needed
    """
    import time
    a = time.time()
    custom_oem_psm_config = r'--oem 1--psm 7'
    newdata = f(image, config=custom_oem_psm_config)
    rotation = int(re.search('(?<=Rotate: )\\d+', newdata).group(0))
    logging.info("Rotation degrees : %s", rotation)
    logging.info("Time taken in rotation op. is : %s", time.time()-a)
    return rotate_img(image, rotation)


def rotate_img(image, degrees):
    """Returns image rotated to the angle provided by detect_orientation

    :param image: The input image
    :param degrees: Angle to rotate
    :return Corrected image
    """
    if degrees == 90:
        return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    elif degrees == 180:
        return cv2.rotate(image, cv2.ROTATE_180)
    elif degrees == 270:
        return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif degrees == 0:
        return image
    else:
        logging.info("DEGREE = %s", degrees)


def straighten(image):
    """
    Applies straighten to an image

    :param image : Input image
    :return Straightened image
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center=center, angle=angle, scale=1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    logging.info("Straightening angle : %s", angle)
    return rotated

def sharpen_image(image):
    kernel = np.array([[0, -1, 0], [-1, 5,-1],[0, -1, 0]])  
    sharpened = cv2.filter2D(image, -1, kernel)
    logging.info("Image Sharpened")
    return sharpened

def gamma_correction(image):
    lookUpTable = np.empty((1,256), np.uint8)
    gamma=0.4
    for i in range(256):
        lookUpTable[0,i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
    res = cv2.LUT(image, lookUpTable)
    logging.info('Gamma Correction Applied')
    return res

def straighten_thresh(image):
    """
    Applies straighten to an image

    :param image : Input threshold image
    :return Straightened image
    """
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center=center, angle=angle, scale=1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    # print("Straightening angle : ", angle)
    return rotated

def extract_image(image):
    """
    Returns borderless image

    :param image : Image with border
    :returns borderless image
    """
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    re, img = cv2.threshold(img, 160, 255, cv2.THRESH_BINARY)
    cont, hier = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    area = 0
    biggest_cont = cont[0][0]
    peri = cv2.approxPolyDP(cont[0][0], 0.1, False)

    for i in cont:
        area1 = cv2.contourArea(i)
        if area1 > area:
            peri = cv2.approxPolyDP(i, 0.1, True)
            area = area1
            biggest_cont = i

    mask = np.full((image.shape[0], image.shape[1],3), 255 ,dtype=np.uint8)
    cv2.drawContours(mask, [biggest_cont], -1, (255,255,255), thickness=5)
    cv2.fillPoly(mask, pts=[biggest_cont], color=(0,0,0))
    sub_image = cv2.bitwise_or(image,mask)
    sub_image = detect_orientation(sub_image)
    sub_image = straighten(sub_image)
    return sub_image


def plot_before_after(before, after, image_title, show = True, save = False):
    """
    Plot describing the input_image and pre processed image

    :param save: If set to true saves the plot
    :param show: If set to true show the plot
    :param before: Before correction image
    :param after: After correction image
    """
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12, 15))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(before, cv2.COLOR_BGR2RGB))
    # plt.axis('off')
    plt.grid(True)
    plt.title(label="Before : ")

    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(after, cv2.COLOR_BGR2RGB))
    # plt.axis('off')
    plt.grid(True)
    plt.title(label="After : ")
    if save:
        name = image_title + '_results.jpg'
        plt.savefig(name)
        logging.info('Results saved!')
    if show:
        plt.show()
