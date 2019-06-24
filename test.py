#!/usr/bin/env python 
# -*- coding:utf-8 -*


import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from tensorflow.python.platform import gfile

def read_file(filename):
    result=np.zeros((32,32))
    fr = open(filename)
    for i in range(32):
        linestr = fr.readline()
        for j in range(32):
            result[i,j]=int(linestr[j])
    return result


sess = tf.Session()

test_x_data = read_file('testDigits/6_55.txt')
test_x_data = np.expand_dims(test_x_data,0)
test_x_data = np.expand_dims(test_x_data,3)



with gfile.FastGFile('saved_model/HWModel.pb', 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    sess.graph.as_default()
    tf.import_graph_def(graph_def, name='') # 导入计算图

# 需要有一个初始化的过程
sess.run(tf.global_variables_initializer())




op = sess.graph.get_tensor_by_name('op_to_store:0')

# 输入
input_x = sess.graph.get_tensor_by_name('eval_input:0')

ret = sess.run(op,  feed_dict={input_x: test_x_data})
print(ret)