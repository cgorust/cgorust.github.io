from singleton import Singleton

from bs4 import BeautifulSoup
import difflib

class File(object):
    __metaclass__ = Singleton    

    def getHTML(self, path):
        with open(path) as fp:
            return BeautifulSoup(fp, 'html.parser')

    def diffFile(self, pageA, pageB):
        diffList = difflib.ndiff(pageA, pageB) 
        if next(diffList, None) is not None:
            print("file changed")
           
