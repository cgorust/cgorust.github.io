from page.page import Page

import copy
from bs4 import BeautifulSoup

class WordPage(Page):
    template = {}

    def __init__(self, path):
        super().__init__(path)
        type(self).template = Page("_server/template/page.html")
        type(self).template.find("main").append(Page("_server/template/word.html").getRoot())

    def getHeaderNode(self):
        return self.page.find("div", {"id": "dict_container"}).find("h1").find("span")           

    def getContentNode(self):
        return self.page.find("pre", {"id": "word_content"})          

    def getRelationNode(self, relationName):
        return self.page.find("b", text = relationName)         

    def getRelations(self, relationName):
        relationNodes = self.page.getRelationNode(relationName)
        relations = []
        if relationNodes != None:
            relations = [r.getText() for r in relationNodes.findNextSiblings("a", recursive = False)]
        return relations

    def setRelations(self, relationName, relationStr): 
        relationNode = self.page.getRelationNode(relationName).parent
        if relationStr != "":
            relationNode.append(BeautifulSoup(relationStr)) 
        else:
            relationNode.attrs["hidden"]=None  

    def getWord(self):
        word = {}
        word["Header"] = self.getHeaderNode().getText()
        word["Content"] = self.getContentNode().getText()
        word["Superconcept"] = self.getRelations("Superconcept: ")
        word["Supercategory"] = self.getRelations("Supercategory: ")
        word["Subconcept"] = self.getRelations("Subconcept: ")
        word["Subcategory"] = self.getRelations("Subcategory: ")
        return word

    def applyNewTemplate(self, word):
        oldText = str(self.file)    

        self.file = copy.deepcopy(self.wordPageTemplate)
        self.getHeaderNode().string=word["Header"]
        self.getContentNode().string=word["Content"]
        self.setRelation("Superconcept", word["Superconcept"])
        self.setRelation("Supercategory", word["Supercategory"])
        self.setRelation("Subconcept", word["Subconcept"])
        self.setRelation("Subcategory", word["Subcategory"])
        newText = str(self.file)
        if oldText != newText:
            return False
        return True    

    def headerToAddr(self, header):
        addr = BeautifulSoup("<a href=\"/dictionary/" + self.headerToPath(header) + "\">"+ header +"</a>", 'html.parser')
        return str(addr)

    def setRelation(self, relationName, relations):
        relationStr = ""
        if relations != []:
            first = True
            for r in relations:
                if first:
                    first = False
                else:
                    relationStr.append(", ")    
                relationStr.append(self.urlEscape(self.headerToAddr(r))) 
 
        self.setRelations(relationName+ ": ", relationStr)        