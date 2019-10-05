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

class ReadDigitalDigit:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./config/config.ini')

        self.model_file = config['Digital_Digit']['Modelfile']
        if config.has_option('Digital_Digit', 'LogImageLocation'):
            self.log_Image = config['Digital_Digit']['LogImageLocation']
        self.CheckAndLoadDefaultConfig()

        if config.has_option('Digital_Digit', 'LogImageLocation'):
            if (os.path.exists(self.log_Image)):
                for i in range(10):
                    pfad = self.log_Image + '/' + str(i)
                    if not os.path.exists(pfad):
                        os.makedirs(pfad)
                pfad = self.log_Image + '/NaN'
                if not os.path.exists(pfad):
                    os.makedirs(pfad)

            if config.has_option('Digital_Digit', 'LogNames'):
                zw_LogNames = config.get('Digital_Digit', 'LogNames').split(',')
                self.LogNames = []
                for nm in zw_LogNames:
                      self.LogNames.append(nm.strip())
            else:
                self.LogNames = ''
        else:
            self.log_Image = ''

        self.model_file = config['Digital_Digit']['Modelfile']
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
        test_image = cv2.resize(image,(20,32), interpolation = cv2.INTER_CUBIC)
        cv2.imwrite('./image_tmp/resize.jpg', test_image)
        test_image = np.array(test_image, dtype="float32")
#      test_image/=255.
        img = np.reshape(test_image,[1,32,20,3])
        result = self.model.predict_classes(img)
        if result == 10:
            result = "NaN"
        else:
            result = result[0]
        return result

    def saveLogImage(self, image, value, logtime):
        if (len(self.LogNames) > 0) and (not image[0] in self.LogNames):
            return
        speichername = image[0] + '_' + logtime + '.jpg'
        speichername = self.log_Image + '/' + str(value) + '/' + speichername
        cv2.imwrite(speichername, image[1])
