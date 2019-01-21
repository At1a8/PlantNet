#!/usr/bin/python
# -*- coding:utf-8 -*-

import os,sys
import cv2
import numpy as np
root='/home/omnisky/caffe/'#根目录 
os.chdir(root)
sys.path.insert(0,root+'python')
import caffe
import json

caffe.set_device(0)
caffe.set_mode_gpu()

alexnet_deploy='/data/chenhongbo/caffe/1-alexnet_match_new_trainval/alexnet_test_image.prototxt'#模型对应的deploy文件
#alexnet_model='/data/chenhongbo/caffe/1-alexnet_match_new_trainval/models_1/alexnet_finetune_cfg000_iter_32000.caffemodel'#训练好的model
alexnet_model='/data/chenhongbo/caffe/1-alexnet_match_new_trainval/models/alexnet_finetune_cfg000_iter_32000.caffemodel'#训练好的model

#vgg16_deploy='/data/chenhongbo/caffe/1-vgg16_match_new_trainval/deploy.prototxt'#模型对应的deploy文件
#vgg16_model='/data/chenhongbo/caffe/1-vgg16_match_new_trainval/models_1/vgg16_iter_18000.caffemodel'
vgg16_deploy='/data/chenhongbo/caffe/1-resnet50_match_new_trainval/deploy.prototxt'#模型对应的deploy文件
vgg16_model='/data/chenhongbo/caffe/1-resnet50_match_new_trainval/models/resnet-50-cervix_iter_44000.caffemodel'

googlenet_deploy='/data/chenhongbo/caffe/1-googlenet_match_new_trainval/deploy.prototxt'#模型对应的deploy文件
#googlenet_model='/data/chenhongbo/caffe/1-googlenet_match_new_trainval/models_00/bvlc_googlenet_iter_34000.caffemodel'
googlenet_model='/data/chenhongbo/caffe/1-googlenet_match_new_trainval/models/bvlc_googlenet_iter_58000.caffemodel'

#googlenet_deploy='/data/chenhongbo/caffe/1-inception-v4_match_new_trainval/deploy.prototxt'#模型对应的deploy文件
#googlenet_model='/data/chenhongbo/caffe/1-inception-v4_match_new_trainval/models/inception-v4-cervix_iter_24000.caffemodel'


dir ='/data/data_disease_61class/testB'#数据路径

correct_num = 0

filelist=[]#用于存放完整路径以及文件名
filenames=os.listdir(dir)#读入在某个目录下的所有文件
for fn in filenames:
    fullfilename = os.path.join(dir,fn)
    filelist.append(fullfilename)#连接成完整路径
#filelist.append(fn)

def Test():
    alexnet_net = caffe.Net(alexnet_deploy,alexnet_model,caffe.TEST)#加载model和network 
    vgg16_net = caffe.Net(vgg16_deploy,vgg16_model,caffe.TEST)#加载model和network  
    googlenet = caffe.Net(googlenet_deploy,googlenet_model,caffe.TEST)#加载model和network  

    alexnet_transformer = caffe.io.Transformer({'data':alexnet_net.blobs['data'].data.shape}) #设定图片的shape格式(1,3,28,28)  
    alexnet_transformer.set_mean('data', np.load('/data/chenhongbo/caffe/0-db_match_new/ilsvrc_2012_mean.npy').mean(1).mean(1)) 
    alexnet_transformer.set_transpose('data', (2,0,1))
    alexnet_transformer.set_channel_swap('data', (2,1,0))
    alexnet_transformer.set_raw_scale('data', 255.0)

    vgg16_transformer = caffe.io.Transformer({'data':vgg16_net.blobs['data'].data.shape}) #设定图片的shape格式(1,3,28,28)  
    vgg16_transformer.set_mean('data', np.load('/data/chenhongbo/caffe/0-db_match_new/ilsvrc_2012_mean.npy').mean(1).mean(1)) 
    vgg16_transformer.set_transpose('data', (2,0,1))
    vgg16_transformer.set_channel_swap('data', (2,1,0))
    vgg16_transformer.set_raw_scale('data', 255.0)

    googlenet_transformer = caffe.io.Transformer({'data':googlenet.blobs['data'].data.shape}) #设定图片的shape格式(1,3,28,28)  
    googlenet_transformer.set_mean('data', np.load('/data/chenhongbo/caffe/0-db_match_new/ilsvrc_2012_mean.npy').mean(1).mean(1)) 
    googlenet_transformer.set_transpose('data', (2,0,1))
    googlenet_transformer.set_channel_swap('data', (2,1,0))
    googlenet_transformer.set_raw_scale('data', 255.0)

    json_result = []

    for i in range(0,len(filelist)):
        global correct_num
        img=filelist[i]
        img_name = os.path.basename(img)
        index = img_name.find("_")
        fact_class = img_name[:index]
        img2=img[:-4]+'_resize'+img[-4:]

        im_ori = cv2.imread(img)
        sp = im_ori.shape
        im_height = sp[0]
        im_width = sp [1]
        if (im_height>im_width):
            im_new_height=int(256*im_height/im_width)
            im_new_width=256
        else:
            im_new_width=int(256*im_width/im_height)
            im_new_height=256
        size = (im_new_width,im_new_height)

        im_resize=cv2.resize(im_ori,size,interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(img2,im_resize)
  
        im = caffe.io.load_image(img2)#加载图片到数据层
        os.remove(img2)   

        alexnet_net.blobs['data'].reshape(1,3,227,227)
        alexnet_net.blobs['data'].data[...] = alexnet_transformer.preprocess('data', im) 
        alexnet_out = alexnet_net.forward()
        alexnet_prob1 = max(alexnet_net.blobs['prob'].data[0])
        alexnet_top_k1 = alexnet_net.blobs['prob'].data[0].flatten().argsort()[-1]
        alexnet_top_k2 = alexnet_net.blobs['prob'].data[0].flatten().argsort()[-2]
        alexnet_top_k3 = alexnet_net.blobs['prob'].data[0].flatten().argsort()[-3]
        alexnet_prob2 = alexnet_net.blobs['prob'].data[0][int(alexnet_top_k2)]
        alexnet_prob3 = alexnet_net.blobs['prob'].data[0][int(alexnet_top_k3)]
        #print 'alexnet_top_k:',alexnet_top_k
        #print 'alexnet_prob:',alexnet_prob

        vgg16_net.blobs['data'].reshape(1,3,224,224)
        vgg16_net.blobs['data'].data[...] = vgg16_transformer.preprocess('data', im)
        vgg16_net_out = vgg16_net.forward()
        vgg16_prob1 = max(vgg16_net.blobs['prob'].data[0])
        vgg16_top_k1 = vgg16_net.blobs['prob'].data[0].flatten().argsort()[-1]
        vgg16_top_k2 = vgg16_net.blobs['prob'].data[0].flatten().argsort()[-2]
        vgg16_top_k3 = vgg16_net.blobs['prob'].data[0].flatten().argsort()[-3]
        vgg16_prob2 = vgg16_net.blobs['prob'].data[0][int(vgg16_top_k2)]
        vgg16_prob3 = vgg16_net.blobs['prob'].data[0][int(vgg16_top_k3)]
        #print 'vgg16_top_k:',vgg16_top_k
        #print 'vgg16_prob:',vgg16_prob

        googlenet.blobs['data'].reshape(1,3,224,224)
        #googlenet.blobs['data'].reshape(1,3,299,299)
        googlenet.blobs['data'].data[...] = googlenet_transformer.preprocess('data', im)
        googlenet_out = googlenet.forward()
        googlenet_prob1 = max(googlenet.blobs['prob'].data[0])
        googlenet_top_k1 = googlenet.blobs['prob'].data[0].flatten().argsort()[-1]
        googlenet_top_k2 = googlenet.blobs['prob'].data[0].flatten().argsort()[-2]
        googlenet_top_k3 = googlenet.blobs['prob'].data[0].flatten().argsort()[-3]
        googlenet_prob2 = googlenet.blobs['prob'].data[0][int(googlenet_top_k2)]
        googlenet_prob3 = googlenet.blobs['prob'].data[0][int(googlenet_top_k3)]
        #print 'googlenet_top_k:',googlenet_top_k
        #print 'googlenet_prob:',googlenet_prob

        '''new_img = np.zeros((4,61),dtype='uint8')
        for j in range(61):
            new_img[0,j] = np.uint8(alexnet_net.blobs['prob'].data[0][j]*255)
            new_img[1,j] = np.uint8(resnet50_net.blobs['prob'].data[0][j]*255)
            new_img[2,j] = np.uint8(googlenet_net.blobs['prob'].data[0][j]*255)
            new_img[3,j] = np.uint8(vgg16_net.blobs['prob'].data[0][j]*255)
        cv2.imwrite('/data/workspace/chenhongbo/caffe/new_data_val/'+img_name,new_img)'''

        top_k_prob = -1
        top_k = -1
        dic  = {}
        dic[alexnet_top_k1] = alexnet_prob1
        dic[alexnet_top_k2] = alexnet_prob2
        dic[alexnet_top_k3] = alexnet_prob3
        if vgg16_top_k1 in dic :
            dic[vgg16_top_k1] =  dic[vgg16_top_k1] + vgg16_prob1
        else :
            dic[vgg16_top_k1] =  vgg16_prob1
        if vgg16_top_k2 in dic :
            dic[vgg16_top_k2] =  dic[vgg16_top_k2] + vgg16_prob2
        else :
            dic[vgg16_top_k2] =  vgg16_prob2
        if vgg16_top_k3 in dic :
            dic[vgg16_top_k3] =  dic[vgg16_top_k3] + vgg16_prob3
        else :
            dic[vgg16_top_k3] =  vgg16_prob3

        if googlenet_top_k1 in dic :
            dic[googlenet_top_k1] =  dic[googlenet_top_k1] + googlenet_prob1
        else :
            dic[googlenet_top_k1] =  googlenet_prob1
        if googlenet_top_k2 in dic :
            dic[googlenet_top_k2] =  dic[googlenet_top_k2] + googlenet_prob2
        else :
            dic[googlenet_top_k2] =  googlenet_prob2
        if googlenet_top_k3 in dic :
            dic[googlenet_top_k3] =  dic[googlenet_top_k3] + googlenet_prob3
        else :
            dic[googlenet_top_k3] =  googlenet_prob3
        
        for key, value in dic.items():
            if value > top_k_prob:
                top_k_prob = value
                top_k = key
        if (top_k == -1):
            print '################################'
            print '################################'
            print '################################'
  
        print img_name,',the class is:',top_k

        #if fact_class == str(top_k):
        #    correct_num = correct_num+1

        #f=file("/data/workspace/chenhongbo/caffe/1-alexnet_match/recognition_result.txt","a")  
        #f.writelines(img+' '+str(top_k)+'\n') #将输出结果写入recognition_result.txt文件中

        current_json = {"image_id":img_name, "disease_class":top_k}
        json_result.append(current_json)

    out_result = "/data/chenhongbo/caffe/testB_20181113_03.json"
    with open(out_result, "w") as f:
        f.write(json.dumps(json_result))
'''
        if (alexnet_top_k == resnet50_top_k == googlenet_top_k) :
            top_k = alexnet_top_k
        else :
            if (alexnet_top_k == resnet50_top_k) or (alexnet_top_k == googlenet_top_k):
                top_k = alexnet_top_k
            elif (resnet50_top_k == googlenet_top_k):
                top_k = resnet50_top_k
            else:
                if (alexnet_prob >= resnet50_prob) and ( alexnet_prob >= googlenet_prob):
                    top_k = alexnet_top_k
                elif (resnet50_prob >= alexnet_prob) and ( resnet50_prob >= googlenet_prob):
                    top_k = resnet50_top_k
                else:
                    top_k = googlenet_top_k
'''   

'''
    print 'the class is:',labels[top_k]#将该序号转换成对应的类别名称，并打印
    f=file("/data/workspace/chenhongbo/caffe/1-alexnet_match/recognition_result.txt","a")
    f.writelines(img+' '+labels[top_k]+'\n')#将输出结果写入recognition_result.txt文件中

    if labels[top_k] == img_category:
        list_compute[int(img_category)] += 1
'''

def resize_image(ori_img,dst_img):
    im_ori = cv2.imread(ori_img)
    sp = im_ori.shape
    im_height = sp[0]
    im_width = sp [1]
    #print "height===%d"%(im_height)
    #print "width===%d"%(im_width)
    if (im_height>im_width):
        im_new_height=int(256*im_height/im_width)
        im_new_width=256
    else:
        im_new_width=int(256*im_width/im_height)
        im_new_height=256
    #print "new_height=============%d"%(im_new_height)
    #print "new_width==============%d"%(im_new_width)
    size = (im_new_width,im_new_height)

    im_resize=cv2.resize(im_ori,size,interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(dst_img,im_resize)

#labels_filename=root +'data/ilsvrc12/synset_words.txt'
#循环遍历文件夹root+'examples/images/'下的所有图片
Test()
'''
if len(filelist) != 0:
    print float(correct_num)/len(filelist)
else:
    print 'No data!'
'''
'''
for i in range(0,len(filelist)):
    img=filelist[i]
    Test(img)
'''
'''
f=file("/data/workspace/iim321/caffe/1-alexnet_pest/pest5/label.txt","a")
if list_fact[0] != 0:
    x0_precent = (float(list_compute[0]) / list_fact[0])
    f.writelines('0:'+str(x0_precent)+'\n')
else:
    f.writelines('0:0'+'\n')
if list_fact[1] != 0 :
    x1_precent = (float(list_compute[1]) / list_fact[1])
    f.writelines('1:'+str(x1_precent)+'\n')
else:
    f.writelines('1:0'+'\n')
if list_fact[2] != 0 :
    x2_precent = (float(list_compute[2]) / list_fact[2])
    f.writelines('2:'+str(x2_precent)+'\n')
else:
    f.writelines('2:0'+'\n')
if list_fact[3] != 0 :
    x3_precent = (float(list_compute[3]) / list_fact[3])
    f.writelines('3:'+str(x3_precent)+'\n')
else:
    f.writelines('3:0'+'\n')
if list_fact[4] != 0 :
    x4_precent = (float(list_compute[4]) / list_fact[4])
    f.writelines('4:'+str(x4_precent)+'\n')
else:
    f.writelines('4:0'+'\n')
'''
