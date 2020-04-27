import os
path = '..\\images\\v1'
# PATH = '..\\images\\v1\\h_baap.JPG'
os.chdir(path)
images = os.listdir()
images = [i for i in images if i[-4:] == '.JPG' or  i[-4:] == '.jpg']
print(images)

def preprocess(PATH):
    import scripts.main_preprocess
    image = scripts.main_preprocess.preprocess(PATH)
    return image


for i in images:
    print('*'*40 ,i, '*'*40)
    image = preprocess(i)
    break
