from data import Data

import http.server

class ServerHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def toLocalPath(self, path: str) -> str:
        if path[0]=='/':
            path = path[1:]
        return path

    def do_GET(self):
        if "/dictionary/" in self.path:
            self.path += ".html"

            Data().checkWordPage(self.toLocalPath(self.path))
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        return http.server.SimpleHTTPRequestHandler.do_GET(self)    


