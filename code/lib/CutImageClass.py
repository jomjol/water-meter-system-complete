import numpy as np
import cv2
import configparser
import os
from shutil import copyfile
from PIL import Image
from pathlib import Path
import threading

class CutImage():
    def __init__(self, readconfig, zwpath='./image_tmp/'):
        self.PathImageZw = zwpath
        self.UpdateConfig(readconfig)

    def UpdateConfig(self, readconfig):
        (self.ConfigOriginalPath, self.ConfigReroutePath) = readconfig.ConfigRerouteConfig()

        self.rotateAngle = readconfig.CutPreRotateAngle()
        (self.reference_name, self.reference_pos) = readconfig.CutReferenceParameter()

        self.reference_image = []
        for i in range(3):
            zwname = self.ReplacePathToConfig(self.reference_name[i])
            self.reference_image.append(cv2.imread(str(zwname)))

        (self.AnalogReadOutEnabled, self.Analog_Counter) = readconfig.CutGetAnalogCounter()
        (self.Digital_Digit) = readconfig.CutGetDigitalDigit()
        self.FastMode = readconfig.Cut_FastMode
        self.M = None


    def ReplacePathToConfig(self, inp):
        zw1 = str(self.ConfigReroutePath)
        zw2 = Path(inp)
        zw2 = str(zw2)
        zw4 = str(Path(self.ConfigOriginalPath))
        zw3 = zw2.replace(zw4, zw1)
        zw3 = Path(zw3)
        return zw3

    def Cut(self, image):
        source = cv2.imread(image)
        cv2.imwrite(self.PathImageZw + 'org.jpg', source)
        target = self.RotateImage(source)
        cv2.imwrite(self.PathImageZw + 'rot.jpg', target)
        target = self.Alignment(target)
        cv2.imwrite(self.PathImageZw + 'alg.jpg', target)

        zeiger = self.cutZeiger(target)
        ziffern = self.cutZiffern(target)

        zeiger = ziffern
        if self.AnalogReadOutEnabled:
            zeiger = self.cutZeiger(target)

        return [zeiger, ziffern]

    def cutZeiger(self, source):
        result = []
        for zeiger in self.Analog_Counter:
#            img[y:y+h, x:x+w]
            x, y, dx, dy = zeiger[1]
            crop_img = source[y:y+dy, x:x+dx]
            name = self.PathImageZw + zeiger[0] + '.jpg'
            cv2.imwrite(name, crop_img)
            crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
            im_pil = Image.fromarray(crop_img)
            singleresult = [zeiger[0], im_pil]
            result.append(singleresult)
        return result

    def cutZiffern(self, source):
        result = []
        for zeiger in self.Digital_Digit:
            x, y, dx, dy = zeiger[1]
            crop_img = source[y:y+dy, x:x+dx]
            name = self.PathImageZw + zeiger[0] + '.jpg'
            cv2.imwrite(name, crop_img)
            crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
            im_pil = Image.fromarray(crop_img)
            singleresult = [zeiger[0], im_pil]
            result.append(singleresult)
        return result

    def Alignment(self, source):
        h, w, ch = source.shape
        if (self.M is None) or (self.FastMode == False):
            self.CalculateAffineTransform(source)
        else:
            CalcAffTransOffline = self.CalcAffTransOfflineClass(self)
            CalcAffTransOffline.start()            
        target = cv2.warpAffine(source, self.M, (w, h))
        return target

    def Alignment(self, source):
        h, w, ch = source.shape
        p0 = self.getRefCoordinate(source, self.reference_image[0])
        p1 = self.getRefCoordinate(source, self.reference_image[1])
        p2 = self.getRefCoordinate(source, self.reference_image[2])

        pts1 = np.float32([p0, p1, p2])
        pts2 = np.float32([self.reference_pos[0], self.reference_pos[1], self.reference_pos[2]])
        M = cv2.getAffineTransform(pts1,pts2)
        target = cv2.warpAffine(source ,M, (w, h))
        return target

    def CalculateAffineTransform(self, source):
        print("Cut CalcAffineTransformation")
        h, w, ch = source.shape
        if debug: 
            print(self.gettimestring() + " Align 01a")        
        p0 = self.getRefCoordinate(source, self.reference_image[0])
        if debug: 
            print(self.gettimestring() + " Align 01b")  
        p1 = self.getRefCoordinate(source, self.reference_image[1])
        if debug: 
            print(self.gettimestring() + " Align 01c")  
        p2 = self.getRefCoordinate(source, self.reference_image[2])
        if debug: 
            print(self.gettimestring() + " Align 02")  

        pts1 = np.float32([p0, p1, p2])
        pts2 = np.float32([self.reference_pos[0], self.reference_pos[1], self.reference_pos[2]])
        self.M = cv2.getAffineTransform(pts1,pts2)


    class CalcAffTransOfflineClass(threading.Thread):
        def __init__(self, _master):
            threading.Thread.__init__(self)
            self.master = _master

        def run(self):
            self.master.CalculateAffineTransform(self.master.targetrot)

    def CutAfter(self):
        print("Cut After")
        if self.FastMode:
            CalcAffTransOffline = self.CalcAffTransOfflineClass(self)
            CalcAffTransOffline.start()        

    def getRefCoordinate(self, image, template):
#        method = cv2.TM_SQDIFF                     #2
        method = cv2.TM_SQDIFF_NORMED              #1
#        method = cv2.TM_CCORR_NORMED                #3
        method = cv2.TM_CCOEFF_NORMED                #4
        res = cv2.matchTemplate(image, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
#        bottom_right = (top_left[0] + w, top_left[1] + h)
        return top_left


    def RotateImage(self, image):
        h, w, ch = image.shape
        center = (w / 2, h / 2)
        M = cv2.getRotationMatrix2D(center, self.rotateAngle, 1.0)
        image = cv2.warpAffine(image, M, (w, h))
        return image

    def DrawROIOLDOLDOLD(self, url):
        im = cv2.imread(url)

        d = 2
        d_eclipse = 1

        x = self.reference_p0[0]
        y = self.reference_p0[1]
        h, w =  self.ref0.shape[:2]
        cv2.rectangle(im,(x-d,y-d),(x+w+2*d,y+h+2*d),(0,0,255),d)
        cv2.putText(im,'ref0',(x,y-5),0,0.4,(0,0,255))

        x = self.reference_p1[0]
        y = self.reference_p1[1]
        h, w =  self.ref1.shape[:2]
        cv2.rectangle(im,(x-d,y-d),(x+w+2*d,y+h+2*d),(0,0,255),d)
        cv2.putText(im,'ref1',(x,y-5),0,0.4,(0,0,255))
        
        x = self.reference_p2[0]
        y = self.reference_p2[1]
        h, w =  self.ref2.shape[:2]
        cv2.rectangle(im,(x-d,y-d),(x+w+2*d,y+h+2*d),(0,0,255),d)
        cv2.putText(im,'ref2',(x,y-5),0,0.4,(0,0,255))

        if self.AnalogReadOutEnabled:
            for zeiger in self.Analog_Counter:
                x, y, w, h = zeiger[1]
                cv2.rectangle(im,(x-d,y-d),(x+w+2*d,y+h+2*d),(0,255,0),d)
                xct = int(x+w/2)+1
                yct = int(y+h/2)+1
                cv2.line(im,(xct-5,yct),(xct+5,yct),(0,255,0),1)
                cv2.line(im,(xct,yct-5),(xct,yct+5),(0,255,0),1)
                cv2.ellipse(im, (xct, yct), (int(w/2)+2*d_eclipse, int(h/2)+2*d_eclipse), 0, 0, 360, (0,255,0), d_eclipse)
                cv2.putText(im,zeiger[0],(x,y-5),0,0.4,(0,255,0))
        for zeiger in self.Digital_Digit:
            x, y, w, h = zeiger[1]
            cv2.rectangle(im,(x-d,y-d),(x+w+2*d,y+h+2*d),(0,255,0),d)
            cv2.putText(im,zeiger[0],(x,y-5),0,0.4,(0,255,0))
        cv2.imwrite('./image_tmp/roi.jpg', im)

    def DrawROI(self, image_in, image_out='./image_tmp/roi.jpg', draw_ref=False, draw_dig=True, draw_cou=True, ign_ref=-1, ign_dig=-1, ign_cou=-1):
        zwimage = str(image_in)
        im = cv2.imread(zwimage)

        d = 3
        d_eclipse = 1
        _colour = (255, 0, 0)

        if draw_ref:
            for i in range(3):
                if i != ign_ref:
                    x, y = self.reference_pos[i]
                    h, w = self.reference_image[i].shape[:2]
                    cv2.rectangle(im,(x-d,y-d),(x+w+2*d,y+h+2*d),_colour,d)
                    cv2.putText(im,self.reference_name[i].replace("./config/", ""),(x,y-5),0,0.4,_colour)


        if self.AnalogReadOutEnabled and draw_cou:
            for i in range(len(self.Analog_Counter)):
                if i != ign_cou:
                    x, y, w, h = self.Analog_Counter[i][1]
                    cv2.rectangle(im,(x-d,y-d),(x+w+2*d,y+h+2*d),(0,255,0),d)
                    xct = int(x+w/2)+1
                    yct = int(y+h/2)+1
                    cv2.line(im,(x,yct),(x+w+5,yct),(0,255,0),1)
                    cv2.line(im,(xct,y),(xct,y+h),(0,255,0),1)
                    cv2.ellipse(im, (xct, yct), (int(w/2)+2*d_eclipse, int(h/2)+2*d_eclipse), 0, 0, 360, (0,255,0), d_eclipse)
                    cv2.putText(im,self.Analog_Counter[i][0],(x,y-5),0,0.5,(0,255,0))

        if draw_dig:
            for i in range(len(self.Digital_Digit)):
                if i != ign_dig:
                    x, y, w, h = self.Digital_Digit[i][1]
                    cv2.rectangle(im,(x-d,y-d),(x+w+2*d,y+h+2*d),(0,255,0),d)
                    cv2.putText(im,self.Digital_Digit[i][0],(x,y-5),0,0.5,(0,255,0))

        zwname = str(image_out)
        cv2.imwrite(zwname, im)