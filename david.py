import tensorflow as tf
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from simulator import Command

import PIL
from PIL import Image

class David:
	def create_new_conv_layer(self, input_data, num_input_channels, num_filters, filter_shape, pool_shape, name):
		# setup the filter input shape for tf.nn.conv_2d
		conv_filt_shape = [filter_shape[0], filter_shape[1], num_input_channels, num_filters]

		# initialise weights and bias for the filter
		weights = tf.Variable(tf.truncated_normal(conv_filt_shape, stddev=0.03),name=name+'_W')
		bias = tf.Variable(tf.truncated_normal([num_filters]), name=name+'_b')

		# setup the convolutional layer operation
		out_layer = tf.nn.conv2d(input_data, weights, [1, 1, 1, 1], padding='SAME')

		# add the bias
		out_layer += bias

		# apply a ReLU non-linear activation
		out_layer = tf.nn.relu(out_layer)

		# now perform max pooling
		ksize = [1, pool_shape[0], pool_shape[1], 1]
		strides = [1, 2, 2, 1]
		out_layer = tf.nn.max_pool(out_layer, ksize=ksize, strides=strides, padding='SAME')

		return out_layer

	def __init__(self):
		w=64
		h=64

		self.x = tf.placeholder(tf.float32, [None, w, h, 3])
		x_shaped = tf.reshape(self.x, [-1, w, h, 3])
		"""self.y = tf.placeholder(tf.float32, [None, 10])"""

		layer1=self.create_new_conv_layer(x_shaped,3,16,[20,20], [2,2],name='layer1')
		layer2=self.create_new_conv_layer(layer1,16,64,[20,20], [2,2],name='layer2')

		"""flattened = tf.reshape(layer2, [-1,7*7*64])"""
		flattened = tf.reshape(layer2, [-1,w*h*4])


		wd1 = tf.Variable(tf.truncated_normal([w*h*4, 100], stddev=0.03), name='wd1')
		bd1 = tf.Variable(tf.truncated_normal([100], stddev=0.01), name='bd1')
		dense_layer1 = tf.matmul(flattened, wd1) + bd1
		dense_layer1 = tf.nn.relu(dense_layer1)

		wd2 = tf.Variable(tf.truncated_normal([100, 4], stddev=0.03), name='wd2')
		bd2 = tf.Variable(tf.truncated_normal([4], stddev=0.01), name='bd2')
		dense_layer2 = tf.matmul(dense_layer1, wd2) + bd2
		self.y_ = tf.nn.softmax(dense_layer2)

		self.sess = tf.Session()

	def reset(self):
		init = tf.global_variables_initializer()
		self.sess.run(init)	

	def save(self):
		return self.sess

	def drive(self, image):
		##Lav funktion der omskriver image til format der passer til netværket
		##Input det i netværket
		##Kig herefter på at lave en genetic udvælgelse af netværker
		
		image=image.resize((64,64), PIL.Image.ANTIALIAS)
		img_array=np.array(image)



		

		img_array=img_array[None, :,:,:3]
		

		init = tf.global_variables_initializer()

		self.sess.run(init)


		result=self.sess.run(self.y_,feed_dict={self.x: img_array})
		
		ret=Command()
		r=np.zeros(5)
		r[np.argmax(result)]=1
		
		ret.update(r[0],r[1],r[2],r[3])

		return ret
