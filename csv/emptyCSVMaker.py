import csv

def createHeaderCSV(filename, header_row):
    with open('..\\csv\\{0}.csv'.format(filename),'w') as file:
        writer_obj = csv.writer(file)
        writer_obj.writerow(header_row)
    return True

filename = 'IRSEntityExtraction'
header_row = ("First name",
              "Home Address",
              "City, town and zip code",
              "SSN",
              "Waqes or Salaries"
              "Adjusted Gross Income")
print(createHeaderCSV(filename,header_row))