import keras
#from keras.models import load_model
from tensorflow.keras.models import load_model
#from tensorflow.python import keras
#from tensorflow.python.keras import Sequential
#from tensorflow.python.keras.layers import Dense, InputLayer, Conv2D, MaxPool2D, Flatten, BatchNormalization
#from keras.models import model_from_json, model_from_yaml
import tensorflow as tf 
from PIL import Image
import numpy as np
import glob
import os
import cv2
import configparser
import math
import time

class ReadAnalogNeedle:
    def __init__(self):
#       model = tf.keras.models.load_model('./config/neuralnets/Train_CNN_Version2_Analog-Readout.h5')
        config = configparser.ConfigParser()
        config.read('./config/config.ini')

        if config.has_option('Analog_Counter', 'LogImageLocation'):
            self.log_Image = config['Analog_Counter']['LogImageLocation']
            if config.has_option('Analog_Counter', 'LogNames'):
                zw_LogNames = config.get('Analog_Counter', 'LogNames').split(',')
                self.LogNames = []
                for nm in zw_LogNames:
                      self.LogNames.append(nm.strip())
            else:
                self.LogNames = ''
        else:
            self.log_Image = ''

        model_file = config['Analog_Counter']['Modelfile']
        self.model = load_model(model_file)

    def Readout(self, PictureList):
        self.result = []
        for image in PictureList:
            value = self.ReadoutSingleImage(image[1])
            if len(self.log_Image) > 0:
                self.saveLogImage(image, value)
            self.result.append(value)
        return self.result

    def ReadoutSingleImage(self, image):
        test_image = cv2.resize(image,(32,32), interpolation = cv2.INTER_CUBIC)
        cv2.imwrite('./image_tmp/resize.jpg', test_image)
        test_image = np.array(test_image, dtype="float32")
#      test_image/=255.
        img = np.reshape(test_image,[1,32,32,3])
        classes = self.model.predict(img)
        out_sin = classes[0][0]
        out_cos = classes[0][1]
        result =  np.arctan2(out_sin, out_cos)/(2*math.pi) % 1
        result = result * 10
        return result

    def saveLogImage(self, image, value):
        if (len(self.LogNames) > 0) and (not image[0] in self.LogNames):
            return
        zeit = time.time()
        speichername = "{:.1f}".format(value) + '_' +  image[0] + '_' + str(int(zeit)) + '.jpg'
        speichername = self.log_Image + '/' + speichername
        cv2.imwrite(speichername, image[1])
