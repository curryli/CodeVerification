# -*- coding:utf-8 -*-
from gen_captcha import gen_captcha_text_and_image  
from gen_captcha import number  
from gen_captcha import alphabet  
from gen_captcha import ALPHABET  
   
import numpy as np  
import tensorflow as tf  
   
text, image = gen_captcha_text_and_image()  
print("验证码图像channel:", image.shape)  # (60, 160, 3)  
# 图像大小  
IMAGE_HEIGHT = 60  
IMAGE_WIDTH = 160  
MAX_CAPTCHA = len(text)  
print("验证码文本最长字符数", MAX_CAPTCHA)   # 验证码最长4字符; 我全部固定为4,可以不固定. 如果验证码长度小于4，用'_'补齐  
   
# 把彩色图像转为灰度图像（色彩对识别验证码没有什么用）  
def convert2gray(img):  
    if len(img.shape) > 2:  
        gray = np.mean(img, -1)  
        # 上面的转法较快，正规转法如下  
        # r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]  
        # gray = 0.2989 * r + 0.5870 * g + 0.1140 * b  
        return gray  
    else:  
        return img  
 
   
# 文本转向量  
char_set = number + alphabet + ALPHABET + ['_']  # 如果验证码长度小于4, '_'用来补齐  
CHAR_SET_LEN = len(char_set)  
 
X = tf.placeholder(tf.float32, [None, IMAGE_HEIGHT*IMAGE_WIDTH])  
Y = tf.placeholder(tf.float32, [None, MAX_CAPTCHA*CHAR_SET_LEN])  
keep_prob = tf.placeholder(tf.float32) # dropout  
   
# 定义CNN  
def crack_captcha_cnn(w_alpha=0.01, b_alpha=0.1):  
    x = tf.reshape(X, shape=[-1, IMAGE_HEIGHT, IMAGE_WIDTH, 1])  
    
    w_c1 = tf.Variable(w_alpha*tf.random_normal([3, 3, 1, 32]))  
    b_c1 = tf.Variable(b_alpha*tf.random_normal([32]))  
    conv1 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(x, w_c1, strides=[1, 1, 1, 1], padding='SAME'), b_c1))  
    conv1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')  
    conv1 = tf.nn.dropout(conv1, keep_prob)  
   
    w_c2 = tf.Variable(w_alpha*tf.random_normal([3, 3, 32, 64]))  
    b_c2 = tf.Variable(b_alpha*tf.random_normal([64]))  
    conv2 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv1, w_c2, strides=[1, 1, 1, 1], padding='SAME'), b_c2))  
    conv2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')  
    conv2 = tf.nn.dropout(conv2, keep_prob)  
   
    w_c3 = tf.Variable(w_alpha*tf.random_normal([3, 3, 64, 64]))  
    b_c3 = tf.Variable(b_alpha*tf.random_normal([64]))  
    conv3 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv2, w_c3, strides=[1, 1, 1, 1], padding='SAME'), b_c3))  
    conv3 = tf.nn.max_pool(conv3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')  
    conv3 = tf.nn.dropout(conv3, keep_prob)  
   
    # Fully connected layer  
    w_d = tf.Variable(w_alpha*tf.random_normal([8*32*40, 1024]))  
    b_d = tf.Variable(b_alpha*tf.random_normal([1024]))  
    dense = tf.reshape(conv3, [-1, w_d.get_shape().as_list()[0]])  
    dense = tf.nn.relu(tf.add(tf.matmul(dense, w_d), b_d))  
    dense = tf.nn.dropout(dense, keep_prob)  
   
    w_out = tf.Variable(w_alpha*tf.random_normal([1024, MAX_CAPTCHA*CHAR_SET_LEN]))  
    b_out = tf.Variable(b_alpha*tf.random_normal([MAX_CAPTCHA*CHAR_SET_LEN]))  
    out = tf.add(tf.matmul(dense, w_out), b_out)  
    #out = tf.nn.softmax(out)  
    return out  


def crack_captcha(captcha_image):  
    output = crack_captcha_cnn()  
   
    saver = tf.train.Saver()  
    with tf.Session() as sess:  
        #训练好以后多出3个文件    checkpoint   crack_capcha.model-3200.meta crack_capcha.model-3200  随便用哪个
        #saver.restore(sess, tf.train.latest_checkpoint('.'))  
        saver.restore(sess, 'crack_capcha.model-3200')
        predict = tf.argmax(tf.reshape(output, [-1, MAX_CAPTCHA, CHAR_SET_LEN]), 2)  
        text_list = sess.run(predict, feed_dict={X: [captcha_image], keep_prob: 1})  
        text = text_list[0].tolist()  
        return text   

if __name__ == "__main__":

   
   text, image = gen_captcha_text_and_image()  
   image = convert2gray(image)  
   image = image.flatten() / 255  
   predict_text = crack_captcha(image)  
   print("real: {}  predict: {}".format(text, predict_text))  