# import imgClassify as iC
import videoSplit as vS
from PIL import Image
import time
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import logging
import pandas as pd
import cPickle
import exifutil

REPO_DIRNAME = './caffe/'   #the relative location of caffe
sys.path.insert(0, REPO_DIRNAME+'python')
import caffe
print ('>>>: ',REPO_DIRNAME)



# print(splitVideo(videoPath))
logging.getLogger().setLevel(logging.INFO)

class ImagenetClassifier(object):
    print ('>>>: ',REPO_DIRNAME)
    default_args = {
        'model_def_file': (
            '{}/models/bvlc_reference_caffenet/deploy.prototxt'.format(REPO_DIRNAME)),
        'pretrained_model_file': (
            '{}/models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel'.format(REPO_DIRNAME)),
        'mean_file': (
            '{}/python/caffe/imagenet/ilsvrc_2012_mean.npy'.format(REPO_DIRNAME)),
        'class_labels_file': (
            '{}/data/ilsvrc12/synset_words.txt'.format(REPO_DIRNAME)),
        'bet_file': (
            '{}/data/ilsvrc12/imagenet.bet.pickle'.format(REPO_DIRNAME)),
    }
    for key, val in default_args.iteritems():
        if not os.path.exists(val):
            raise Exception(
                "File for {} is missing. Should be at: {}".format(key, val))
    default_args['image_dim'] = 256
    default_args['raw_scale'] = 255.

    def __init__(self, model_def_file, pretrained_model_file, mean_file,
                 raw_scale, class_labels_file, bet_file, image_dim, gpu_mode):
        logging.info('Loading net and associated files...')
        if gpu_mode:
            caffe.set_mode_gpu()
        else:
            caffe.set_mode_cpu()
        self.net = caffe.Classifier(
            model_def_file, pretrained_model_file,
            image_dims=(image_dim, image_dim), raw_scale=raw_scale,
            mean=np.load(mean_file).mean(1).mean(1), channel_swap=(2, 1, 0)
        )

        with open(class_labels_file) as f:
            labels_df = pd.DataFrame([
                {
                    'synset_id': l.strip().split(' ')[0],
                    'name': ' '.join(l.strip().split(' ')[1:]).split(',')[0]
                }
                for l in f.readlines()
            ])
        self.labels = labels_df.sort('synset_id')['name'].values

        self.bet = cPickle.load(open(bet_file))
        # A bias to prefer children nodes in single-chain paths
        # I am setting the value to 0.1 as a quick, simple model.
        # We could use better psychological models here...
        self.bet['infogain'] -= np.array(self.bet['preferences']) * 0.1

    def classify_image(self, image):
        try:
            starttime = time.time()
            scores = self.net.predict([image], oversample=True).flatten()
            endtime = time.time()

            indices = (-scores).argsort()[0]
            predictions = self.labels[indices]

            logging.info('result: %s', str(predictions))

            return (True, predictions, '%.3f' % (endtime - starttime))

        except Exception as err:
            logging.info('Classification error: %s', err)
            return (False, 'Something went wrong when classifying the '
                           'image. Maybe try another one?')

# Initialize classifier + warm start by forward for allocation
ImagenetClassifier.default_args.update({'gpu_mode': False})
classifier = ImagenetClassifier(**ImagenetClassifier.default_args)
classifier.net.forward()


def getFileList(path):
    path = str(path)
    if path=="":
        return []
    a = os.listdir(path)
    b = [x for x in a if os.path.isfile(path + x)]
    return sorted(b)

def doTheClassify(path) :
    try:
        image = caffe.io.load_image(path)
    except Exception, err:
        logging.info('image open error: %s', err)

    return classifier.classify_image(image)

def classifyVideo(videoPath):
    #videoInfo = {struct, imgDir}
    videoInfo = vS.splitVideo(videoPath)

    imgList = getFileList(videoInfo['imgDir'])

    classResult = []
    catgory = '-1'
    count = -1
    for imgName in imgList:
        formerCat = catgory
        catgory = os.path.splitext(imgName)[0][:2]
        imgPath = videoInfo['imgDir']+imgName
        if formerCat == catgory:
            classResult[count].append(doTheClassify(imgPath)[1])
        else:
            count += 1
            classResult.append([])
            classResult[count].append(doTheClassify(imgPath)[1])
    finalResult = {}
    finalResult['struct'] = videoInfo['struct']
    finalResult['class'] = classResult
    return finalResult

# print classifyVideo(videoPath)