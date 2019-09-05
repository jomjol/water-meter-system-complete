import configparser
import urllib.request
from multiprocessing import Process, Event
from PIL import Image
from shutil import copyfile
import time 
import os


class LoadFileFromHttp:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./config/config.ini')

        self.TimeoutLoadImage = 30                  # default Timeout = 30s
        if config.has_option('Imagesource', 'TimeoutLoadImage'):
            self.TimeoutLoadImage = int(config['Imagesource']['TimeoutLoadImage'])
            
        self.URLImageSource = ''
        if config.has_option('Imagesource', 'URLImageSource'):
            self.URLImageSource = config['Imagesource']['URLImageSource']

        self.log_Image = ''
        if config.has_option('Imagesource', 'LogImageLocation'):
            self.log_Image = config['Imagesource']['LogImageLocation']   

        self.LogOnlyFalsePictures = False
        if config.has_option('Imagesource', 'LogOnlyFalsePictures'):
            self.LogOnlyFalsePictures = bool(config['Imagesource']['LogOnlyFalsePictures'])
        
        self.LastImageSafed = ''


    def ReadURL(self, event, url, target):
        urllib.request.urlretrieve(url, target)
        event.set()

    def LoadImageFromURL(self, url, target):
        self.LastImageSafed = ''
        if url == '':
            url = self.URLImageSource
        event = Event()
        action_process = Process(target=self.ReadURL, args=(event, url, target))
        action_process.start()
        action_process.join(timeout=self.TimeoutLoadImage)
        action_process.terminate()

        logtime = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
        if event.is_set():
            self.saveLogImage(target, logtime)
            if self.VerifyImage(target) == True:
                result = ''
            else:
                result = 'Error - Imagefile is corrupted'
        else:
            result = 'Error - Problem during Imageload (file not exists or timeout)'
        return (result, logtime)

    def PostProcessLogImageProcedure(self, everythingsuccessfull):
        if (len(self.log_Image) > 0) and self.LogOnlyFalsePictures and (len(self.LastImageSafed) > 0) and everythingsuccessfull:
            os.remove(self.LastImageSafed)
            self.LastImageSafed = '' 

    def VerifyImage(self, img_file):
        try:
            v_image = Image.open(img_file)
            v_image.verify()
            return True
        except OSError:
            return False

    def saveLogImage(self, img_file, logtime):
        if len(self.log_Image) > 0:
            speichername = self.log_Image + '/SourceImage_' + logtime + '.jpg'
            copyfile(img_file, speichername)
            self.LastImageSafed = speichername
