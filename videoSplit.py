import numpy as np
import cv2
import os

#video information
def getVideoInfo(captureItem):	
	fps = captureItem.get(cv2.CAP_PROP_FPS)
	size = (int(captureItem.get(cv2.CAP_PROP_FRAME_WIDTH)),   
	        int(captureItem.get(cv2.CAP_PROP_FRAME_HEIGHT)))
	fNum = captureItem.get(cv2.CAP_PROP_FRAME_COUNT)
	print("fps: ",fps, "size: ", size, "frameNumber: ", fNum)
	return (fps, size, fNum) 

#make dir for img saving
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

def formatNum(num):
    if num<10:
        return '0'+str(num)
    else:
        return str(num)

def splitVideo(videoPath):
    cap = cv2.VideoCapture(videoPath)

    #videoName = [name, postfix]
    videoName = os.path.splitext(os.path.split(videoPath)[1])
    sRet, sFrame = cap.read()
    catgory, count = 0, 0
    result = {}
    progress = []
    imgDir = './img/'+videoName[0]+'/'
    if not sRet:
    	print("error: no video available")
    mkdir(imgDir)
    while(cap.isOpened()):
        # Capture the first and second frame
        fRet, fFrame = sRet, sFrame
        sRet, sFrame = cap.read()

        if sRet:
    	    # Our operations on the frame come here
            fHist = cv2.calcHist([fFrame], [0,1,2], None, [128,128,128], [0, 255, 0, 255, 0, 255])
            sHist = cv2.calcHist([sFrame], [0,1,2], None, [128,128,128], [0, 255, 0, 255, 0, 255])
            hResult = cv2.compareHist(fHist, sHist, cv2.HISTCMP_CORREL)
            posFrame = cap.get(cv2.CAP_PROP_POS_FRAMES)

            if posFrame % 10 == 0 :
            	count += 1
            	name = './img/'+videoName[0]+'/'+formatNum(catgory) + '_' + formatNum(count)+'.jpg'
            	print(name)
            	cv2.imwrite(name, sFrame)
            ##############################to be done
            # count >= 5 to avoid being too short
            if hResult < 0.8 and count >= cap.get(cv2.CAP_PROP_FRAME_COUNT)/100:
                count = 0
                catgory += 1
                progress.append(round(cap.get(cv2.CAP_PROP_POS_FRAMES)/cap.get(cv2.CAP_PROP_FRAME_COUNT),2))
                print(">>> ", hResult)
                print('position: ', progress)
    	    # Display the resulting frame
            ##############################   
            if cv2.waitKey(1) & 0xFF == ord('q'):
    	        break
        else:
    		break
    # When everything done, release the capture
    if progress == []:
        progress.append(1)

    result['struct'] = progress
    result['imgDir'] = imgDir
    getVideoInfo(cap)
    cap.release()
    return result



