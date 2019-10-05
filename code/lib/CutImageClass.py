import numpy as np
import cv2
import configparser
import os
from shutil import copyfile




class CutImage:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./config/config.ini')

        self.rotateAngle = float(config['alignment']['initial_rotation_angle'])

        self.reference_image0 = config['alignment.ref0']['image']
        self.reference_p0 = (int(config['alignment.ref0']['pos_x']), int(config['alignment.ref0']['pos_y']))


        self.reference_image1 = config['alignment.ref1']['image']
        self.reference_p1 = (int(config['alignment.ref1']['pos_x']), int(config['alignment.ref1']['pos_y']))

        self.reference_image2 = config['alignment.ref2']['image']
        self.reference_p2 = (int(config['alignment.ref2']['pos_x']), int(config['alignment.ref2']['pos_y']))

        self.CheckAndLoadDefaultConfig()

        self.ref0 = cv2.imread(self.reference_image0)
        self.ref1 = cv2.imread(self.reference_image1)
        self.ref2 = cv2.imread(self.reference_image2)


        zw_Analog_Counter = config.get('Analog_Counter', 'names').split(',')
        self.Analog_Counter = []
        for nm in zw_Analog_Counter:
            nm = nm.strip()
            cnt = []
            cnt.append(nm)
            x1 = int(config['Analog_Counter.'+nm]['pos_x'])
            y1 = int(config['Analog_Counter.'+nm]['pos_y'])
            dx = int(config['Analog_Counter.'+nm]['dx'])
            dy = int(config['Analog_Counter.'+nm]['dy'])
            p_neu = (x1, y1, dx, dy)
            cnt.append(p_neu)
            self.Analog_Counter.append(cnt)

        zw_Digital_Digit = config.get('Digital_Digit', 'names').split(',')
        self.Digital_Digit = []
        for nm in zw_Digital_Digit:
            nm = nm.strip()
            cnt = []
            cnt.append(nm)
            x1 = int(config['Digital_Digit.'+nm]['pos_x'])
            y1 = int(config['Digital_Digit.'+nm]['pos_y'])
            dx = int(config['Digital_Digit.'+nm]['dx'])
            dy = int(config['Digital_Digit.'+nm]['dy'])
            p_neu = (x1, y1, dx, dy)
            cnt.append(p_neu)
            self.Digital_Digit.append(cnt)

    def CheckAndLoadDefaultConfig(self):
        defaultdir = "./config_default/"
        targetdir = './config/'
        if not os.path.exists(self.reference_image0):
            zerlegt = self.reference_image0.split('/')
            pfad = zerlegt[0]
            for i in range(1, len(zerlegt)-1):
                pfad = pfad + '/' + zerlegt[i]
                if not os.path.exists(pfad):
                    os.makedirs(pfad)
            defaultmodel = self.reference_image0.replace(targetdir, defaultdir)
            copyfile(defaultmodel, self.reference_image0)

        if not os.path.exists(self.reference_image1):
            zerlegt = self.reference_image1.split('/')
            pfad = zerlegt[0]
            for i in range(1, len(zerlegt)-1):
                pfad = pfad + '/' + zerlegt[i]
                if not os.path.exists(pfad):
                    os.makedirs(pfad)
            defaultmodel = self.reference_image1.replace(targetdir, defaultdir)
            copyfile(defaultmodel, self.reference_image1)

        if not os.path.exists(self.reference_image2):
            zerlegt = self.reference_image2.split('/')
            pfad = zerlegt[0]
            for i in range(1, len(zerlegt)-1):
                pfad = pfad + '/' + zerlegt[i]
                if not os.path.exists(pfad):
                    os.makedirs(pfad)
            defaultmodel = self.reference_image2.replace(targetdir, defaultdir)
            copyfile(defaultmodel, self.reference_image2)

    def Cut(self, image):
        source = cv2.imread(image)
        cv2.imwrite('./image_tmp/org.jpg', source)
        target = self.RotateImage(source)
        cv2.imwrite('./image_tmp/rot.jpg', target)
        target = self.Alignment(target)
        cv2.imwrite('./image_tmp/alg.jpg', target)

        zeiger = self.cutZeiger(target)
        ziffern = self.cutZiffern(target)

        return [zeiger, ziffern]

    def cutZeiger(self, source):
        result = []
        for zeiger in self.Analog_Counter:
#            img[y:y+h, x:x+w]
            x, y, dx, dy = zeiger[1]
            crop_img = source[y:y+dy, x:x+dx]
            name = './image_tmp/' + zeiger[0] + '.jpg'
            cv2.imwrite(name, crop_img)
            singleresult = [zeiger[0], crop_img]
            result.append(singleresult)
        return result

    def cutZiffern(self, source):
        result = []
        for zeiger in self.Digital_Digit:
            x, y, dx, dy = zeiger[1]
            crop_img = source[y:y+dy, x:x+dx]
            name = './image_tmp/' + zeiger[0] + '.jpg'
            cv2.imwrite(name, crop_img)
            singleresult = [zeiger[0], crop_img]
            result.append(singleresult)
        return result


    def Alignment(self, source):
        h, w, ch = source.shape
        p0 = self.getRefCoordinate(source, self.ref0)
        p1 = self.getRefCoordinate(source, self.ref1)
        p2 = self.getRefCoordinate(source, self.ref2)

        pts1 = np.float32([p0, p1, p2])
        pts2 = np.float32([self.reference_p0, self.reference_p1, self.reference_p2])
        M = cv2.getAffineTransform(pts1,pts2)
        target = cv2.warpAffine(source ,M, (w, h))
        return target

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

    def DrawROI(self, url):
        im = cv2.imread(url)

        d = 2

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

        for zeiger in self.Analog_Counter:
            x, y, w, h = zeiger[1]
            cv2.rectangle(im,(x-d,y-d),(x+w+2*d,y+h+2*d),(0,255,0),d)
            cv2.putText(im,zeiger[0],(x,y-5),0,0.4,(0,255,0))
        for zeiger in self.Digital_Digit:
            x, y, w, h = zeiger[1]
            cv2.rectangle(im,(x-d,y-d),(x+w+2*d,y+h+2*d),(0,255,0),d)
            cv2.putText(im,zeiger[0],(x,y-5),0,0.4,(0,255,0))
        cv2.imwrite('./image_tmp/roi.jpg', im)

