import cv2
import numpy as np

fFrame = cv2.imread('./img/beauty01.jpg')
sFrame = cv2.imread('./img/beauty02.jpg')

fHist = cv2.calcHist([fFrame], [0,1,2], None, [256,256,256], [0, 255, 0, 255, 0, 255])
sHist = cv2.calcHist([sFrame], [0,1,2], None, [256,256,256], [0, 255, 0, 255, 0, 255])
result = cv2.compareHist(fHist, sHist, cv2.HISTCMP_CORREL)
print(fHist)
print(">>>")
print(sHist)
print(">>>")
print(result)