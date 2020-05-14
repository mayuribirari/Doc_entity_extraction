import cv2
import os
import io
import csv

from google.cloud import vision
import logging
from math import ceil

def image_to_desciption_text(image_path):
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image(content=content)
    # response = client.text_detection(image=image)
    response = client.document_text_detection(image=image)
    return response.text_annotations[0].description

def complete(image):
    images_container = []
    for i in x_y:
        images_container.append(image[i[0][1]:i[1][1], i[0][0]:i[1][0]])

    width_max = 0
    height_max = 0
    for img in images_container:
        h, w = img.shape[:2]
        width_max = max(width_max, w)
        height_max = max(height_max, h)

    images_padded = []
    for img in images_container:
        h, w = img.shape[:2]
        diff_vert = height_max - h
        pad_top = diff_vert//2
        pad_bottom = diff_vert - pad_top
        diff_hori = width_max - w
        pad_left = diff_hori//2
        pad_right = diff_hori - pad_left
        img_padded = cv2.copyMakeBorder(img, pad_top +5, pad_bottom+5, pad_left+5, pad_right+5, cv2.BORDER_CONSTANT,
                                        value=(255,255,255))
        images_padded.append(img_padded)

    v_stack = cv2.vconcat(images_padded)
    v_stack = cv2.copyMakeBorder(v_stack, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=(100, 100, 100))
    logging.info('Image stacking completed')
    return v_stack

if __name__ == '__main__':
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '..\\json\\Handwritting Recognission-2cf8babac416.json'
    PROJECT_ID = 'handwritting-recognission'
    SESSION_ID = '123'
    BATCH_SIZE = 14
    imageFilePath = '..\\images\\v2\\preprocessedImages'
    entities = ("Buyer name", "Property address", "Seller Brokerage Firm ", "Buyers brokerage firm",
                "Initial deposit", "Balance downpayment", "purchase price", "date prepared")
    x_y = (((267, 151), (972, 172)), ((377, 175), (955, 191)), ((259, 358), (748, 376)), ((263, 441), (749, 463)),
           ((876, 577), (1054, 601)), ((881, 1251), (1052, 1272)), ((876, 1285), (1052, 1309)),
           ((126, 113), (281, 137)))
    imageFiles = os.listdir(path = imageFilePath)
    # print(len(imageFiles))
    totalBatches = ceil(len(imageFiles)/BATCH_SIZE)
    for batch in range(totalBatches):
        batchImageContainer = []
        imagesBatch = [cv2.imread(filename=imageFilePath+'\\'+imageFiles[batch*BATCH_SIZE + i])for i in range(BATCH_SIZE)]
        # imagesSelfStack = [complete(singleImage) for singleImage in imagesBatch]
        fullBatchImageStack = cv2.vconcat([complete(singleImage) for singleImage in imagesBatch])
        cv2.imwrite(filename=imageFilePath+'\\fullBatchImageStack.jpg',img=fullBatchImageStack)
        text_in_img: str = image_to_desciption_text(imageFilePath+'\\fullBatchImageStack.jpg')
        os.remove(imageFilePath+'\\fullBatchImageStack.jpg')
        text_in_img_split = text_in_img.splitlines()
        data = [text_in_img_split[fileNumber*len(entities) : fileNumber*len(entities) + len(entities)] for fileNumber in range(BATCH_SIZE)]
        with open('..\\csv\\CaliforniaAssociations.csv','a+' ,newline='') as fileCSV:
            writerObj = csv.writer(fileCSV, lineterminator='\n')
            for singleFileData in data:
                writerObj.writerow(singleFileData)
