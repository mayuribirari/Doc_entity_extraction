import cv2
spottedImage = cv2.imread(r'D:\Hvantage\Doc_entity_extraction\images\v3\r0000_00.png')
spottedImageCopy = spottedImage.copy()
spottedImageResolution = spottedImage.shape[0]*spottedImage.shape[1]
thresholdArea = 30
print(thresholdArea)
spottedImageGrayscale = cv2.cvtColor(spottedImage,cv2.COLOR_RGB2GRAY)
spottedImageThresh = cv2.threshold(spottedImageGrayscale,10,255,cv2.THRESH_BINARY)[1]
contoursSpottedImage,_ = cv2.findContours(spottedImageThresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for contour in contoursSpottedImage:
    polygonicCountour = cv2.approxPolyDP(contour,epsilon= 0.1*cv2.arcLength(contour,True),closed = True)
    area = cv2.contourArea(polygonicCountour)
    if area < thresholdArea and area:
        print(area)
        cv2.drawContours(spottedImage, [contour],-1,(0,0,255),3)
        cv2.fillPoly(spottedImageCopy,pts = [contour],color=(255,255,255))
# cv2.imshow("Result1",cv2.resize(spottedImage,(0,0),fx=0.35,fy=0.35))
horizontalStackingResult = cv2.hconcat([spottedImageCopy,spottedImage])
# cv2.imshow("Result",horizontalStackingResult)
cv2.imwrite("spotRemoved.jpg",horizontalStackingResult)
cv2.waitKey(0)
cv2.destroyAllWindows()