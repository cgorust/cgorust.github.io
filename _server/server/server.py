from server.serverHandler import ServerHandler
from lib.singleton import Singleton

import http.server

PORT = 8000

class Server(object, metaclass = Singleton):
    def __init__(self):
        self.httpServer = http.server.HTTPServer(('', PORT), ServerHandler)

    def run(self):
        self.httpServer.serve_forever()

    def __del__(self):
        self.httpServer.shutdown()
        self.httpServer.server_close()