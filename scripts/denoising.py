import cv2


def denoising(image):
    list_img=[]
    x,y=550,550
    x1,y1=-550,-550
    crop_img_topL = image[1:y, 1:x]
    crop_img_topR = image[1:550, -550:-1]
    
    crop_img_bottomL = image[-550:-1, 1:550]
    crop_img_bottomR = image[x1:-1, y1:-1]
    #cv2.imshow("cropped_topL", crop_img_topL)
    list_img.append(crop_img_topL)
    list_img.append(crop_img_topR)
    list_img.append(crop_img_bottomL)
    list_img.append(crop_img_bottomR)
    '''
    cv2.imshow("cropped_bottomR", crop_img_bottomR)
    cv2.imshow("cropped_topR", crop_img_topR)
    cv2.imshow("cropped_bottomL", crop_img_bottomL)
    cv2.waitKey(0)
    '''
    return list_img
    #extract_fields(list_img[0])


def extract_fields(x):
    import os
    import io
    from google.cloud import vision
    # print(os.getcwd())
    image_path = os.getcwd()+'\\'+x
    # print(image_path)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'C:/Users/hello/Desktop/projects/Doc_entity_extraction/json/Handwritting Recognission-2cf8babac416.json'
    
    PROJECT_ID = 'handwritting-recognission'
    SESSION_ID = '123'

    def image_to_desciption_text(image_path):
        # print(image_path)
        with io.open(image_path, 'rb') as image_file:
            # print('debug1')
            content = image_file.read()
        # print('debug2')

        client = vision.ImageAnnotatorClient()
        image = vision.types.Image(content=content)
        response = client.document_text_detection(image=image)
        return type(response)
    print('inside extraxts')
    print(image_to_desciption_text(image_path))
    # return fields
    return None  

if __name__=='__main__':
    PATH='C:\\Users\\hello\\Desktop\\projects\\Doc_entity_extraction\\images\\r0100\\r0100_00.png'
    name1 = 'topL.jpg'
    name2 = 'topR.jpg'
    name3 = 'bottomL.jpg'
    name4 = 'bottomR.jpg'
    image = cv2.imread(PATH)
    test_list=denoising(image)
    for i in test_list:
        cv2.imshow("test", i)
        cv2.waitKey(0)
    cv2.imwrite(name1,test_list[0])
    cv2.imwrite(name2,test_list[1])
    cv2.imwrite(name3,test_list[2])
    cv2.imwrite(name4,test_list[3])
    extract_fields(name1)
    