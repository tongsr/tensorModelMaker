import  matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf


batch_size = 100
learning_rate = 0.005
evaluation_size = 500

target_size = 10
num_channels = 1
generations = 500
conv1_features = 25
conv2_features = 50
max_pool_size1 = 4
max_pool_size2 = 4
fully_connected_size = 100

image_width = 32
image_height = 32
resulting_width = image_width//(max_pool_size1*max_pool_size2)
resulting_height = image_height//(max_pool_size1*max_pool_size2)





conv1_weight = tf.Variable(tf.truncated_normal([4,4,num_channels,conv1_features],stddev=0.1,dtype=tf.float64))
conv1_bias = tf.Variable(tf.zeros([conv1_features],dtype=tf.float64))


conv2_weight = tf.Variable(tf.truncated_normal([4,4,conv1_features,conv2_features],stddev=0.1,dtype=tf.float64))
conv2_bias = tf.Variable(tf.zeros([conv2_features],dtype=tf.float64))




full1_input_size = resulting_height*resulting_width*conv2_features
full1_weight = tf.Variable(tf.truncated_normal([full1_input_size,fully_connected_size],stddev=0.1,dtype=tf.float64))
full1_bias = tf.Variable(tf.truncated_normal([fully_connected_size],stddev=0.1,dtype=tf.float64))

full2_weight = tf.Variable(tf.truncated_normal([fully_connected_size,target_size],stddev=0.1,dtype=tf.float64))
full2_bias = tf.Variable(tf.truncated_normal([target_size],stddev=0.1,dtype=tf.float64))


def read_file(filename):
    result=np.zeros((32,32))
    fr = open(filename)
    for i in range(32):
        linestr = fr.readline()
        for j in range(32):
            result[i,j]=int(linestr[j])
    return result

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





sess = tf.Session()


#唤醒训练结果
new_saver = tf.train.Saver()
new_saver.restore(sess,'saved_model/model.ckpt')



test_x_data = read_file('testDigits/7_9.txt')
test_x_data = np.expand_dims(test_x_data,0)
test_x_data = np.expand_dims(test_x_data,3)

result = sess.run(my_conv_net(test_x_data))
print(result)
print(np.argmax(result,axis=1))