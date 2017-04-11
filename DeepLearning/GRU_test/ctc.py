from captcha.image import ImageCaptcha
import matplotlib.pyplot as plt
import numpy as np
import random
import os
import cv2
import string
characters = string.digits + string.ascii_uppercase
print(characters)

width, height, n_len, n_class = 170, 80, 4, 63

from keras import backend as K

def ctc_lambda_func(args):
    y_pred, labels, input_length, label_length = args
    y_pred = y_pred[:, 2:, :]
    return K.ctc_batch_cost(labels, y_pred, input_length, label_length)


def __data_label__(path, count):
    MapDict = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "a": 10, "b": 11,
               "c": 12, "d": 13, "e": 14, "f": 15, "g": 16, "h": 17,
               "i": 18, "j": 19, "k": 20, "l": 21, "m": 22, "n": 23, "o": 24, "p": 25, "q": 26, "r": 27, "s": 28,
               "t": 29, "u": 30, "v": 31, "w": 32, "x": 33, "y": 34, "z": 35,
               "A": 36, "B": 37, "C": 38, "D": 39, "E": 40, "F": 41, "G": 42, "H": 43, "I": 44, "J": 45, "K": 46,
               "L": 47, "M": 48, "N": 49, "O": 50, "P": 51,
               "Q": 52, "R": 53, "S": 54, "T": 55, "U": 56, "V": 57, "W": 58, "X": 59, "Y": 60, "Z": 61}

    data = np.empty((count, 1, 80, 170), dtype="float32")
    # label = np.empty((count,),dtype="uint8")
    # label=[]
    label = np.empty((count, 4), "uint8")
    i = 0;

    filelist = os.listdir(path)
    # print filelist
    for ff in filelist:
        # print path,ff

        img = cv2.imread(path + ff, 0)
        # print 'ccccccccccccccccccccccccccc',type(img)
        img = cv2.resize(img, (170, 80), interpolation=cv2.INTER_CUBIC)
        # img = cv2.resize(img,(0, 0), fx=0.85, fy=1.6, interpolation=cv2.INTER_CUBIC)
        arr = np.asarray(img, dtype="float32")
        # arr = np.transpose(arr,(2, 1, 0))
        data[i, :, :, :] = arr

        # fy = ff
        labelStr = ff.split("_")[0]
        tmplabel = []
        for s in labelStr:
            # print MapDict[s],"\n"
            tmplabel.append(MapDict[s])
        label[i] = tmplabel
        i += 1

    # print "i is: "+ str(i)
    data /= np.max(data)
    data -= np.mean(data)
    return data, label

trainpath = r'/home/xrli/PicsForLen/TrainImgs/4/'
testpath = r'/home/xrli/PicsForLen/TrainImgs/4/'
testcount= 40000  #__getnum__(testpath)
traincount= 40000   #__getnum__(trainpath)
#testdata,testlabel= __data_label__(testpath, testcount)
#print testdata.shape, testlabel
#print testlabel
traindata,trainlabel= __data_label__(trainpath, traincount)
traindata = traindata.transpose((0,3,2,1))
print 'aaaaaaaaaaaaabbbbbbbbbbbbbbb',np.max(trainlabel)
from keras.models import *
from keras.layers import *
rnn_size = 128

input_tensor = Input((width, height, 1))
x = input_tensor
for i in range(3):
    x = Convolution2D(32, 3, 3, activation='relu')(x)
    x = Convolution2D(32, 3, 3, activation='relu')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)

conv_shape = x.get_shape()
x = Reshape(target_shape=(int(conv_shape[1]), int(conv_shape[2]*conv_shape[3])))(x)

x = Dense(32, activation='relu')(x)

gru_1 = GRU(rnn_size, return_sequences=True, init='he_normal', name='gru1')(x)
gru_1b = GRU(rnn_size, return_sequences=True, go_backwards=True, init='he_normal', name='gru1_b')(x)
gru1_merged = merge([gru_1, gru_1b], mode='sum')

gru_2 = GRU(rnn_size, return_sequences=True, init='he_normal', name='gru2')(gru1_merged)
gru_2b = GRU(rnn_size, return_sequences=True, go_backwards=True, init='he_normal', name='gru2_b')(gru1_merged)
x = merge([gru_2, gru_2b], mode='concat')
x = Dropout(0.25)(x)
x = Dense(n_class, init='he_normal', activation='softmax')(x)
base_model = Model(input=input_tensor, output=x)

labels = Input(name='the_labels', shape=[n_len], dtype='float32')
input_length = Input(name='input_length', shape=[1], dtype='int64')
label_length = Input(name='label_length', shape=[1], dtype='int64')
loss_out = Lambda(ctc_lambda_func, output_shape=(1,), name='ctc')([x, labels, input_length, label_length])

model = Model(input=[input_tensor, labels, input_length, label_length], output=[loss_out])
model.compile(loss={'ctc': lambda y_true, y_pred: y_pred}, optimizer='adadelta')

#model.load_weights('captcha_break-master/model.h5')

def gen(batch_size=128):
    X = np.zeros((batch_size, width, height, 1), dtype=np.uint8)
    y = np.zeros((batch_size, n_len), dtype=np.uint8)
    ii=0
    while True:
        generator = ImageCaptcha(width=width, height=height)
        for i in range(batch_size):
            random_str = ''.join([random.choice(characters) for j in range(4)])
            X[i] = traindata[ii,:,:,:]

            #plt.imshow(X[i].transpose(1, 0, 2))
            y[i] = trainlabel[ii,:]
            ii+=1
	    ii%=40000
            a = np.ones(batch_size)*int(conv_shape[1]-2)
            b = np.ones(batch_size)*n_len
        yield [X, y, np.ones(batch_size)*int(conv_shape[1]-2), np.ones(batch_size)*n_len], np.ones(batch_size)

[X_test, y_test, a, b],c  = next(gen(1))
#plt.imshow(X_test[0].transpose(1, 0, 2))
#plt.title(''.join([characters[x] for x in y_test[0]]))

def evaluate(model, batch_num=10):
    batch_acc = 0
    generator = gen(128)
    for i in range(batch_num):
        [X_test, y_test, _, _], _  = next(generator)
        y_pred = base_model.predict(X_test)
        shape = y_pred[:,2:,:].shape
        out = K.get_value(K.ctc_decode(y_pred[:,2:,:], input_length=np.ones(shape[0])*shape[1])[0][0])[:, :4]
        if out.shape[1] == 4:
            batch_acc += ((y_test == out).sum(axis=1) == 4).mean()
    return batch_acc / batch_num

from keras.callbacks import *

class Evaluate(Callback):
    def __init__(self):
        self.accs = []
    
    def on_epoch_end(self, epoch, logs=None):
        acc = evaluate(base_model)*100
        self.accs.append(acc)
        print
        print('acc: %f%%'%acc)

evaluator = Evaluate()

model.fit_generator(gen(128), samples_per_epoch=40000, nb_epoch=200,
                    callbacks=[EarlyStopping(patience=10), evaluator],
                    validation_data=gen(), nb_val_samples=1280)

#model.fit_generator(gen(128), samples_per_epoch=51200, nb_epoch=200,
#                    callbacks=[EarlyStopping(patience=10), evaluator],
#                    validation_data=gen(), nb_val_samples=1280)

characters2 = characters + ' '
[X_test, y_test, _, _], _  = next(gen(1))
y_pred = base_model.predict(X_test)
y_pred = y_pred[:,2:,:]
out = K.get_value(K.ctc_decode(y_pred, input_length=np.ones(y_pred.shape[0])*y_pred.shape[1], )[0][0])[:, :4]
out = ''.join([characters[x] for x in out[0]])
y_true = ''.join([characters[x] for x in y_test[0]])

plt.imshow(X_test[0].transpose(1, 0, 2))
plt.title('pred:' + str(out) + '\ntrue: ' + str(y_true))

argmax = np.argmax(y_pred, axis=2)[0]
list(zip(argmax, ''.join([characters2[x] for x in argmax])))

evaluate(base_model)

model.save('model.h5')
