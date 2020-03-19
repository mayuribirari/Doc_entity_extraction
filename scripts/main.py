def preprocess(PATH):
    import scripts.main_preprocess
    image = scripts.main_preprocess.preprocess(PATH)
    return image


def extract_fields(image):
    import os
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'json\\Handwritting Recognission-2cf8babac416.json'

    # Code by Mayuri
    # PROJECT_ID = 'handwritting-recognission'
    # SESSION_ID = '123'
    return fields


def convert_to_csv(fields):
    import csv
    import pandas as pd
    titles = ("Buyer Name", "Property address", "Purchase Price", "Seller Brokerage Firm & License Number",
              "Buyers Brokerage Firm & License Number", "Initial Deposit", "Balance Downpayment", "Purchase Price",
              "Date Prepared"
              )
    with open('Extracted_Entities.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(titles)
        writer.writerow(fields)
    df = pd.read_csv('Extracted_Entities.csv')
    print(df)



PATH = '..\\images\\v2\\Lightroom\\out1.pdf_scaled_80.jpg'
image = preprocess(PATH)
fields = extract_fields(image)
convert_to_csv(fields)
