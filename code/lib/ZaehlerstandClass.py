import configparser
import lib.ReadAnalogNeedleClass
import lib.CutImageClass
import lib.ReadDigitalDigitClass
import lib.LoadFileFromHTTPClass
import math
import os
from shutil import copyfile

class Zaehlerstand:
    def __init__(self):
        self.CheckAndLoadDefaultConfig()

        config = configparser.ConfigParser()
        config.read('./config/config.ini')

        print('Start Init Zaehlerstand')
        self.readAnalogNeedle = lib.ReadAnalogNeedleClass.ReadAnalogNeedle()
        print('Analog Model Init Done')
        self.readDigitalDigit = lib.ReadDigitalDigitClass.ReadDigitalDigit()
        print('Digital Model Init Done')
        self.CutImage = lib.CutImageClass.CutImage()
        print('Digital Model Init Done')
        self.LoadFileFromHTTP = lib.LoadFileFromHTTPClass.LoadFileFromHttp()

        self.ConsistencyEnabled = False        
        if config.has_option('ConsistencyCheck', 'Enabled'):
            self.ConsistencyEnabled = config['ConsistencyCheck']['Enabled']
            if self.ConsistencyEnabled.upper() == 'TRUE':
                self.ConsistencyEnabled = True

        self.AllowNegativeRates = True
        if config.has_option('ConsistencyCheck', 'AllowNegativeRates'):
            self.AllowNegativeRates = config['ConsistencyCheck']['AllowNegativeRates']
            if self.AllowNegativeRates.upper() == 'FALSE':
                self.AllowNegativeRates = False

        if config.has_option('ConsistencyCheck', 'MaxRateValue'):
            self.MaxRateValue = float(config['ConsistencyCheck']['MaxRateValue'])
        if config.has_option('ConsistencyCheck', 'ErrorReturn'):
            self.ErrorReturn = config['ConsistencyCheck']['ErrorReturn']

        self.LastVorkomma = ''
        self.LastNachkomma = ''

    def CheckAndLoadDefaultConfig(self):
        defaultdir = "./config_default/"
        targetdir = './config/'
        if not os.path.exists('./config/config.ini'):
            copyfile(defaultdir + 'config.ini', targetdir + 'config.ini')

    def setPreValue(self, setValue):
        zerlegt = setValue.split('.')
        vorkomma = zerlegt[0][0:len(self.CutImage.Digital_Digit)]
        self.LastVorkomma = vorkomma.zfill(len(self.CutImage.Digital_Digit))
        nachkomma = zerlegt[1][0:len(self.CutImage.Analog_Counter)]
        while len(nachkomma) < len(self.CutImage.Analog_Counter):
            nachkomma = nachkomma + '0'
        self.LastNachkomma = nachkomma
        result = 'Last value set to:  ' + self.LastVorkomma + '.' + self.LastNachkomma
        return result

    def getROI(self, url):
        txt, logtime = self.LoadFileFromHTTP.LoadImageFromURL(url, './image_tmp/original.jpg')

        if len(txt) == 0:
            self.CutImage.Cut('./image_tmp/original.jpg')
            print('Start ROI')
            self.CutImage.DrawROI('./image_tmp/alg.jpg')
            txt = '<p>ROI Image: <p><img src=/image_tmp/roi.jpg></img><p>'
            print('Get ROI done')
        return txt


    def getZaehlerstand(self, url, simple = True, UsePreValue = False, single = False, ignoreConsistencyCheck = False):
        txt, logtime = self.LoadFileFromHTTP.LoadImageFromURL(url, './image_tmp/original.jpg')

        if len(txt) == 0:
            print('Start CutImage, AnalogReadout, DigitalReadout')
            resultcut = self.CutImage.Cut('./image_tmp/original.jpg')
            resultanalog = self.readAnalogNeedle.Readout(resultcut[0], logtime)
            resultdigital = self.readDigitalDigit.Readout(resultcut[1], logtime)
            
            self.akt_nachkomma = self.AnalogReadoutToValue(resultanalog)
            self.akt_vorkomma = self.DigitalReadoutToValue(resultdigital, UsePreValue, self.LastNachkomma, self.akt_nachkomma)
            self.LoadFileFromHTTP.PostProcessLogImageProcedure(True)

            print('Start Making Zaehlerstand')
            (error, errortxt) = self.checkConsistency(ignoreConsistencyCheck)
            self.UpdateLastValues(error)
            txt = self.MakeReturnValue(error, errortxt, single)

            if not simple:
                txt = txt + '<p>Aligned Image: <p><img src=/image_tmp/alg.jpg></img><p>'
                txt = txt + 'Digital Counter: <p>'
                for i in range(len(resultdigital)):
                    if resultdigital[i] == 'NaN':
                        zw = 'NaN'
                    else:
                        zw = str(int(resultdigital[i]))
                    txt += '<img src=/image_tmp/'+  str(resultcut[1][i][0]) + '.jpg></img>' + zw
                txt = txt + '<p>'
                txt = txt + 'Analog Meter: <p>'
                for i in range(len(resultanalog)):
                    txt += '<img src=/image_tmp/'+  str(resultcut[0][i][0]) + '.jpg></img>' + "{:.1f}".format(resultanalog[i])
                txt = txt + '<p>'
            print('Get Zaehlerstand done')
        return txt

    def MakeReturnValue(self, error, errortxt, single):
        output = ''
        if (error):
            if self.ErrorReturn.find('Value') > -1:
                output = str(self.akt_vorkomma.lstrip("0")) + '.' + str(self.akt_nachkomma)
                if not single:
                    output = output + '\t' + self.akt_vorkomma  + '\t' + self.akt_nachkomma
            if len(output) > 0:
                output = output + '\t' + errortxt
            else:
                 output = errortxt
        else:
            output = str(self.akt_vorkomma.lstrip("0")) + '.' + str(self.akt_nachkomma)
            if not single:
                output = output + '\t' + self.akt_vorkomma  + '\t' + self.akt_nachkomma
        return output

    def UpdateLastValues(self, error):
        if 'N' in self.akt_vorkomma:
            return
        if error:
            if self.ErrorReturn.find('NewValue') > -1:
                self.LastNachkomma = self.akt_nachkomma
                self.LastVorkomma = self.akt_vorkomma
            else:
                self.akt_nachkomma = self.LastNachkomma
                self.akt_vorkomma = self.LastVorkomma
        else:
            self.LastNachkomma = self.akt_nachkomma
            self.LastVorkomma = self.akt_vorkomma

    def checkConsistency(self, ignoreConsistencyCheck):
        error = False
        errortxt = ''
        if (len(self.LastVorkomma) > 0) and not('N' in self.akt_vorkomma) and self.ConsistencyEnabled:
            akt_zaehlerstand = float(str(self.akt_vorkomma.lstrip("0")) + '.' + str(self.akt_nachkomma))   
            old_zaehlerstand = float(str(self.LastVorkomma.lstrip("0")) + '.' + str(self.LastNachkomma)) 
            delta = akt_zaehlerstand - old_zaehlerstand
            if not(self.AllowNegativeRates) and (delta < 0):
                error = True
                errortxt = "ErrorNegativeRate"
            if abs(delta) > self.MaxRateValue:
                if error:
                    errortxt = "ErrorRateTooHigh (" + str(delta) + ")" + errortxt
                else:
                    errortxt = "ErrorRateTooHigh (" + str(delta) + ")"
                error = True
            if self.ErrorReturn.find('ErrorMessage') == -1:
                errortxt = ''
            if error and (self.ErrorReturn.find('Readout') > -1):
                if len(errortxt):
                    errortxt = errortxt + '\t' + str(akt_zaehlerstand)
                else:
                    errortxt = str(akt_zaehlerstand)
        return (error, errortxt)

    def AnalogReadoutToValue(self, res_analog):
        prev = -1
        erg = ''
        for item in res_analog[::-1]:
#        for item in res_analog:
            prev = self.ZeigerEval(item, prev)
            erg = str(int(prev)) + erg
        return erg

    def ZeigerEval(self, zahl, ziffer_vorgaenger):
        ergebnis_nachkomma = math.floor((zahl * 10) % 10)
        ergebnis_vorkomma = math.floor(zahl % 10)

        if ziffer_vorgaenger == -1:
            ergebnis = ergebnis_vorkomma
        else:
            ergebnis_rating = ergebnis_nachkomma - ziffer_vorgaenger
            if ergebnis_nachkomma >= 5:
                ergebnis_rating-=5
            else:
                ergebnis_rating+=5
            ergebnis = round(zahl)
            if ergebnis_rating < 0:
                ergebnis-=1
            if ergebnis == -1:
                ergebnis+=10

        ergebnis = ergebnis  % 10
        return ergebnis


    def DigitalReadoutToValue(self, res_digital, UsePreValue, lastnachkomma, aktnachkomma):
        erg = ''
        if UsePreValue and (len(self.LastVorkomma) > 0) and (len(self.LastNachkomma) > 0):
            last = int(lastnachkomma[0:1])
            aktu = int(aktnachkomma[0:1])
            if aktu < last:
                overZero = 1
            else:
                overZero = 0
        else:
            UsePreValue = False
        
        for i in range(len(res_digital)-1, -1, -1):
            item = res_digital[i]
            if item == 'NaN':
                if UsePreValue:
                    item = int(self.LastVorkomma[i])
                    if overZero:
                        item = item + 1
                        if item == 10:
                            item = 0
                            overZero = 1
                        else:
                            overZero = 0
                else:
                    item = 'N'
            erg = str(item) + erg

        return erg

