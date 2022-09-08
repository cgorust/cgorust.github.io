from bs4 import BeautifulSoup
import urllib.parse

class Path:
    @classmethod
    def pathToKey(cls, path) -> str:
        path = path.replace(".html", "").replace("dictionary/", "")
        path = urllib.parse.unquote(path)
        if path.lower().capitalize() != path:
            print("Path format error:" + path)
        key = path.replace("%23", "#")
        return key

    @classmethod
    def keyToPath(cls, key) -> str:
        path = key
        path = path.replace("#", "%23")
        path = "dictionary/" + path
        return path

    @classmethod
    def getAddr(cls, path, header) -> str:
        addr = BeautifulSoup("<a href=\"/" + path.replace(".html", "") + "\">"+ header +"</a>", 'html.parser')
        return str(addr)

    @classmethod
    def headerToKey(cls, header) -> str:
        key = header.replace(" ", "_").capitalize()
        return key        

    @classmethod
    def headerToPath(cls, header) -> str: 
        return cls.keyToPath(cls.headerToKey(header))           