import numpy as np
import matplotlib.pyplot as plt
import sys
import os

caffe_root = './caffe/'   #the relative location of caffe
sys.path.insert(0, caffe_root+'python')
import caffe


def setUpNet():
    if os.path.isfile(caffe_root + 'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel'):
        print 'CaffeNet found.'
    else:
        print 'You have to download the pre-trained CaffeNet model first.'
    caffe.set_mode_cpu()    
    model_def = caffe_root + 'models/bvlc_reference_caffenet/deploy.prototxt'
    model_weights = caffe_root + 'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel'
    net = caffe.Net(model_def,      # defines the structure of the model
                    model_weights,  # contains the trained weights
                    caffe.TEST)
    return net

def createTransformer(net) :
    # load the mean ImageNet image (as distributed with Caffe) for subtraction
    mu = np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy')
    mu = mu.mean(1).mean(1)  # average over pixels to obtain the mean (BGR) pixel values
    # print 'mean-subtracted values:', zip('BGR', mu)

    # create transformer for the input called 'data'
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

    transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
    transformer.set_mean('data', mu)            # subtract the dataset-mean value in each channel
    transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
    transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR
    return transformer



def classifyImg(net, transformer, path):
    # net = setUpNet()
    # transformer = createTransformer(net)
    image = caffe.io.load_image(path)
    transformed_image = transformer.preprocess('data', image)
    plt.imshow(image)
    # copy the image data into the memory allocated for the net
    net.blobs['data'].data[...] = transformed_image

    ### perform classification
    output = net.forward()
    output_prob = output['prob'][0]  # the output probability vector for the first image in the batch

    # print 'predicted class is:', output_prob.argmax()

    #load labels
    labels_file = caffe_root + 'data/ilsvrc12/synset_words.txt'
    if not os.path.exists(labels_file):
        print('no label files')     
    labels = np.loadtxt(labels_file, str, delimiter='\t')
    print '>>>output label:', labels[output_prob.argmax()]
    return labels[output_prob.argmax()]
    # sort top five predictions from softmax output
    # top_inds = output_prob.argsort()[::-1][:5]  # reverse sort and take five largest items

    # print '>>>probabilities and labels:', zip(output_prob[top_inds], labels[top_inds])

