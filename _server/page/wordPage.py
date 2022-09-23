from page.page import Page
from model.word import Word
from model.path import Path
from model.text import Text

import copy
from bs4 import BeautifulSoup

class WordPage(Page):
    template = {}

    count = 0

    def __init__(self, path, main =None):
        super().__init__(path)
        if type(self).template == {}:
            type(self).template = Page("_server/template/page.html")
            type(self).template.getRoot().find("main").append(Page("_server/template/word.html").getRoot())
        if main != None:
            self.getRoot().find("main").replaceWith(BeautifulSoup(main, 'html.parser'))

    def getHeaderNode(self):
        return self.page.find("div", {"id": "dict_container"}).find("h1").find("span")           

    def getContentNode(self):
        return self.page.find("pre", {"id": "word_content"})          

    def getRelationNode(self, relationName: str):
        return self.page.find("b", text = relationName)         

    def getRelations(self, relationName: str) -> list:
        relationName += ": "
        relationNodes = self.getRelationNode(relationName)
        relations = []
        if relationNodes != None:
            relations = [Text.htmlDecodeText(r.findChildren("a")[0].getText()) for r in relationNodes.findNextSiblings("span", recursive = False)]
        return relations

    def setRelations(self, relationName: str, relationStr: str): 
        relationName += ": "
        relationNode = self.getRelationNode(relationName).parent
        if relationStr != "":
            if relationNode.has_attr("hidden"):
                del relationNode["hidden"]
            relationNode.append(BeautifulSoup(relationStr, 'html.parser')) 
        else:
            if not relationNode.has_attr("hidden"):
                relationNode.attrs["hidden"]=None  

    def getWord(self) -> Word:
        content = ""
        texts = self.getContentNode().findAll(text=True, recursive=False)
        if len(texts) > 0:
            content = str(texts[0])
        contentNode = self.getContentNode()
        children = contentNode.findChildren("div" , recursive=False)
        for child in children:
            content = content + "\n" + str(child.contents[0])
        #content = "<p>" + content + "</p>"

        word = Word(self.path
            , Text.htmlDecodeText(self.getHeaderNode().getText())
            , content
            , self.getRelations("Superconcept")
            , self.getRelations("Supercategory")
            , self.getRelations("Subconcept")
            , self.getRelations("Subcategory")
        )
        return word


    def stripWord(self, word: Word) -> Word:
        word.Header = word.Header.strip()
        word.Key = Path.headerToKey(word.Header)
        word.Content = word.Content
        word.SubCategories[:]=[ i.strip() for i in word.SubCategories]
        word.SuperCategories[:]=[ i.strip() for i in word.SuperCategories]
        word.SubConcepts[:]=[ i.strip() for i in word.SubConcepts]
        word.SuperConcepts[:]=[ i.strip() for i in word.SuperConcepts]
        return word    

    def applyNewTemplate(self, word: Word) -> bool:
        oldText = str(self.page)    

        self.page = copy.deepcopy(type(self).template.getRoot())
        self.getHeaderNode().string=word.Header
        self.getContentNode().string=word.Content
        self.setRelation("Superconcept", word.SuperConcepts)
        self.setRelation("Supercategory", word.SuperCategories)
        self.setRelation("Subconcept", word.SubConcepts)
        self.setRelation("Subcategory", word.SubCategories)
        newText = str(self.page)
        if oldText != newText:
            return True
        return False    



    def setRelation(self, relationName: str, relations: list):
        relationStr = ""
        if relations != []:
            first = True
            for r in relations:
                relationStr +="<span>"
                if first == True:
                    first = False
                else:
                    relationStr += ",  "
                relationStr += Path.getAddr(r)
                relationStr +="</span>"
        self.setRelations(relationName, relationStr)        