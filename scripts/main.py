def preprocess(PATH):
    import scripts.main_preprocess
    image = scripts.main_preprocess.preprocess(PATH)
    return image


# def extract_fields(x):
#     import os
#     import io
#     from google.cloud import vision
#     # print(os.getcwd())
#     image_path = os.getcwd()+'\\'+x
#     # print(image_path)
#     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '..\\json\\Handwritting Recognission-2cf8babac416.json'
#     PROJECT_ID = 'handwritting-recognission'
#     SESSION_ID = '123'
#
#     def image_to_desciption_text(image_path):
#         # print(image_path)
#         with io.open(image_path, 'rb') as image_file:
#             # print('debug1')
#             content = image_file.read()
#         # print('debug2')
#         client = vision.ImageAnnotatorClient()
#         image = vision.types.Image(content=content)
#         response = client.text_detection(image=image)
#         return response.text_annotations[0].description
#
#     print(image_to_desciption_text(image_path))
#     # return fields
#     return None
#
# def convert_to_csv(fields):
#     import csv
#     import pandas as pd
#     titles = ("Buyer Name", "Property address", "Purchase Price", "Seller Brokerage Firm & License Number",
#               "Buyers Brokerage Firm & License Number", "Initial Deposit", "Balance Downpayment", "Purchase Price",
#               "Date Prepared"
#               )
#     with open('Extracted_Entities.csv', 'w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(titles)
#         writer.writerow(fields)
#     df = pd.read_csv('Extracted_Entities.csv')
#     print(df)


import os

# PATH = '..\\images\\v2\\Lightroom\\out1.pdf_border_black.jpg'
# PATH = '..\\images\\v2\\Lightroom\\out1.pdf_rot+scaled.jpg'
 # PATH = '..\\images\\v2\\Lightroom\\out1.pdf_180+rot+scaled.jpg'
# PATH = '..\\images\\v2\\Lightroom\\out1.pdf_left_skewed_10.jpg'
# PATH = '..\\images\\v2\\Lightroom\\out1.pdf_normal.jpg'
# PATH = '..\\images\\v2\\Lightroom\\out1.pdf_right_skewed8.JPG'
# PATH = '..\\images\\v2\\Lightroom\\out1.pdf_scaled_80.jpg'
# PATH = '..\\images\\v2\\Lightroom\\out1.pdf_90+border.jpg'
PATH = '..\\images\\v2\\out8.pdf.jpg'



# PATH = '..\\images\\v3\\r0000_00.png'
# PATH = '..\\images\\v3\\r0100_00.png'


image_name = preprocess(PATH)
# print(os.getcwd(),type(image_name))
image_name = "dump_output1.jpg"
# extract_fields(image_name)
# extract_fields(image,img_folder_path)

