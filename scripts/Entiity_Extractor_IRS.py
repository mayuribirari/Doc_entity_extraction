import cv2
import os
import io
import csv
from google.cloud import vision
import logging

concat_img_path = 'Concat_test.jpg'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '..\\json\\Handwritting Recognission-2cf8babac416.json'
PROJECT_ID = 'handwritting-recognission'
SESSION_ID = '123'
ROI_coordinates = []



def image_to_desciption_text(image_path):
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)
    return response.text_annotations[0].description

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

    # PATH TO FOLDER
    images_path = '..\\images\\v3\\Demo'
    images_files = os.listdir(path=images_path)
    entities = ("First name","Home Address","City, town and zip code","SSN","Waqes or Salaries","Adjusted Gross Income")
    x_y = (((180,84),(769,111)),((180,130),(771,154)),((180,175),(772,199)),
           ((781,89),(967,112)),((813,664),(930,688)),((813,1305),(933,1333)))
    # assert len(entities)==len(x_y)
    for file_number,file_name in enumerate(images_files):
        image = cv2.imread(file_name)
        image_copy = image.copy()
        image_org = image.copy()
        images_container = []
        for pts in x_y:
            images_container.append(image_org[pts[0][1]:pts[1][1], pts[0][0]:pts[1][0]])
            logging.info('ROIs extracted')
            v_stacked = pad_images_to_same_size(images_container)
            cv2.imshow("Padded_concat", v_stacked)
            cv2.imwrite('Concat_test.jpg',v_stacked)
            logging.info('Concat_stacking saved successfully')
            cv2.waitKey(0)
        text_in_img:str = image_to_desciption_text(concat_img_path)
        text_in_img_split = text_in_img.splitlines()
        print(text_in_img_split,len(text_in_img_split))
        assert len(entities) == len(text_in_img_split)
        with open('..\\csv\\IRSEntityExtraction', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(text_in_img_split)
        print('File {0} of {1} completed'.format(file_number+1,len(images_files)))
        logging.info('CSV file created successfully')


    # print(text_in_img_split)