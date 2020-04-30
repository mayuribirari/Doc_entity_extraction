import cv2
import numpy as np
from scripts.preprocessing import display,detect_orientation

# img = cv2.imread('..\\images\\v2\\Lightroom\\out1.pdf_rot+scaled.jpg')

def detect_border_color(img):
    img = cv2.threshold((cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)),127,255,cv2.THRESH_BINARY)[1]
    l,b = img.shape
    PERCENTAGE = 3
    l = (l*PERCENTAGE)//100
    b = (b*PERCENTAGE)//100
    # print(l,b)
    c1 = img[:,:b]
    c2 = img[:l,:]
    # display(c1)
    # display(c2)
    values1, counts1 = np.unique(c1, return_counts=True)
    values2, counts2 = np.unique(c2, return_counts=True)
    if values1[np.argmax(counts1)] == values2[np.argmax(counts2)]:
        # print(type(values1[np.argmax(counts1)]))
        return values1[np.argmax(counts1)]
    else:
        print("[DEBUG]: Not cropping extra space!")
        return None

def cropped(img,value):
    # print(img.shape)
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img_gray = cv2.threshold(img_gray,127,255,type = cv2.THRESH_BINARY)[1]
    cont_x = [i for i in range(img_gray.shape[0]) if set(img_gray[i]) != {value}]
    first_x,last_x =cont_x[0],cont_x[-1]

    img_gray_trans = np.transpose(img_gray)
    cont_y = [i for i in range(img_gray_trans.shape[0]) if set(img_gray_trans[i]) != {value}]
    first_y,last_y =cont_y[0],cont_y[-1]

    img_cropped : np.ndarray = img[first_x:last_x,first_y:last_y]
    print('[DEBUG]: Original image shape :',img.shape,'Removed Border image shape :',img_cropped.shape)
    return img_cropped
