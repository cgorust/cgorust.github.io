from singleton import Singleton
from file import File

from bs4 import BeautifulSoup
import glob
import copy

class Data(object, metaclass=Singleton):
    dictionary = {}

    def __init__(self):
        self.indexPageTemplate = File().getHTML("_server/template/page.html")
        self.wordPageTemplate = copy.deepcopy(self.indexPageTemplate)
        self.wordPageTemplate.find("main").append(File().getHTML("_server/template/word.html"))

        self.populateDictionary()
        print("data populated")

    def headerToPath(self, header):
        return header.replace(" ", "_").capitalize()

    def populateDictionary(self):
        apply = True
        for path in glob.iglob("dictionary/*.html", recursive=True):
            file, header, content, superConcepts, superCategories, subConcepts, subCategories = self.getWord(path)
            self.dictionary[header] = {}
            if self.headerToPath(header) != path.replace("dictionary/", "").replace(".html", ""):
                print("Path and header is not match. Path: " + path + "; header: " + header)
                #os.replace(path, "dictionary/"+ self.headerToPath(header) + ".html")
            self.dictionary[header]["Content"]=content
            self.dictionary[header]["Superconcept"]=superConcepts
            self.dictionary[header]["Supercategory"]=superCategories
            self.dictionary[header]["Subconcept"]=subConcepts
            self.dictionary[header]["Subcategory"]=subCategories
            if apply:
                newFile = self.applyNewTemplate(header)
                if str(file) == str(newFile):
                    print("Template did no change")
                    apply = False
                else:
                    f = open(path, "w")
                    f.write(str(newFile))
                    f.close()        


    def getAddr(self, header):
        return BeautifulSoup("<a href=\"/dictionary/" + self.headerToPath(header) + "\">"+ header +"</a>", 'html.parser')

    def setRelation(self, file, relationName, header):
        relations = File().getRelationNode(file, relationName+ ": ").parent
        #print(self.dictionary[header])
        if self.dictionary[header][relationName] != []:
            first = True
            for r in self.dictionary[header][relationName]:
                if first:
                    first = False
                else:
                    relations.append(", ")    
                relations.append(self.getAddr(r)) 
        else:
            relations.attrs["hidden"]=None  

    def applyNewTemplate(self, header):
        file = copy.deepcopy(self.wordPageTemplate)
        File().getHeaderNode(file).string=header
        File().getContentNode(file).string=self.dictionary[header]["Content"]
        self.setRelation(file, "Superconcept", header)
        self.setRelation(file, "Supercategory", header)
        self.setRelation(file, "Subconcept", header)
        self.setRelation(file, "Subcategory", header)
        return file

    def getWord(self, path):
        file = File().getHTML(path)
        #print(path)
        header = File().getHeaderNode(file).getText()
        content = File().getContentNode(file).getText()
        superConcepts = File().getRelations(file, "Superconcept: ")
        superCategories = File().getRelations(file, "Supercategory: ")
        subConcepts = File().getRelations(file, "Subconcept: ")
        subCategories = File().getRelations(file, "Subcategory: ")
        return [file, header, content, superConcepts, superCategories, subConcepts, subCategories]

    def checkWordPage(self, path):
        if path[0]=='/':
            path = path[1:]

        _, header, content, superConcepts, superCategories, subConcepts, subCategories = self.getWord(path)
        if header not in self.dictionary:
            print("page is not in cache")
            return
        if self.dictionary[header]["Content"] != content or \
            self.dictionary[header]["Superconcept"] != superConcepts  or \
            self.dictionary[header]["Supercategory"] != superCategories  or \
            self.dictionary[header]["Subconcept"] != subConcepts  or \
            self.dictionary[header]["Subcategory"] != subCategories:
            print("page content is not the same as in cache")
            return 

            
