# status initialize

import os
os.environ['CUDA_VISIBLE_DEVICES'] = '1'

# out of memory
import tensorflow as tf
with tf.Graph().as_default():
  gpu_options = tf.compat.v1.GPUOptions(allow_growth=True)