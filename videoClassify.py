import imgClassify as iC
import videoSplit as vS
import os

cwd = os.getcwd()
print(cwd)
# imgPath = os.listdir('./img/Megamind/')
# print(imgPath)
# videoPath = './video/Megamind.avi'
# print(splitVideo(videoPath))
def getFileList(path):
    path = str(path)
    if path=="":
        return []
    a = os.listdir(path)
    b = [x for x in a if os.path.isfile(path + x)]
    return sorted(b)

def classifyVideo(videoPath):
    #videoInfo = {struct, imgDir}
    videoInfo = vS.splitVideo(videoPath)

    imgList = getFileList(videoInfo['imgDir'])
    net = iC.setUpNet()
    transformer = iC.createTransformer(net)

    classResult = []
    catgory = '-1'
    count = -1
    for imgName in imgList:
        formerCat = catgory
        catgory = os.path.splitext(imgName)[0][:2]
        imgPath = videoInfo['imgDir']+imgName
        print imgPath
        if formerCat == catgory:
            classResult[count].append(iC.classifyImg(net, transformer, imgPath))
        else:
            count += 1
            print count
            classResult.append([])
            classResult[count].append(iC.classifyImg(net, transformer, imgPath))
        # result.append(iC.classfyImg(net, transformer, imgPath))
    print classResult
    finalResult = {}
    finalResult['struct'] = videoInfo['struct']
    finalResult['class'] = classResult
    return finalResult

# print classifyVideo(videoPath)