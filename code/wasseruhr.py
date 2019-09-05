from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse
import lib.ZaehlerstandClass

import socketserver

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        global wasserzaehler
        url_parse = parse.urlparse(self.path)
        query_parse = parse.parse_qs(url_parse.query)

        if "/image_tmp/" in url_parse.path:
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            with open('.'+self.path, 'rb') as file: 
                self.wfile.write(file.read()) # Read the file and send the contents
            return

        url = ''
        if 'url' in query_parse:
            url = query_parse['url'][0]

        simple = True
        if ('&full' in self.path) or ('?full' in self.path):
            simple = False

        preValue = ''
        if 'prevalue' in query_parse:
            url = query_parse['prevalue'][0]

        if (len(url) > 0) or ('wasserzaehler' in url_parse.path):
            result = wasserzaehler.getZaehlerstand(url, simple, preValue)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(result, 'UTF-8'))

if __name__ == '__main__':

    wasserzaehler = lib.ZaehlerstandClass.Zaehlerstand()

    PORT = 3000
    with socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
        print("Wasserzaehler is serving at port", PORT)
        httpd.serve_forever()
