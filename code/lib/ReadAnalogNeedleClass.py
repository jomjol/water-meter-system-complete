import keras
from tensorflow.keras.models import load_model
import tensorflow as tf 
from PIL import Image
import numpy as np
import glob
import os
import cv2
import configparser
import math
import time
from shutil import copyfile

class ReadAnalogNeedle:
    def __init__(self):
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

        self.model_file = config['Analog_Counter']['Modelfile']

        self.CheckAndLoadDefaultConfig()

        self.model = load_model(self.model_file)

    def CheckAndLoadDefaultConfig(self):
        defaultdir = "./config_default/"
        targetdir = './config/'
        if not os.path.exists(self.model_file):
            zerlegt = self.model_file.split('/')
            pfad = zerlegt[0]
            for i in range(1, len(zerlegt)-1):
                pfad = pfad + '/' + zerlegt[i]
                if not os.path.exists(pfad):
                    os.makedirs(pfad)
            defaultmodel = self.model_file.replace(targetdir, defaultdir)
            copyfile(defaultmodel, self.model_file)
        if len(self.log_Image) > 0:
            if not os.path.exists(self.log_Image):
                zerlegt = self.log_Image.split('/')
                pfad = zerlegt[0]
                for i in range(1, len(zerlegt)):
                    pfad = pfad + '/' + zerlegt[i]
                    if not os.path.exists(pfad):
                        os.makedirs(pfad)

    def Readout(self, PictureList, logtime):
        self.result = []
        for image in PictureList:
            value = self.ReadoutSingleImage(image[1])
            if len(self.log_Image) > 0:
                self.saveLogImage(image, value, logtime)
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

    def saveLogImage(self, image, value, logtime):
        if (len(self.LogNames) > 0) and (not image[0] in self.LogNames):
            return
        speichername = "{:.1f}".format(value) + '_' +  image[0] + '_' + logtime + '.jpg'
        speichername = self.log_Image + '/' + speichername
        cv2.imwrite(speichername, image[1])
