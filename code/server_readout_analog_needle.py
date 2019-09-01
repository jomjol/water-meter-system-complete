from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse
import urllib.request
import socketserver

import lib.ReadAnalogNeedleClass
import cv2

AnalogReadout = lib.ReadAnalogNeedleClass.ReadAnalogNeedle()

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        global AnalogReadout
        if "/image_tmp/" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            with open('.'+self.path, 'rb') as file: 
                self.wfile.write(file.read()) # Read the file and send the contents 
        if "url=" in self.path:
            url = parse.parse_qs(parse.urlparse(self.path).query)['url'][0]
            urllib.request.urlretrieve(url, './image_tmp/original.jpg')
            ###################################################################################################
            # Readout erwartet ein Array von Bildern mit jeweils Array von Name und geladenem Bild (per OpenCV)
            # Notwendig für spätere Impementierung im Wasserzaehler mit mehreren Ziffer/Zähler
            loadedimg = cv2.imread('./image_tmp/original.jpg')  # Laden Bild per OpenCV
            picture = ['original.jpg', loadedimg]               # ein Bild: [Name, geladenes Bild]
            filelist = [picture]                                # Array der Bilder [Bild] - hier nur ein Bild
            ###################################################################################################
            result = AnalogReadout.Readout(filelist)
            txt = 'Original: <p><img src=/image_tmp/original.jpg></img><p>'
            txt = txt + 'Resize (32x32): <p><img src=/image_tmp/resize.jpg></img><p>'
            txt = txt + "Readout:\t" + "{:.1f}".format(result[0])
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(txt, 'UTF-8'))

PORT = 3000

with socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
