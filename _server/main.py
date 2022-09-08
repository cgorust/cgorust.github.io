from server.server import Server
from data.data import Data

import os

os.chdir("..")
data = Data()
server = Server()
server.run()

