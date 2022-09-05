from http import server

class handler(server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = server.SimpleHTTPRequestHandler.translate_path(self, path)
        if path != "/":
            path += ".html"
        return path


with server.HTTPServer(('', 8000), handler) as httpServer:
    httpServer.serve_forever()
