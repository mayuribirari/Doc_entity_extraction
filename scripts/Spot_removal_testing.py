import cv2
spottedImage = cv2.imread(r'D:\Hvantage\Doc_entity_extraction\scripts\Spots.png')
spottedImageCopy = spottedImage.copy()
spottedImageResolution = spottedImage.shape[0]*spottedImage.shape[1]
thresholdArea = 0.00085*spottedImageResolution
spottedImageGrayscale = cv2.cvtColor(spottedImage,cv2.COLOR_RGB2GRAY)
spottedImageThresh = cv2.threshold(spottedImageGrayscale,160,255,cv2.THRESH_BINARY)[1]
contoursSpottedImage,_ = cv2.findContours(spottedImageThresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for contour in contoursSpottedImage:
    polygonicCountour = cv2.approxPolyDP(contour,epsilon= 0.1*cv2.arcLength(contour,True),closed = True)
    area = cv2.contourArea(polygonicCountour)
    if area < thresholdArea:
        cv2.drawContours(spottedImage, [contour],-1,(0,255,0),0)
        cv2.fillPoly(spottedImage,pts = [contour],color=(255,255,255))
horizontalStackingResult = cv2.hconcat([spottedImageCopy,spottedImage])
cv2.imshow("Result",horizontalStackingResult)
cv2.imwrite('spotRemovedTesting.jpg',horizontalStackingResult)
cv2.waitKey(0)
cv2.destroyAllWindows()