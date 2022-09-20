from data.data import Data
from page.page import Page

import http.server
from urllib.parse import parse_qs

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


    def do_POST(self):
        if "/dictionary/" in self.path:
            path = self.toLocalPath(self.path + ".html")
            field_data = self.rfile.read(int(self.headers['Content-Length'])).decode("utf8")
            message = parse_qs(field_data)

            err = False
            errMsg = ""
            if message['action'][0] == "save":
                [err, errMsg] = Data().checkSaveWord(path, message['content'][0])

            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            if err == True:
                message = errMsg
                self.wfile.write(bytes(message, "utf8"))
            else:
                message = "Checked!"
                self.wfile.write(bytes(message, "utf8"))

        if "/suggestion/" in self.path:
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            message = self.rfile.read(int(self.headers['Content-Length'])).decode("utf8")
            words = Data().getDictWords(message)
            self.wfile.write(bytes(words, "utf8"))

