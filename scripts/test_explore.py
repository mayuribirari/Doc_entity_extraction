import cv2
img = cv2.imread('0.jpg')
img_padded = cv2.copyMakeBorder(img,100,100,100,100,cv2.BORDER_WRAP,value=(255,255,255))


cv2.imshow('Padding_test',img_padded)
cv2.waitKey(0)
cv2.destroyAllWindows()