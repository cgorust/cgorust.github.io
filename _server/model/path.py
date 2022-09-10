from model.text import Text

from bs4 import BeautifulSoup
import urllib.parse
import html

class Path:
    @classmethod
    def isUrlEncodedPath(cls, path) -> str:
        newPath = urllib.parse.unquote(path)
        if newPath == path:
            return False
        return True

    @classmethod
    def urlEncodePath(cls, path) -> str:
        if cls.isUrlEncodedPath(path):
            return path
        path = urllib.parse.quote(path)
        path = path.replace("#", "%23")
        return path

    @classmethod
    def urlDecodePath(cls, path) -> str:
        if not cls.isUrlEncodedPath(path):
            return path
        path = urllib.parse.unquote(path)
        path = path.replace("%23", "#")
        return path

    @classmethod
    def pathToKey(cls, path) -> str:
        path = path.replace(".html", "").replace("dictionary/", "")
        path = cls.urlDecodePath(path)
        if path.lower().capitalize() != path:
            print("Path format error:" + path)
        return path

    @classmethod
    def keyToPath(cls, key) -> str:
        path = key
        path = Path.urlEncodePath(path)
        path = "dictionary/" + path + ".html"
        return path

    @classmethod
    def getAddr(cls, header) -> str:
        addr = BeautifulSoup("<a href=\"/" + cls.headerToPath(header).replace(".html", "") + "\">"
            + Text.htmlEncodeText(header) +"</a>", 'html.parser')
        return str(addr)

    @classmethod
    def headerToKey(cls, header) -> str:
        key = header.replace(" ", "_").capitalize()
        return key        

    @classmethod
    def headerToPath(cls, header) -> str: 
        return cls.keyToPath(cls.headerToKey(header))           