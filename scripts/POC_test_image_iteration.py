# -*- coding: utf-8 -*-
"""Test image_iteration

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lFNW65lry0mxudP9jNcphXAEm4d9W0iI

# Mount Drive for Images
"""
#
# from google.colab import drive
# drive.mount('/content/drive')
#
# !ls "/content/drive/My Drive/images/"
#
# import os
# os.getcwd()
# path = '/content/drive/My Drive/images/'
# os.chdir(path)
# os.getcwd()
#
# """# Imports & Declaring Functions"""
#
# !sudo apt install tesseract-ocr
# !pip install pytesseract

# Commented out IPython magic to ensure Python compatibility.
import cv2
import numpy as np
import re

# # For code to work on Colab
# import matplotlib.pyplot as plt
# # %matplotlib inline
# from google.colab.patches import cv2_imshow


import pytesseract

# def plot_before_after(before, title ,after):
#   """
#   :param before: Before correction image
#   :param before: After correction image
#   :param Title: Name of the image
#   """
#
#   plt.figure(figsize=(18,25))
#   plt.subplot(1, 2, 1)
#   plt.imshow(cv2.cvtColor(before, cv2.COLOR_BGR2RGB))
#   plt.axis('off')
#   plt.title(label = "Before : "+title)
#
#
#   plt.subplot(1, 2, 2)
#   plt.imshow(after,cmap='Greys_r')
#   plt.axis('off')
#   plt.title(label = 'After : ' +title)
#   plt.show()

def detect_orientation(image):
    """ Returns correct oriented image
    :param image: Input image
    """
    newdata = pytesseract.image_to_osd(image)
    rotation = int(re.search('(?<=Rotate: )\\d+', newdata).group(0))
    # print("Rotation degrees : ", rotation)
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
        print("DEGREE = ", degrees)


def straighten(image):
    """Applies straighten to an image
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
    # print("Straightening angle : ", angle)
    return rotated

def straighten_thresh(image):
    """Applies straighten to an image
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
  img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  re, img = cv2.threshold(img,180, 255, cv2.THRESH_BINARY)
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

  mask = np.zeros((image.shape[0], image.shape[1]),dtype=np.uint8)
  cv2.drawContours(mask, [biggest_cont], -1, (255, 255, 255), 2)
  sub_image = img - mask
  st_sub_images = straighten_thresh(sub_image)
  return st_sub_images

"""#Driver Function"""

for image_name in os.listdir(path):
  img_before = cv2.imread(image_name)
  img2 = detect_orientation(img_before)
  img2 = straighten(img2)
  img_after = extract_image(img2)
  plot_before_after(img_before,image_name,img_after)
  break