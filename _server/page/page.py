from curses import newpad
from model.path import Path

from bs4 import BeautifulSoup
from urllib.parse import unquote
import os

class Page(object):
    def __init__(self, path):
        #print("Loading " + path)
        newPath = Path.urlDecodePath(path)
        if newPath == path:
            self.path = newPath
        else:
            if os.path.exists(path) and not os.path.exists(newPath):
                dir = os.path.dirname(newPath)
                if dir != "dictionary":
                    os.makedirs(dir)
                os.rename(path, newPath)
            self.path = newPath    
        with open(self.path) as fp:
            self.page = BeautifulSoup(fp, 'html.parser')

    def save(self):
        f = open(self.path, "w")
        f.write(str(self.page))
        f.close()  

    def getRoot(self) -> BeautifulSoup:
        return self.page