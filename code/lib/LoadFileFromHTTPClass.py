import urllib.request
from multiprocessing import Process, Event
from PIL import Image
from shutil import copyfile
import time 
import os


class LoadFileFromHttp:
    def __init__(self, readconfig):
        (self.TimeoutLoadImage, self.URLImageSource, self.log_Image, self.LogOnlyFalsePictures) = readconfig.LoadHTTPParameter()
        self.CheckAndLoadDefaultConfig()
        self.LastImageSafed = ''

    def CheckAndLoadDefaultConfig(self):
        if len(self.log_Image) > 0:
            if not os.path.exists(self.log_Image):
                zerlegt = self.log_Image.split('/')
                pfad = zerlegt[0]
                for i in range(1, len(zerlegt)):
                    pfad = pfad + '/' + zerlegt[i]
                    if not os.path.exists(pfad):
                        os.makedirs(pfad)

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
        action_process.close()

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
