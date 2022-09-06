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

      