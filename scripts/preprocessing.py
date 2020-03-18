import cv2
import pytesseract
import re
import numpy as np


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
    """ Returns correct oriented image
    :param image: Input image
    """
    custom_oem_psm_config = r'--oem 1--psm 7'
    newdata = pytesseract.image_to_osd(image,config= custom_oem_psm_config)
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


# def extract_image(image, thresh_value = 190):
#     """
#     Returns borderless image
#     :param image : Image with border
#     :returns borderless image
#     """
#
#     img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     _, img = cv2.threshold(img, thresh_value, 255, cv2.THRESH_BINARY)
#     cont, hier = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     area = 0
#     biggest_cont = cont[0][0]
#
#     for i in cont:
#         area1 = cv2.contourArea(i)
#         if area1 > area:
#             area = area1
#             biggest_cont = i
#
#     mask = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
#     cv2.drawContours(mask, [biggest_cont], -1, (255, 255, 255))
#
#     sub_image = img - mask
#     st_sub_images = straighten_thresh(sub_image)
#     display(st_sub_images,0.5,0.5)
#
#
#     l, b = st_sub_images.shape
#     PERCENTAGE = 3
#     l = (l * PERCENTAGE) // 100
#     b = (b * PERCENTAGE) // 100
#     print(l, b)
#     c1 = st_sub_images[:, :b]
#     c2 = st_sub_images[:l, :]
#     display(c1)
#     display(c2)
#
#     values1, counts1 = np.unique(c1, return_counts=True)
#     values2, counts2 = np.unique(c2, return_counts=True)
#     if values1[np.argmax(counts1)] == values2[np.argmax(counts2)]:
#         value = values1[np.argmax(counts1)]
#         print(value)
#         cont_x = [i for i in range(st_sub_images.shape[0]) if set(st_sub_images[i]) != {value}]
#         first_x, last_x = cont_x[1], cont_x[-1]
#
#         st_sub_images_trans = np.transpose(st_sub_images)
#         cont_y = [i for i in range(st_sub_images_trans.shape[0]) if set(st_sub_images_trans[i]) != {value}]
#         first_y, last_y = cont_y[1], cont_y[-1]
#
#         img_cropped: np.ndarray = st_sub_images[first_x:last_x, first_y:last_y]
#         display(img_cropped, 0.35, 0.35)
#         print(img_cropped.shape)
#         return img_cropped
#
#     else:
#         thresh = cv2.threshold(st_sub_images, 1, 255, cv2.THRESH_BINARY)[1]
#         contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         if len(contours) == 1:
#             cnt = contours[0]
#             x, y, w, h = cv2.boundingRect(cnt)
#             st_sub_images = st_sub_images[y:y + h, x:x + w]
#         return st_sub_images


def extract_image(image):
  """
  Returns borderless image
  :param image : Image with border
  :returns borderless image
  """
  img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  re, img = cv2.threshold(img,160, 255, cv2.THRESH_BINARY)
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
  cv2.drawContours(mask, [biggest_cont], -1,(255,255,255),thickness=0)
  sub_image = img - mask
  st_sub_images = straighten_thresh(sub_image)
  thresh = cv2.threshold(st_sub_images,1,255,cv2.THRESH_BINARY)[1]
  contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  if len(contours) == 1:
    cnt = contours[0]
    x,y,w,h = cv2.boundingRect(cnt)
    st_sub_images = st_sub_images[y:y+h,x:x+w]
  return st_sub_images

def plot_before_after(before, after):
    """
    :param before: Before correction image
    :param after: After correction image
    """
    import matplotlib.pyplot as plt
    plt.figure(figsize=(16, 22))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(before, cv2.COLOR_BGR2RGB))
    # plt.axis('off')
    plt.grid(True)
    plt.title(label="Before : ")

    plt.subplot(1, 2, 2)
    plt.imshow(after, cmap='Greys_r')
    # plt.axis('off')
    plt.grid(True)
    plt.title(label='After : ')
    plt.show()
