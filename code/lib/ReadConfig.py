import numpy as np
import cv2
import configparser
import os
from shutil import copyfile
import shutil
from PIL import Image

class ReadConfig:
    def __init__(self, _path, _pathdefault="./config_default/", _configreroute = './config/', copydummyconfig = True):
        self.PathToConfig = _path
        self.ConfigExist = False
        if copydummyconfig:
            self.CheckAndLoadDefaultConfig(_pathdefault)
        self.ParseConfig()
        self.ConfigOriginalPath = './config/'
        self.ConfigReroutePath = _configreroute


    def ParseConfig(self):
        pfadini = str(self.PathToConfig.joinpath('config.ini'))
        self.ConfigExist = os.path.exists(pfadini)

        if not self.ConfigExist:
            return

        config = configparser.ConfigParser()
        config.read(pfadini)

        ##################  DigitalReadOut Parameters ########################
        self.Digit_LogNames = ''
        self.Digit_log_Image = ''
        self.Digit_LogNames_Enabled = False
        self.Digit_LogNamesFull = ''

        self.Digit_model_file = config['Digital_Digit']['Modelfile']

        self.Digit_DoLog = config.has_option('Digital_Digit', 'LogImageLocation')
        if self.Digit_DoLog:
            self.Digit_log_Image = config['Digital_Digit']['LogImageLocation']
            self.Digit_LogNames = ''
            self.Digit_LogNames_Enabled = config.has_option('Digital_Digit', 'LogNames')
            if self.Digit_LogNames_Enabled:
                self.Digit_LogNamesFull = config.get('Digital_Digit', 'LogNames').split(',')
                self.Digit_LogNames = []
                for nm in self.Digit_LogNamesFull:
                      self.Digit_LogNames.append(nm.strip())

        ##################  AnalogReadOut Parameters ########################
        self.Analog_log_Image = ''
        self.Analog_LogNames = ''
        self.Analog_LogName_Enabled = False
        self.Analog_LogNamesFull = ''

        self.Analog_model_file = config['Analog_Counter']['Modelfile']

        self.Analog_DoLog = config.has_option('Analog_Counter', 'LogImageLocation')
        if self.Analog_DoLog:
            self.Analog_log_Image = config['Analog_Counter']['LogImageLocation']
            self.Analog_LogNames = ''
            self.Analog_LogName_Enabled = config.has_option('Analog_Counter', 'LogNames')
            if self.Analog_LogName_Enabled:
                self.Analog_LogNamesFull = config.get('Analog_Counter', 'LogNames').split(',')
                self.Analog_LogNames = []
                for nm in self.Analog_LogNamesFull:
                      self.Analog_LogNames.append(nm.strip())

        ##################  ZaehlerstandClass Parameters ########################
        self.Zaehler_AnalogReadOutEnabled = True
        if config.has_option('AnalogReadOut', 'Enabled'):
            self.Zaehler_AnalogReadOutEnabled = config['AnalogReadOut']['Enabled']
            if self.Zaehler_AnalogReadOutEnabled.upper() == 'FALSE':
                self.Zaehler_AnalogReadOutEnabled = False

        self.Zaehler_ConsistencyEnabled = False        
        if config.has_option('ConsistencyCheck', 'Enabled'):
            self.Zaehler_ConsistencyEnabled = config['ConsistencyCheck']['Enabled']
            if self.Zaehler_ConsistencyEnabled.upper() == 'TRUE':
                self.Zaehler_ConsistencyEnabled = True

        self.Zaehler_AllowNegativeRates = True
        if config.has_option('ConsistencyCheck', 'AllowNegativeRates'):
            self.Zaehler_AllowNegativeRates = config['ConsistencyCheck']['AllowNegativeRates']
            if self.Zaehler_AllowNegativeRates.upper() == 'FALSE':
                self.Zaehler_AllowNegativeRates = False

        self.Zaehler_MaxRateValue = None
        self.Zaehler_ErrorReturn = ''
        if config.has_option('ConsistencyCheck', 'MaxRateValue'):
            self.Zaehler_MaxRateValue = float(config['ConsistencyCheck']['MaxRateValue'])
        if config.has_option('ConsistencyCheck', 'ErrorReturn'):
            self.Zaehler_ErrorReturn = config['ConsistencyCheck']['ErrorReturn']

        self.Zaehler_ReadPreValueFromFileMaxAge = 0
        if config.has_option('ConsistencyCheck', 'ReadPreValueFromFileMaxAge'):
            self.Zaehler_ReadPreValueFromFileMaxAge = int(config['ConsistencyCheck']['ReadPreValueFromFileMaxAge'])
        self.Zaehler_ReadPreValueFromFileAtStartup = False
        if config.has_option('ConsistencyCheck', 'ReadPreValueFromFileAtStartup'):
            self.Zaehler_ReadPreValueFromFileAtStartup = config['ConsistencyCheck']['ReadPreValueFromFileAtStartup']
            if self.Zaehler_ReadPreValueFromFileAtStartup.upper() == 'TRUE':
                self.Zaehler_ReadPreValueFromFileAtStartup = True
            else:
                self.Zaehler_ReadPreValueFromFileAtStartup = False

        ##################  LoadFileFromHTTP Parameters ########################
        self.HTTP_TimeoutLoadImage = 30                  # default Timeout = 30s
        if config.has_option('Imagesource', 'TimeoutLoadImage'):
            self.HTTP_TimeoutLoadImage = int(config['Imagesource']['TimeoutLoadImage'])
            
        self.HTTP_URLImageSource = ''
        self.URLImageSource_Enabled = config.has_option('Imagesource', 'URLImageSource')
        if self.URLImageSource_Enabled:
            self.HTTP_URLImageSource = config['Imagesource']['URLImageSource']

        self.HTTP_log_Image = ''
        self.LogImageLocation_Enabled = config.has_option('Imagesource', 'LogImageLocation')
        if self.LogImageLocation_Enabled:
            self.HTTP_log_Image = config['Imagesource']['LogImageLocation']   

        self.HTTP_LogOnlyFalsePictures = False
        self.HTTP_LogOnlyFalsePictures_Enabled = config.has_option('Imagesource', 'LogOnlyFalsePictures')
        if self.HTTP_LogOnlyFalsePictures_Enabled:
            self.HTTP_LogOnlyFalsePictures = bool(config['Imagesource']['LogOnlyFalsePictures'])


        ################## ImageCut Parameters ###############################
        self.Cut_FastMode = False
        if config.has_option('alignment', 'fastmode'):
            self.Cut_FastMode = config['alignment']['fastmode']
            if self.Cut_FastMode.upper() == 'TRUE':
                self.Cut_FastMode = True 
            else:
                self.Cut_FastMode = False    

        self.Cut_rotateAngle = float(config['alignment']['initial_rotation_angle'])
        print(self.Cut_rotateAngle)


        self.Cut_reference_name = []
        self.Cut_reference_name.append(config['alignment.ref0']['image'])
        self.Cut_reference_name.append(config['alignment.ref1']['image'])
        self.Cut_reference_name.append(config['alignment.ref2']['image'])

        self.Cut_reference_pos = []
        self.Cut_reference_pos.append((int(config['alignment.ref0']['pos_x']), int(config['alignment.ref0']['pos_y'])))
        self.Cut_reference_pos.append((int(config['alignment.ref1']['pos_x']), int(config['alignment.ref1']['pos_y'])))
        self.Cut_reference_pos.append((int(config['alignment.ref2']['pos_x']), int(config['alignment.ref2']['pos_y'])))


        self.AnalogReadOutEnabled = True
        if config.has_option('AnalogReadOut', 'Enabled'):
            self.AnalogReadOutEnabled = config['AnalogReadOut']['Enabled']
            if self.AnalogReadOutEnabled.upper() == 'FALSE':
                self.AnalogReadOutEnabled = False


        zw_Analog_Counter = config.get('Analog_Counter', 'names').split(',')
        self.Cut_Analog_Counter = []
        for nm in zw_Analog_Counter:
            nm = nm.strip()
            cnt = []
            cnt.append(nm)
            x1 = int(config['Analog_Counter.'+nm]['pos_x'])
            y1 = int(config['Analog_Counter.'+nm]['pos_y'])
            dx = int(config['Analog_Counter.'+nm]['dx'])
            dy = int(config['Analog_Counter.'+nm]['dy'])
            p_neu = (x1, y1, dx, dy)
            self.AnalogCounter_Default = p_neu
            cnt.append(p_neu)
            self.Cut_Analog_Counter.append(cnt)

        zw_Digital_Digit = config.get('Digital_Digit', 'names').split(',')
        self.Cut_Digital_Digit = []
        for nm in zw_Digital_Digit:
            nm = nm.strip()
            cnt = []
            cnt.append(nm)
            x1 = int(config['Digital_Digit.'+nm]['pos_x'])
            y1 = int(config['Digital_Digit.'+nm]['pos_y'])
            dx = int(config['Digital_Digit.'+nm]['dx'])
            dy = int(config['Digital_Digit.'+nm]['dy'])
            p_neu = (x1, y1, dx, dy)
            self.DigitalDigit_Default = p_neu
            cnt.append(p_neu)
            self.Cut_Digital_Digit.append(cnt)

    def CutGetAnalogCounter(self):
        return (self.Zaehler_AnalogReadOutEnabled, self.Cut_Analog_Counter)        

    def CutGetDigitalDigit(self):
        return (self.Cut_Digital_Digit)   

    def CutPreRotateAngle(self):
        return (self.Cut_rotateAngle)

    def CutReferenceParameter(self):
        return (self.Cut_reference_name, self.Cut_reference_pos)


    def LoadHTTPParameter(self):
        return (self.HTTP_TimeoutLoadImage, self.HTTP_URLImageSource, self.HTTP_log_Image, self.HTTP_LogOnlyFalsePictures)

    def ZaehlerAnalogEnabled(self):
        return self.Zaehler_AnalogReadOutEnabled

    def ZaehlerConsistency(self):
        return (self.Zaehler_ConsistencyEnabled, self.Zaehler_AllowNegativeRates, self.Zaehler_MaxRateValue, self.Zaehler_ErrorReturn)
        
    def ZaehlerReadPrevalue(self):
        return (self.Zaehler_ReadPreValueFromFileAtStartup, self.Zaehler_ReadPreValueFromFileMaxAge)


    def DigitModelFile(self):
        return self.Digit_model_file

    def DigitGetLogInfo(self):
        return (self.Digit_DoLog, self.Digit_LogNames, self.Digit_log_Image)

    def AnalogModelFile(self):
        return self.Analog_model_file

    def AnalogGetLogInfo(self):
        return (self.Analog_DoLog, self.Analog_LogNames, self.Analog_log_Image)

    def ConfigRerouteConfig(self):
        return (self.ConfigOriginalPath, self.ConfigReroutePath)

    def CheckAndLoadDefaultConfig(self, defaultdir):
        zw = str(self.PathToConfig.joinpath('config.ini'))
        if not os.path.exists(zw):
            for file in os.listdir(defaultdir):
                if os.path.isdir(defaultdir + file):
                    shutil.copytree(defaultdir + file, str(self.PathToConfig.joinpath(file)))
                else:
                    zw = str(self.PathToConfig.joinpath(file))
                    shutil.copyfile(defaultdir + file, zw)
        zw = str(self.PathToConfig.joinpath('prevalue.ini'))
        if not os.path.exists(zw):
            copyfile(defaultdir + 'prevalue.ini', zw)