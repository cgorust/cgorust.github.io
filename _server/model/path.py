from bs4 import BeautifulSoup
import urllib.parse

class Path:
    @classmethod
    def isEncodedPath(cls, path) -> str:
        newPath = urllib.parse.unquote(path)
        if newPath == path:
            return False
        return True

    @classmethod
    def encodePath(cls, path) -> str:
        if cls.isEncodedPath(path):
            return path
        path = urllib.parse.quote(path)
        path = path.replace("#", "%23")
        return path

    @classmethod
    def decodePath(cls, path) -> str:
        if not cls.isEncodedPath(path):
            return path
        path = urllib.parse.unquote(path)
        path = path.replace("%23", "#")
        return path

    @classmethod
    def pathToKey(cls, path) -> str:
        path = path.replace(".html", "").replace("dictionary/", "")
        path = cls.decodePath(path)
        if path.lower().capitalize() != path:
            print("Path format error:" + path)
        return path

    @classmethod
    def keyToPath(cls, key) -> str:
        path = key
        path = "dictionary/" + path + ".html"
        return path

    @classmethod
    def getAddr(cls, header) -> str:
        addr = BeautifulSoup("<a href=\"/" + cls.headerToPath(header).replace(".html", "") + "\">"
            + header +"</a>", 'html.parser')
        return str(addr)

    @classmethod
    def headerToKey(cls, header) -> str:
        key = header.replace(" ", "_").capitalize()
        return key        

    @classmethod
    def headerToPath(cls, header) -> str: 
        return cls.keyToPath(cls.headerToKey(header))           