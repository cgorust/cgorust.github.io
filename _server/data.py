from singleton import Singleton
from file import File

from bs4 import BeautifulSoup
import difflib
import glob
import os

class Data(object, metaclass=Singleton):
    dictionary = {}

    def __init__(self):
        self.wordPageTemplate = File().getHTML("_server/template/wordPage.html")
        self.populateDictionary()
        print("data populated")

    def headerToPath(self, header):
        return header.replace(" ", "_").capitalize()

    def populateDictionary(self):
        for path in glob.iglob("dictionary/*.html", recursive=True):
            header, content, superConcepts, superCategories, subConcepts, subCategories = self.getWord(path)
            self.dictionary[header] = {}
            if self.headerToPath(header) != path.replace("dictionary/", "").replace(".html", ""):
                print("Path and header not match: " + path + ", " + header)
                #os.replace(path, "dictionary/"+ self.headerToPath(header) + ".html")
            self.dictionary[header]["content"]=content
            self.dictionary[header]["superConcepts"]=superConcepts
            self.dictionary[header]["superCategories"]=superCategories
            self.dictionary[header]["subConcepts"]=subConcepts
            self.dictionary[header]["subCategories"]=subCategories

    def getWord(self, path):
        file = File().getHTML(path)
        header = file.find("div", {"id": "dict_container"}).findChildren("h1", recursive=False)[0].getText()
        content = file.find("pre", {"id": "word_content"}).getText()
        superConcepts = file.find_all("b", text="Superconcept: ")
        if superConcepts!= []:
            superConcepts=[x.getText() for x in superConcepts[0].findNextSiblings("a", recursive=False)]
        superCategories = file.find_all("b", text="Supercategory: ")
        if superCategories!= []:
            superCategories=[x.getText() for x in superCategories[0].findNextSiblings("a", recursive=False)]
        subConcepts = file.find_all("b", text="Subconcept: ")
        if subConcepts!= []:
            subConcepts=[x.getText() for x in subConcepts[0].findNextSiblings("a", recursive=False)]
        subCategories = file.find_all("b", text="Subcategory: ")
        if subCategories!= []:
            subCategories=[x.getText() for x in subCategories[0].findNextSiblings("a", recursive=False)]
        return [header, content, superConcepts, superCategories, subConcepts, subCategories]

    def diffWordPageTemplate(self, page):
        File().diffFile(str(self.wordPageTemplate), str(page)) 

    def checkWordPage(self, path):
        if path[0]=='/':
            path = path[1:]

        header, content, superConcepts, superCategories, subConcepts, subCategories = self.getWord(path)
        if not header in self.dictionary:
            print("page is not in memory!")
            return
        if  self.dictionary[header]["content"]!=content or \
            self.dictionary[header]["superConcepts"]!=superConcepts  or \
            self.dictionary[header]["superCategories"]!=superCategories  or \
            self.dictionary[header]["subConcepts"]!=subConcepts  or \
            self.dictionary[header]["subCategories"]!=subCategories:
            print("page content wrong!")
            return 

            
