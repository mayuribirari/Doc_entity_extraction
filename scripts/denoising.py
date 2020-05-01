import cv2

def denoising(image):
    x,y=550,550
    crop_img = image[1:y, 1:x]
    cv2.imshow("cropped", crop_img)
    cv2.waitKey(0)
    cv2.imwrite(name,crop_img)
    extract_fields(name)


def extract_fields(x):
    import os
    import io
    from google.cloud import vision
    # print(os.getcwd())
    image_path = os.getcwd()+'\\'+x
    # print(image_path)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'C:/Users/hello/Desktop/projects/Doc_entity_extraction/Handwritting Recognission-2cf8babac416.json'
    
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
        response = client.text_detection(image=image)
        return response.text_annotations[0].description
    print('inside extraxts')
    print(image_to_desciption_text(image_path))
    # return fields
    return None  

if __name__=='__main__':
    PATH='C:\\Users\\hello\\Desktop\\projects\\Doc_entity_extraction\\images\\r0100\\r0100_00.png'
    name = 'test1.jpg'
    image = cv2.imread(PATH)
    denoising(image)