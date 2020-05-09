import cv2
import json
from enum import Enum
import numpy as np
from itertools import cycle
import scripts.preprocessing

def find_vertices(list_of_vertices):
    x=[]
    y=[]
    for i in list_of_vertices:
        for j in i.vertices:
            x.append(j.x)
            y.append(j.y)
    return x,y

def denoising(image):
    list_img=[]
    x,y=600,600
    x1,y1=-x,-y
    crop_img_topL = image[1:y, 1:x]
    crop_img_topR = image[1:y, x1:-1]
    
    crop_img_bottomL = image[y1:-1, 1:x]
    crop_img_bottomR = image[y1:-1, x1:-1]
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

def extract_image(image):
    """
    Returns borderless image

    :param image : Image with border
    :returns borderless image
    """
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    re, img = cv2.threshold(img, 125, 255, cv2.THRESH_BINARY)
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
    mask = np.full(image.shape[0:2],255,dtype=np.uint8)
    #mask = np.full((image.shape[0], image.shape[1],3), 255 ,dtype=np.uint8)
    cv2.drawContours(mask, [biggest_cont], -1, (255,255,255), thickness=5)
    #cv2.fillPoly(mask, pts=[biggest_cont], color=(0,0,0))
    sub_image = cv2.bitwise_and(image,image,mask)
    #sub_image = detect_orientation(sub_image)
    #sub_image = straighten(sub_image)
    return sub_image


class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5


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

    def image_to_desciption_text(image_path,feature):
        # print(image_path)
        with io.open(image_path, 'rb') as image_file:
            # print('debug1')
            content = image_file.read()
        # print('debug2')
        bounds=[]
        client = vision.ImageAnnotatorClient()
        image = vision.types.Image(content=content)
        response = client.document_text_detection(image=image)
        document = response.full_text_annotation
        for page in document.pages:
            for block in page.blocks:
                '''for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        for symbol in word.symbols:
                            if (feature == FeatureType.SYMBOL):
                                None
                                #bounds.append(symbol.bounding_box)
                                

                        if (feature == FeatureType.WORD):
                            None
                            #bounds.append(word.bounding_box)

                    if (feature == FeatureType.PARA):
                        None
                        #bounds.append(paragraph.bounding_box)
'''
                if (feature == FeatureType.BLOCK):
                    bounds.append(block.bounding_box)       
        return bounds
        
    block_vertices=image_to_desciption_text(image_path,FeatureType.BLOCK)
    return block_vertices 

def crop_image(img,arr):
    #mask = np.zeros(img.shape[0:2],255, dtype=np.uint8)
    mask = np.full(img.shape[0:2],255,dtype=np.uint8)
    points = np.array(arr)
    '''
    mask = np.full((image.shape[0], image.shape[1],3), 255 ,dtype=np.uint8)
    cv2.drawContours(mask, [biggest_cont], -1, (255,255,255), thickness=5)
    cv2.fillPoly(mask, pts=[biggest_cont], color=(0,0,0))
    sub_image = cv2.bitwise_or(image,mask)
    #sub_image = detect_orientation(sub_image)
    #sub_image = straighten(sub_image)
    cv2.imshow('test',sub_image)
    cv2.waitKey(0)
    return sub_image
    
    '''
    #method 1 smooth region
    cv2.drawContours(mask, [points], -1, (255, 255, 255), -1, cv2.LINE_AA)
    
    #method 2 not so smooth region
    # cv2.fillPoly(mask, points, (255))
    
    res = cv2.bitwise_and(img,img,mask = mask)
    rect = cv2.boundingRect(points) # returns (x,y,w,h) of the rect
    cropped = res[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]
    ## crate the white background of the same size of original image
    wbg = np.ones_like(img, np.uint8)*255
    cv2.bitwise_not(wbg,wbg, mask=mask)
    # overlap the resulted cropped image on the white background
    dst = wbg+res
    '''
    cv2.imshow('Original',img)
    cv2.imshow("Mask",mask)
    cv2.imshow("Cropped", cropped )
    cv2.imshow("Samed Size Black Image", res)
    cv2.imshow("Samed Size White Image", dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''
    
    return cropped

def alternate():
    while True:
        yield 0
        yield 1

if __name__=='__main__':
    #PATH='C:\\Users\\hello\\Desktop\\projects\\Doc_entity_extraction\\images\\r0100\\r0100_00.png'
    #PATH='C:\\Users\\hello\\Desktop\\projects\\Doc_entity_extraction\\images\\v2\\Lightroom\\out1.pdf_rot+scaled.jpg'
    #PATH = 'C:\\Users\\hello\\Desktop\\projects\\Doc_entity_extraction\\images\\v1\\h_180.jpg'
    PATH='C:\\Users\\hello\\Desktop\\projects\\Doc_entity_extraction\\dump_output1.jpg'
    name1 = 'topL.jpg'
    name2 = 'topR.jpg'
    name3 = 'bottomL.jpg'
    name4 = 'bottomR.jpg'
    image = cv2.imread(PATH)
    image1=np.copy(image)
    

    list_corner_images=denoising(image)
    list_corner_images_name=[name1,name2,name3,name4]
    for i,j in zip(list_corner_images_name,range(0,len(list_corner_images))):
        cv2.imwrite(i,list_corner_images[j])

    
    
    x_cordinates=[]
    y_cordinates=[]

    for i,j in zip(list_corner_images_name,range(0,len(list_corner_images_name))):
        list_points=extract_fields(i)
        xl,yl=find_vertices(list_points)
        xl = [item for item in xl if item >= 0]
        yl = [item for item in yl if item >= 0]
        
        if j==0:
            x_cordinates.append(min(xl))
            y_cordinates.append(min(yl))
        if j==1:
            x_cordinates.append(max(xl))
            y_cordinates.append(min(yl))
        if j==2:
            x_cordinates.append(min(xl))
            y_cordinates.append(max(yl))
        if j==3:
            x_cordinates.append(max(xl))
            y_cordinates.append(max(yl))
    

    image_width,image_height=image1.shape[1],image1.shape[0]   #1056,1425
    
    ##  POINTS  ##
    
    xtl,ytl=x_cordinates[0],y_cordinates[0]  #60,61
    xtr,ytr=(image_width-600)+x_cordinates[1],y_cordinates[1]
    xbl,ybl=x_cordinates[2],(image_height-600)+y_cordinates[2]
    xbr,ybr=(image_width-600)+x_cordinates[3],(image_height-600)+y_cordinates[3]
    
    ###DRAW BOUNDARY#####
    '''
    pts = np.array([[xtl,ytl],[xtr,ytr],[xbr,ybr],[xbl,ybl]], np.int32)
    pts = pts.reshape((-1,1,2))
    image_draw_boundary=cv2.polylines(image1,[pts],True,(255,0,0))
    cv2.imshow('Boundary Image',image_draw_boundary)
    cv2.waitKey(0)
    name_boundary = 'boundary_result.jpg'
    cv2.imwrite(name_boundary,image_draw_boundary)
    '''
    ### CROPPING ###

    
    name_cropping = 'cropping_result.jpg'
    np_array=list([[xtl,ytl],[xtr,ytr],[xbr,ybr],[xbl,ybl]])
    image_cropped=crop_image(image1,np_array)
    cv2.imwrite(name_cropping,image_cropped)
    

    ### 2nd ROUND PREPROCESS ####

    PATH2='C:\\Users\\hello\\Desktop\\projects\\Doc_entity_extraction\\cropping_result.jpg'
    image=scripts.preprocessing.detect_orientation(image_cropped)
    image=scripts.preprocessing.straighten(image)
    image=extract_image(image)   
    name_final_output='final_output.jpg'
    cv2.imwrite(name_final_output,image)


    #### BEFORE AND AFTER ####
    scripts.preprocessing.plot_before_after(image1,image,"Before and After",save=False,show=True)