from bs4 import BeautifulSoup
from urllib.parse import unquote

class Page(object):
    def __init__(self, path):
        #print("Loading " + path)
        self.path = path
        with open(path) as fp:
            self.page = BeautifulSoup(fp, 'html.parser')

    def save(self):
        f = open(self.path, "w")
        f.write(str(self.page))
        f.close()  

    def unescapePath(self, path):
        path = unquote(path)
        path = path.replace("%23", "#")
        return path

    def escapePath(self, path):
        return path.replace("#", "%23")

    def getRoot(self):
        return self.page