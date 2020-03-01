from tensorflow.keras.models import load_model
import tensorflow.keras.backend as K
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
from PIL import Image 

class ReadDigitalDigit:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./config/config.ini')

        self.log_Image = ''
        self.LogNames = ''

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
    
    def binarize_array(self, numpy_array, threshold=127):
        for i in range(len(numpy_array)):
            for j in range(len(numpy_array[0])):
                if numpy_array[i][j] > threshold:
                    numpy_array[i][j] = 255
                else:
                    numpy_array[i][j] = 0
        return numpy_array

    
    
    def ReadoutSingleImage(self, image):
        img = image
        test_image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        shape = test_image.shape
        maxs = shape[0] * shape[1]
        maxh = shape[0]
        maxw = shape[1]
        imgray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
        imgray = cv2.bilateralFilter(imgray, 11, 17, 17)
        edged = cv2.Canny(imgray, 250, 255)
        contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # print(contours)
        contours_poly = [None] * len(contours)
        boundRect = [None] * len(contours)
        maxpos = -1
        maxval = 0
        x, y, w, h = 0, 0, 0, 0
        for i, c in enumerate(contours):
            contours_poly[i] = cv2.approxPolyDP(c, 2, True)
            boundRect[i] = cv2.boundingRect(contours_poly[i])
            size = (boundRect[i][2] * boundRect[i][3])
            if size > maxval:
                maxpos = i
                maxval = size
                x, y, w, h = boundRect[i]
        x = x - 3
        if x < 0:
            x = 0
        else:
            w = w + 6
            if w + x > maxw:
                w = maxw - x
        y = y - 3
        if y < 0:
            x = 0
        else:
            h = h + 6
            if y + h > maxh:
                h = maxh - y
        xr = x + w
        yu = y + h

        img = np.asarray(test_image[y:yu, x:xr])
        img = Image.fromarray(img)
        img = img.convert("L")
        img = img.filter(ImageFilter.GaussianBlur(radius=1))
        img = np.array(img)
        img = self.binarize_array(img)
        img = Image.fromarray(img)
        # img.show()
        img = img.convert("RGB")
        #        test_image = image.resize((20, 32), Image.NEAREST)
        test_image = img.resize((20, 32), Image.NEAREST)
        
        test_image.save('./image_tmp/resize.jpg', "JPEG")
        test_image = np.array(test_image, dtype="float32")
        img = np.reshape(test_image,[1,32,20,3])
        result = self.model.predict_classes(img)
        K.clear_session()
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
        image[1].save(speichername, "JPEG")

