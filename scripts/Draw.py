import cv2
import os
import io
from google.cloud import vision
import logging


image = cv2.imread('dump_output.jpg')
image_copy = image.copy()
image_org = image.copy()
img_path = 'Concat_test.jpg'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '..\\json\\Handwritting Recognission-2cf8babac416.json'
PROJECT_ID = 'handwritting-recognission'
SESSION_ID = '123'
ROI_coordinates = []
undo = []
now_pt1 = now_pt2 = None
cropping = False
sel_rect_endpoint = None
cv2.namedWindow("image", cv2.WINDOW_AUTOSIZE)

def roi_selection(event, x, y, flags, param):
    global ROI_coordinates, now_pt1, now_pt2, sel_rect_endpoint, cropping, undo

    if event == cv2.EVENT_LBUTTONDOWN:
        undo.append(image.copy())
        cropping = True
        now_pt1 = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE and cropping:
        sel_rect_endpoint = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        now_pt2 = (x, y)
        cropping = False
        sel_rect_endpoint = None
        if now_pt2 != now_pt1:
            if now_pt1[1] > now_pt2[1]:
                ROI_coordinates.append((now_pt2, now_pt1))
            else:
                ROI_coordinates.append((now_pt1, now_pt2))
        cv2.rectangle(image, now_pt1, now_pt2, (0, 0, 255), 2)
        cv2.imshow("image", image)
        # print(ROI_coordinates)

cv2.setMouseCallback("image", roi_selection)

def image_to_desciption_text(image_path):
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image(content=content)
    # response = client.text_detection(image=image)
    response = client.document_text_detection(image=image)
    return response.text_annotations[0].description

def pad_images_to_same_size(images):
    """
    :param images: sequence of images
    :return: list of images padded so that all images have same width and height (max width and height are used)
    """
    width_max = 0
    height_max = 0
    for img in images:
        h, w = img.shape[:2]
        width_max = max(width_max, w)
        height_max = max(height_max, h)

    images_padded = []
    for img in images:
        h, w = img.shape[:2]
        diff_vert = height_max - h
        pad_top = diff_vert//2
        pad_bottom = diff_vert - pad_top
        diff_hori = width_max - w
        pad_left = diff_hori//2
        pad_right = diff_hori - pad_left
        img_padded = cv2.copyMakeBorder(img, pad_top +1, pad_bottom+1, pad_left+1, pad_right+1, cv2.BORDER_CONSTANT, value=(255,255,255))
        images_padded.append(img_padded)

    v_stack = cv2.vconcat(images_padded)
    return v_stack

if __name__  =='__main__':
    while True:
        if not cropping:
            cv2.imshow('image', image)
        elif cropping and sel_rect_endpoint:
            rec = image.copy()
            cv2.rectangle(rec, now_pt1, sel_rect_endpoint, (0, 0, 255), 2)
            cv2.imshow('image', rec)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            exit()

        elif key == ord('u'):
            image = undo.pop()
            ROI_coordinates.pop()
            cv2.imshow('image', image)

        elif key == ord('c'):
            image = image_copy.copy()
            ROI_coordinates = []
            undo = []
            # print(ROI_coordinates,undo)

        elif key == ord('a'):
            logging.info(' Accepted ROIs!')
            for i in ROI_coordinates:
                logging.info('[DEBUG] : %s', i[0][1], i[1][1], i[0][0], i[1][0])
            break

    cv2.destroyAllWindows()
    images_container = []

    for i in ROI_coordinates:
        images_container.append(image_org[i[0][1]:i[1][1], i[0][0]:i[1][0]])

    v_stacked = pad_images_to_same_size(images_container)
    cv2.imshow("Padded_concat", v_stacked)
    cv2.imwrite('Concat_test.jpg',v_stacked)


    text_in_img:str = image_to_desciption_text(img_path)
    entities = ['Date Prepared','Purchase Price',"Seller's Agent"]
    text_in_img_split = text_in_img.splitlines()

    print('-'*40)
    # for i in entities:
    #     i = i.lower()
    #     for j in text_in_img_split:
    #         j = j.lower()
    #         if i in j:
    #             print(i.upper(),"matched with : ",j)

    # If sequence is followed:
    print('-'*40)
    # for i,j in zip(entities,text_in_img_split):
    #        print(i,":",j)
    # cv2.imshow('Concat',v_stack)
    print(text_in_img_split)
    cv2.waitKey()
