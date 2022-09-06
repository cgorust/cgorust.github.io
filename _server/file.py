from singleton import Singleton

from bs4 import BeautifulSoup
import difflib

class File(object, metaclass=Singleton):
    def getHTML(self, path):
        with open(path) as fp:
            return BeautifulSoup(fp, 'html.parser')

    def getHeaderNode(self, file):
        return file.find("div", {"id": "dict_container"}).find("h1").find("span")           

    def getContentNode(self, file):
        return file.find("pre", {"id": "word_content"})          

    def getRelationNode(self, file, relationName):
        return file.find("b", text= relationName)         

    def getRelations(self, file, relationName):
        relations = File().getRelationNode(file, relationName)
        if relations!= None:
            relations=[x.getText() for x in relations.findNextSiblings("a", recursive=False)]
        else:
            relations=[]
        return relations

    def getSitemaps(self, file):
        sitemaps = file.find_all("loc")
        urls = [x.getText() for x in sitemaps]
        return urls

    def getWordTimes(self, file):
        urls = file.find_all("url")
        wordTimes = []
        for url in urls:
            loc = url.find("loc").getText()
            lastmod = url.find("lastmod").getText()
            wordTimes.append((loc, lastmod))
        return wordTimes