#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import tensorflow as tf
import numpy as np
import os
from tensorflow.contrib.learn.python.learn.datasets.mnist import read_data_sets
from tensorflow.python.framework import graph_util
import tfcoreml as tf_converter



def read_file(filename):
    result=np.zeros((32,32))
    fr = open(filename)
    for i in range(32):
        linestr = fr.readline()
        for j in range(32):
            result[i,j]=int(linestr[j])
    return result

def get_training_data():
    datalist = os.listdir('trainingDigits')
    m=len(datalist)
    train_matrix=np.zeros((m,32,32))
    result_array=[]
    for i in range(m):
        fileName=datalist[i]
        ans=int(fileName.split('_')[0])
        result_array.append(ans)
        train_matrix[i:]=read_file('trainingDigits/%s' %fileName)
        #result_array.append(read_file('trainingDigits/%s' %fileName))
    #train_xdata = np.array([np.reshape(x,(32,32)) for x in result_array])
    return np.array(result_array),train_matrix


train_labels,train_xdata = get_training_data()

sess = tf.Session()

batch_size = 100
learning_rate = 0.005
evaluation_size = 1
image_width = train_xdata[0].shape[0]
image_height = train_xdata[0].shape[1]
#print('width = '+ str(image_width))
target_size = max(train_labels)+1
#print('size = '+ str(target_size))
num_channels = 1
generations = 500
conv1_features = 25
conv2_features = 50
max_pool_size1 = 4
max_pool_size2 = 4
fully_connected_size = 100


x_input_shape = (batch_size,image_width,image_height,num_channels)
x_input = tf.placeholder(tf.float64,shape=x_input_shape)
y_target = tf.placeholder(tf.int32,shape=(batch_size))

eval_input_shape = (evaluation_size,image_width,image_height,num_channels)
eval_input = tf.placeholder(tf.float64,shape=eval_input_shape,name='eval_input')
eval_target = tf.placeholder(tf.int32,shape=(evaluation_size))

conv1_weight = tf.Variable(tf.truncated_normal([4,4,num_channels,conv1_features],stddev=0.1,dtype=tf.float64))
conv1_bias = tf.Variable(tf.zeros([conv1_features],dtype=tf.float64))


conv2_weight = tf.Variable(tf.truncated_normal([4,4,conv1_features,conv2_features],stddev=0.1,dtype=tf.float64))
conv2_bias = tf.Variable(tf.zeros([conv2_features],dtype=tf.float64))


resulting_width = image_width//(max_pool_size1*max_pool_size2)
resulting_height = image_height//(max_pool_size1*max_pool_size2)

full1_input_size = resulting_height*resulting_width*conv2_features
full1_weight = tf.Variable(tf.truncated_normal([full1_input_size,fully_connected_size],stddev=0.1,dtype=tf.float64))
full1_bias = tf.Variable(tf.truncated_normal([fully_connected_size],stddev=0.1,dtype=tf.float64))

full2_weight = tf.Variable(tf.truncated_normal([fully_connected_size,target_size],stddev=0.1,dtype=tf.float64))
full2_bias = tf.Variable(tf.truncated_normal([target_size],stddev=0.1,dtype=tf.float64))




def my_conv_net(input_data):
    conv1 = tf.nn.conv2d(input_data,conv1_weight,strides=[1,1,1,1],padding='SAME')
    relu1 = tf.nn.relu(tf.nn.bias_add(conv1,conv1_bias))
    max_pool1 = tf.nn.max_pool(relu1,ksize=[1,max_pool_size1,max_pool_size1,1],strides=[1,max_pool_size1,max_pool_size1,1],padding='SAME')

    conv2 = tf.nn.conv2d(max_pool1,conv2_weight,strides=[1,1,1,1],padding='SAME')
    relu2 = tf.nn.relu(tf.nn.bias_add(conv2,conv2_bias))
    max_pool2 = tf.nn.max_pool(relu2,ksize=[1,max_pool_size2,max_pool_size2,1],strides=[1,max_pool_size2,max_pool_size2,1],padding='SAME')


    final_conv_shape = max_pool2.get_shape().as_list()
    final_shape = final_conv_shape[1]*final_conv_shape[2]*final_conv_shape[3]
    flat_output = tf.reshape(max_pool2,[final_conv_shape[0],final_shape])

    fully_connected1 = tf.nn.relu(tf.add(tf.matmul(flat_output,full1_weight),full1_bias))
    final_model_output = tf.add(tf.matmul(fully_connected1,full2_weight),full2_bias)

    return (final_model_output)



def conv_test(input_data):
    conv1 = tf.nn.conv2d(input_data,conv1_weight,strides=[1,1,1,1],padding='SAME')
    relu1 = tf.nn.relu(tf.nn.bias_add(conv1,conv1_bias))
    max_pool1 = tf.nn.max_pool(relu1,ksize=[1,max_pool_size1,max_pool_size1,1],strides=[1,1,1,1],padding='SAME')

    conv2 = tf.nn.conv2d(max_pool1,conv2_weight,strides=[1,1,1,1],padding='SAME')
    relu2 = tf.nn.relu(tf.nn.bias_add(conv2,conv2_bias))
    max_pool2 = tf.nn.max_pool(relu2,ksize=[1,max_pool_size2,max_pool_size2,1],strides=[1,1,1,1],padding='SAME')
    return max_pool2





model_output = my_conv_net(x_input)
loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y_target,logits=model_output))
opt = tf.train.MomentumOptimizer(learning_rate,0.9)
train_step = opt.minimize(loss)






result2 = tf.reshape(tf.argmax(my_conv_net(eval_input),axis=1),shape=[],name='op_to_store')

init = tf.global_variables_initializer()
sess.run(init)



for i in range(generations):
    rand_index = np.random.choice(len(train_xdata),size=batch_size)
    rand_x = train_xdata[rand_index]
    rand_x = np.expand_dims(rand_x,3)
    rand_y = train_labels[rand_index]
    train_dict = {x_input: rand_x, y_target: rand_y}
    sess.run(train_step,feed_dict=train_dict)

test_x_data = read_file('testDigits/5_9.txt')
test_x_data = np.expand_dims(test_x_data,0)
test_x_data = np.expand_dims(test_x_data,3)




#result = sess.run(my_conv_net(test_x_data))
#print(result)
#print(np.argmax(result,axis=1))


#saver=tf.train.Saver()  # 不传入参数代表默认存入全部参数
#file_name = 'saved_model/model.ckpt'  # 将保存到当前目录下的的saved_model文件夹下model.ckpt文件
#saver.save(sess,file_name )  # 保存好的模型文件







constant_graph=graph_util.convert_variables_to_constants(sess,sess.graph_def,['op_to_store'])



print(sess.run(result2,feed_dict={eval_input:test_x_data}))




saver=tf.train.Saver()  # 不传入参数代表默认存入全部参数
file_name = 'saved_model/model.ckpt'  # 将保存到当前目录下的的saved_model文件夹下model.ckpt文件
saver.save(sess,file_name )  # 保存好的模型文件



#生成pb模型
with tf.gfile.FastGFile('saved_model/HWModel.pb', mode='wb') as f:
    f.write(constant_graph.SerializeToString())




#将pb模型转换成mlmodel，可应用于ios的CoreML
tf_converter.convert(tf_model_path='saved_model/HWModel.pb',
                     mlmodel_path='saved_model/HWModel.mlmodel',
                     output_feature_names=['op_to_store:0'],input_name_shape_dict={"eval_input:0":[1,32,32,1]})







