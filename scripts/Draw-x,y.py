import cv2
import os
import io
import csv
import pandas as pd
from google.cloud import vision


image = cv2.imread('dump_output1.jpg')
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
# cv2.namedWindow("image", cv2.WINDOW_AUTOSIZE)

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
    entities = ("Buyer name","Property address","Seller Brokerage Firm ","Buyers brokerage firm",
                "Initial deposit","Balance downpayment","purchase price","date prepared")
    x_y = (((267,151),(972,172)),((377,175),(955,191)),((259,358),(748,376)),((263,441),(749,463)),
           ((866,577),(1054,601)),((860,1251),(1052,1272)),((858,1291),(1052,1309)),((126,113),(281,137)))
    print(len(x_y),len(entities))
    assert len(entities)==len(x_y)
    # while True:
    #     if not cropping:
    #         cv2.imshow('image', image)
    #     elif cropping and sel_rect_endpoint:
    #         rec = image.copy()
    #         cv2.rectangle(rec, now_pt1, sel_rect_endpoint, (0, 0, 255), 2)
    #         cv2.imshow('image', rec)
    #
    #     key = cv2.waitKey(1) & 0xFF
    #
    #     if key == ord('q'):
    #         exit()
    #
    #     elif key == ord('u'):
    #         image = undo.pop()
    #         ROI_coordinates.pop()
    #         cv2.imshow('image', image)
    #
    #     elif key == ord('c'):
    #         image = image_copy.copy()
    #         ROI_coordinates = []
    #         undo = []
    #         # print(ROI_coordinates,undo)
    #
    #     elif key == ord('a'):
    #         print('[DEBUG] : Accepted ROIs!')
    #         for i in ROI_coordinates:
    #             print('[DEBUG] :', i[0][1], i[1][1], i[0][0], i[1][0])
    #         break

    # cv2.destroyAllWindows()
    images_container = []

    for i in x_y:
        images_container.append(image_org[i[0][1]:i[1][1], i[0][0]:i[1][0]])

    v_stacked = pad_images_to_same_size(images_container)
    cv2.imshow("Padded_concat", v_stacked)
    cv2.imwrite('Concat_test.jpg',v_stacked)
    cv2.waitKey(0 )


    text_in_img:str = image_to_desciption_text(img_path)

    text_in_img_split = text_in_img.splitlines()
    print(text_in_img_split,len(text_in_img_split))

    assert len(entities) == len(text_in_img_split)
    with open('..\\csv\\Extracted_Entities.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(entities)
        writer.writerow(text_in_img_split)
    df = pd.read_csv('Extracted_Entities.csv')
    print(df)

    print('-'*40)
    print('-'*40)
    print(text_in_img_split)