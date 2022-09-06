from server import Server
from data import Data

import os

os.chdir("..")
data = Data()
server = Server()
server.run()

