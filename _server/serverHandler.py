from data import Data

import http.server
import os

class ServerHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def do_GET(self):
        if "/dictionary/" in self.path:
            self.path += ".html"
            print(self.path)
            data = Data()
            data.checkWordPage(self.path)
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        return http.server.SimpleHTTPRequestHandler.do_GET(self)    


