from tensorflow.keras.models import load_model
import tensorflow.keras.backend as K
import tensorflow as tf 
from PIL import Image
import numpy as np
import glob
import os
import math
import time
from shutil import copyfile

class ReadAnalogNeedle:
    def __init__(self, readconfig, zwpath='./image_tmp/'):
        self.PathImageZw = zwpath
        self.UpdateConfig(readconfig)

    def UpdateConfig(self, readconfig):
        self.log_Image = ''
        self.LogNames = ''

        self.model_file = readconfig.AnalogModelFile()
        (self.doLog, self.LogNames, self.log_Image) = readconfig.AnalogGetLogInfo()

        self.MakeLogFileDirectories()

        self.model = load_model(self.model_file)

    def MakeLogFileDirectories(self):
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
        test_image = image.resize((32, 32), Image.NEAREST)
        test_image.save(self.PathImageZw + 'resize.jpg', "JPEG")
        test_image = np.array(test_image, dtype="float32")
        img = np.reshape(test_image,[1,32,32,3])
        classes = self.model.predict(img)
        out_sin = classes[0][0]
        out_cos = classes[0][1]
        K.clear_session()
        result =  np.arctan2(out_sin, out_cos)/(2*math.pi) % 1
        result = result * 10
        return result

    def saveLogImage(self, image, value, logtime):
        if (len(self.LogNames) > 0) and (not image[0] in self.LogNames):
            return
        speichername = "{:.1f}".format(value) + '_' +  image[0] + '_' + logtime + '.jpg'
        speichername = self.log_Image + '/' + speichername
        image[1].save(speichername, "JPEG")
