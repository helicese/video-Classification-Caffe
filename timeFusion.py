import videoClassify as vC

# videoPath = './video/Megamind.avi'
# rawData = {'struct': [0.37, 0.57, 0.74], 'class': [['bow tie', 'harmonica', 'bow tie', 'bow tie', 'bow tie', 'harmonica', 'harmonica', 'bow tie', 'bow tie'], ['drumstick', 'drumstick', 'hand blower', 'punching bag', 'punching bag', 'hair spray'], ['bow tie', 'bow tie', 'drumstick', 'bow tie', 'bow tie'], ['Band Aid', 'Band Aid', 'bow tie', 'bow tie', 'Band Aid', 'Band Aid', 'mask']]}

def process(index, item):
    print str(index) + ': '
    print item

def voting(vT, item, score):
    if item not in vT:
        vT[item] = 0
    vT[item] += score 
    return vT

def getFinal(videopath):
    rawData = vC.classifyVideo(videopath)
    classList = rawData['class']
    result = {}
    newList = []
    for index, item in enumerate(classList):
        a = []
        # voting = list(set(item))
        for i in xrange(len(item)):
            # process(index, item)
            vT = {}
            if i == 0:
                a.append(item[0])
            elif i == 1:
                a.append(item[1])
            elif i == 2:
                vT = voting(vT, item[0], 1)
                vT = voting(vT, item[1], 1.2)
                vT = voting(vT, item[2], 1.5)
                a.append(sorted(vT.items(), key=lambda vT:-vT[1])[0][0])
            elif i == 3:
                vT = voting(vT, item[0], 1)
                vT = voting(vT, item[1], 2)
                vT = voting(vT, item[2], 3.2)
                vT = voting(vT, item[3], 4.1)
                a.append(sorted(vT.items(), key=lambda vT:-vT[1])[0][0])
            else :
                vT = voting(vT, item[i-4], 1)
                vT = voting(vT, item[i-3], 2)
                vT = voting(vT, item[i-2], 2.1)
                vT = voting(vT, item[i-1], 2.3)
                vT = voting(vT, item[i], 3.1)
                a.append(sorted(vT.items(), key=lambda vT:-vT[1])[0][0])
        newList.append(a)
        result['struct'] = rawData['struct']
        result['raw'] = rawData['class']
        result['new'] = newList
    return result

# print getFinal(videoPath)

# [['bow tie', 'harmonica', 'bow tie', 'bow tie', 'bow tie', 'harmonica', 'harmonica', 'bow tie', 'bow tie'], ['drumstick', 'drumstick', 'hand blower', 'punching bag', 'punching bag', 'hair spray'], ['bow tie', 'bow tie', 'drumstick', 'bow tie', 'bow tie'], ['Band Aid', 'Band Aid', 'bow tie', 'bow tie', 'Band Aid', 'Band Aid', 'mask']]
# [['bow tie', 'harmonica', 'bow tie', 'bow tie', 'bow tie', 'bow tie', 'bow tie', 'bow tie', 'bow tie'], ['drumstick', 'drumstick', 'drumstick', 'punching bag', 'punching bag', 'punching bag'], ['bow tie', 'bow tie', 'bow tie', 'bow tie', 'bow tie'], ['Band Aid', 'Band Aid', 'Band Aid', 'bow tie', 'Band Aid', 'Band Aid', 'Band Aid']]
# [['bow tie', 'harmonica', 'bow tie', 'bow tie', 'bow tie', 'bow tie', 'harmonica', 'bow tie', 'bow tie'], ['drumstick', 'drumstick', 'drumstick', 'punching bag', 'punching bag', 'punching bag'], ['bow tie', 'bow tie', 'bow tie', 'bow tie', 'bow tie'], ['Band Aid', 'Band Aid', 'Band Aid', 'bow tie', 'Band Aid', 'Band Aid', 'Band Aid']]