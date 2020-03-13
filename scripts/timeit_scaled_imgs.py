
import concurrent.futures

code1 = '''
d = pytesseract.image_to_string(image=img1)
'''

code2 = '''
d = pytesseract.image_to_string(image = img2)
'''


def action(code):
    import timeit
    NUMBER = 100
    setup = '''
import cv2
import pytesseract
img1 = cv2.imread('..\images\j.JPG')
img2 = cv2.imread('..\images\j_scaled50.jpg')
    '''
    return timeit.timeit(stmt=code, setup=setup, number=NUMBER)


# print(timeit.timeit(stmt = code1,setup=setup + "img1 = cv2.imread('..\images\j.JPG')",number=100)) #47.084535599999995
# print(timeit.timeit(stmt = code2,setup=setup + "img2 = cv2.imread('..\images\j_scaled50.jpg')",number=100)) #78.6073261

if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor() as executor:
        f1: concurrent.futures.Future = executor.submit(action, code1)
        f2: concurrent.futures.Future = executor.submit(action, code2)
        print(f1.result())  # 71.19418089999999
        print(f2.result())  # 112.1429165
