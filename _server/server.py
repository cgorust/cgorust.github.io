from http import server
import os
import subprocess

class handler(server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = server.SimpleHTTPRequestHandler.translate_path(self, path)
        print(path)
        if "fileToedit.html" in path:
            pass
        if "/dictionary/" in path:
            path += ".html"
        if "/edit/" in path:
            file = path.split("/edit/")[-1]
            path = path.split("/edit/")[0]+"/fileToEdit.html"
            file = "dictionary/" + file
            subprocess.call('cp ' + file + ".html" + ' ' + "fileToEdit.html", shell=True)
        return path


with server.HTTPServer(('', 8000), handler) as httpServer:
    httpServer.serve_forever()
