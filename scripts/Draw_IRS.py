import cv2
import os
import io
import csv

from google.cloud import vision
import logging

img_path = 'dump_output1.jpg'
master_img = cv2.imread(r'D:\Hvantage\Doc_entity_extraction\images\v3\New Folder\Lightroom\r0434_00.jpg')
image = cv2.imread('dump_output1.jpg')
image_copy = image.copy()
image_org = image.copy()
concat_img_path = 'Concat_test_IRS.jpg'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '..\\json\\Handwritting Recognission-2cf8babac416.json'
PROJECT_ID = 'handwritting-recognission'
SESSION_ID = '123'
ROI_coordinates = []
undo = []
now_pt1 = now_pt2 = None
cropping = False
sel_rect_endpoint = None
# cv2.namedWindow("image", cv2.WINDOW_AUTOSIZE)

# def roi_selection(event, x, y, flags, param):
#     global ROI_coordinates, now_pt1, now_pt2, sel_rect_endpoint, cropping, undo
#
#     if event == cv2.EVENT_LBUTTONDOWN:
#         undo.append(image.copy())
#         cropping = True
#         now_pt1 = (x, y)
#
#     elif event == cv2.EVENT_MOUSEMOVE and cropping:
#         sel_rect_endpoint = (x, y)
#
#     elif event == cv2.EVENT_LBUTTONUP:
#         now_pt2 = (x, y)
#         cropping = False
#         sel_rect_endpoint = None
#         if now_pt2 != now_pt1:
#             if now_pt1[1] > now_pt2[1]:
#                 ROI_coordinates.append((now_pt2, now_pt1))
#             else:
#                 ROI_coordinates.append((now_pt1, now_pt2))
#         cv2.rectangle(image, now_pt1, now_pt2, (0, 0, 255), 2)
#         cv2.imshow("image", image)
#         # print(ROI_coordinates)
#
# cv2.setMouseCallback("image", roi_selection)

def image_to_desciption_text(image_path):
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image(content=content)
    # response = client.text_detection(image=image)
    response = client.document_text_detection(image=image)
    return response.text_annotations

def pad_images_to_same_size(images):
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
    logging.info('Image stacking completed')
    return v_stack

if __name__  =='__main__':
    master_label = (14,154) # X1,Y1
    master_x_y = (((400, 208), (1748, 269)), ((400, 310), (1744, 369)), ((383, 1104), (1358, 1395)), ((1831, 1504), (2102, 1550)),
                  ((1839,2402),(2101,2456)))  # X2,Y2
    original_relative_to_label = []
    for i in master_x_y:
        original_relative_to_label.append(((i[0][0]-master_label[0],i[0][1]-master_label[1]),
                                           (i[1][0]-master_label[0],i[1][1]-master_label[1])))
    # original_relative_to_label =[((397, 75), (1745, 136)), ((397, 177), (1741, 236)),
    #                              ((380, 971), (1355, 1262)), ((1828, 1371), (2099, 1417)),
    #                              ((1836, 2269), (2098, 2323))] #X2-X1,Y2-Y1 = X3,Y3
    image_copy = master_img[master_label[1]:,master_label[0]:]
    cv2.imshow("Master_image", image_copy)
    orig_cont = []
    for i in original_relative_to_label:
        orig_cont.append(image_copy[i[0][1]:i[1][1], i[0][0]:i[1][0]])
    v_stacked = pad_images_to_same_size(orig_cont)
    resized = cv2.resize(v_stacked,(0,0),fx = 0.35,fy = 0.35)
    cv2.imshow("Master_Padded_concat", resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # print(original_relative_to_label)

    new_origin_x, new_origin_y = None, None #X4,Y4
    text_in_img: str = image_to_desciption_text(img_path)
    for i in text_in_img[1:]:
        if i.description == 'Label':
            new_origin_x = i.bounding_poly.vertices[0].x
            new_origin_y = i.bounding_poly.vertices[0].y
            print('Label found!')
            print(new_origin_x, new_origin_y)

            # To draw a rectangle over 'Label' in the testing image
            ROI_coordinates.append(((i.bounding_poly.vertices[0].x, i.bounding_poly.vertices[0].y),
                                    (i.bounding_poly.vertices[2].x, i.bounding_poly.vertices[2].y)))
            # print(ROI_coordinates)
            break

    if new_origin_y and new_origin_x:
        label_coordinates = (new_origin_x, new_origin_y) #X4,Y4
    else:
        print('Label not found')
        exit()
    img_label_coordinates = image[new_origin_y:,new_origin_x:]
    cv2.imshow("Test_image",img_label_coordinates)
    relative_label = (label_coordinates[0]-master_label[0], label_coordinates[1]-master_label[1]) #X5,Y5
    # cv2.rectangle(image, ROI_coordinates[0][0], ROI_coordinates[0][1], color=(255, 0, 0), thickness=3)
    # cv2.imshow("OCR_Tracing", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # cv2.imshow('Before crop',image)
    # image = image[new_origin_y:,new_origin_x:]
    # cv2.imshow('After crop',image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    new_relative_to_label = []
    for i in original_relative_to_label:
        new_relative_to_label.append(((i[0][0]-relative_label[0],i[0][1] - relative_label[1]),
                                     (i[1][0]-relative_label[0],i[1][1] - relative_label[1]))) #X6,Y6
    images_container = []
    for i in new_relative_to_label:
        images_container.append(img_label_coordinates[i[0][1]:i[1][1], i[0][0]:i[1][0]])
    print('ROIs extracted')
    v_stacked = pad_images_to_same_size(images_container)
    resized = cv2.resize(v_stacked,(0,0),fx = 0.35,fy = 0.35)
    cv2.imshow("Padded_concat_test", resized)
    cv2.imwrite('Concat_test_IRS.jpg',v_stacked)
    print('Concat_stacking saved successfully')
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    text_in_img:str = image_to_desciption_text(concat_img_path)
    print(text_in_img[0].description)


