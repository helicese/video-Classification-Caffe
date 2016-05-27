import numpy as np
import cv2
import os

videoPath = './video/demo.mp4'
videoName = 'demo'
cap = cv2.VideoCapture(videoPath)

#video information
def getVideoInfo(captureItem):	
	fps = captureItem.get(cv2.CAP_PROP_FPS)
	size = (int(captureItem.get(cv2.CAP_PROP_FRAME_WIDTH)),   
	        int(captureItem.get(cv2.CAP_PROP_FRAME_HEIGHT)))
	fNum = cap.get(cv2.CAP_PROP_FRAME_COUNT)
	print("fps: ",fps, "size: ", size, "frameNumber: ", fNum)
	return (fps, size, fNum) 

def mkdir(path):
    path=path.strip() 
    isExists=os.path.exists(path)
 
    if not isExists:
        print path+' create success'
        os.makedirs(path)
        return True
    else:
        print path+' exists'
        return False


sRet, sFrame = cap.read()

catgory, count = 0, 0
if not sRet:
	print("error: no video available")
mkdir('./img/'+videoName+'/')
while(cap.isOpened()):
    # Capture the first and second frame
    fRet, fFrame = sRet, sFrame
    sRet, sFrame = cap.read()

    if sRet:
	    # Our operations on the frame come here
        fHist = cv2.calcHist([fFrame], [0,1,2], None, [64,64,64], [0, 255, 0, 255, 0, 255])
        sHist = cv2.calcHist([sFrame], [0,1,2], None, [64,64,64], [0, 255, 0, 255, 0, 255])
        result = cv2.compareHist(fHist, sHist, cv2.HISTCMP_CORREL)
        posFrame = cap.get(cv2.CAP_PROP_POS_FRAMES)
        if posFrame % 10 == 0 :
        	count += 1
        	name = './img/'+videoName+'/'+str(catgory) + '_' + str(count)+'.jpg'
        	print(name)
        	cv2.imwrite(name, sFrame)
        
        if result < 0.9:
            count = 0
            catgory += 1
            print(">>> ", result)
            print('position: ', cap.get(cv2.CAP_PROP_POS_FRAMES)/cap.get(cv2.CAP_PROP_FRAME_COUNT))
	    # Display the resulting frame
            cv2.imshow('sFrame',sFrame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
	        break
    else:
		break

# When everything done, release the capture
getVideoInfo(cap)
cap.release()
cv2.destroyAllWindows()