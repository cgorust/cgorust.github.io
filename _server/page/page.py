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

    def getRoot(self) -> BeautifulSoup:
        return self.page