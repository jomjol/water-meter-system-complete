from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse
import urllib.request
import lib.ZaehlerstandClass

#import http.server
import socketserver

wasserzaehler = lib.ZaehlerstandClass.Zaehlerstand()

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        global wasserzaehler
        if "/image_tmp/" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            with open('.'+self.path, 'rb') as file: 
                self.wfile.write(file.read()) # Read the file and send the contents 
        if "url=" in self.path:
            url = parse.parse_qs(parse.urlparse(self.path).query)['url'][0]
            simple = True
            preValue = ''
            if ('&full' in self.path) or ('?full' in self.path):
                simple = False
            if 'prevalue' in self.path:
                preValue = parse.parse_qs(parse.urlparse(self.path).query)['prevalue'][0]
            urllib.request.urlretrieve(url, './image_tmp/original.jpg')
            print('Picture Download done')
            result = 'Hello World'
            result = wasserzaehler.getZaehlerstand('./image_tmp/original.jpg', simple, preValue)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(result, 'UTF-8'))

PORT = 3000

with socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
