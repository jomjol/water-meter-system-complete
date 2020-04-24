import tflite_runtime.interpreter as tflite

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
from datetime import datetime

debug = True

class UseClassificationCNN:
    def __init__(self, in_Modelfile, in_dx, in_dy, in_numberclasses, in_LogImageLocation, in_LogNames):
        self.log_Image = in_LogImageLocation
        self.LogNames = ''
        self.dx = in_dx
        self.dy = in_dy

        self.model_file = in_Modelfile

        self.CheckAndLoadDefaultConfig()

        if in_LogImageLocation:
            if (os.path.exists(self.log_Image)):
                for i in range(in_numberclasses):
                    pfad = self.log_Image + '/' + str(i)
                    if not os.path.exists(pfad):
                        os.makedirs(pfad)

            if in_LogNames:
                zw_LogNames = in_LogNames.split(',')
                self.LogNames = []
                for nm in zw_LogNames:
                      self.LogNames.append(nm.strip())
            else:
                self.LogNames = ''
        else:
            self.log_Image = ''

        filename, file_extension = os.path.splitext(self.model_file)
        if file_extension != ".tflite":
            print("ERROR - only TFLite-Model (*.tflite) are support since version 7.0.0 and higher")
            quit()

        self.interpreter = tflite.Interpreter(model_path=self.model_file)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()


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
        if debug: 
            print(self.gettimestring() + " Validity 01")
        test_image = image.resize((self.dx,  self.dy), Image.NEAREST)
        if debug: 
            print(self.gettimestring() + " Validity 02")
        test_image.save('./image_tmp/resize.jpg', "JPEG")
        if debug: 
            print(self.gettimestring() + " Validity 03")
        test_image = np.array(test_image, dtype="float32")
        if debug: 
            print(self.gettimestring() + " Validity 04")
        img = np.reshape(test_image,[1, self.dy, self.dx,3])
        if debug: 
            print(self.gettimestring() + " Validity 05")


        input_data = img
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        result = np.argmax(output_data)


        if debug: 
            print(self.gettimestring() + " Validity 06")
        if debug: 
            print(self.gettimestring() + " Validity 07")

        return result

    def saveLogImage(self, image, value, logtime):
        if (len(self.LogNames) > 0) and (not image[0] in self.LogNames):
            return
        speichername = image[0] + '_' + logtime + '.jpg'
        speichername = self.log_Image + '/' + str(value) + '/' + speichername
        image[1].save(speichername, "JPEG")

    def gettimestring(self):
        curr_time = datetime.now()
        formatted_time = curr_time.strftime('%Y-%m-%d %H:%M:%S.%f')
        return formatted_time

