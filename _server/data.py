from singleton import Singleton
from file import File

from bs4 import BeautifulSoup
import glob
import copy

class Data(object, metaclass=Singleton):
    dictionary = {}

    def __init__(self):
        self.wordPageTemplate = File().getHTML("_server/template/wordPage.html")
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
                print("Path and header not match: " + path + ", " + header)
                #os.replace(path, "dictionary/"+ self.headerToPath(header) + ".html")
            self.dictionary[header]["content"]=content
            if superConcepts != None:
                self.dictionary[header]["superConcepts"]=superConcepts
            if superCategories != None:
                self.dictionary[header]["superCategories"]=superCategories
            if subConcepts != None:
                self.dictionary[header]["subConcepts"]=subConcepts
            if subCategories != None:
                self.dictionary[header]["subCategories"]=subCategories
            if apply:
                newFile = self.applyNewTemplate(header)
                if str(file) == str(newFile):
                    print("template has no change")
                    apply = False
                else:
                    f = open(path, "w")
                    f.write(str(newFile))
                    f.close()        


    def getAddr(self, header):
        return BeautifulSoup("<a href=\"/dictionary/" + self.headerToPath(header) + "\">"+ header +"</a>", 'html.parser')

    def applyNewTemplate(self, header):
        file = copy.deepcopy(self.wordPageTemplate)
        file.find("div", {"id": "dict_container"}).find("h1").find("span").string=header
        file.find("pre", {"id": "word_content"}).string=self.dictionary[header]["content"]
        superConcepts = file.find("b", text="Superconcept: ").parent
        if self.dictionary[header]["superConcepts"] != []:
            first = True
            for x in self.dictionary[header]["superConcepts"]:
                if first:
                    first = False
                else:
                    superConcepts.append(", ")    
                superConcepts.append(self.getAddr(x)) 
        else:
            superConcepts.attrs["hidden"]=None  
        superCategories = file.find("b", text="Supercategory: ").parent
        if self.dictionary[header]["superCategories"] != []:
            first = True
            for x in self.dictionary[header]["superCategories"]:
                if first:
                    first = False
                else:
                    superCategories.append(", ")    
                superCategories.append(self.getAddr(x)) 
        else:
            superCategories.attrs["hidden"]=None  
        subConcepts = file.find("b", text="Subconcept: ").parent
        if self.dictionary[header]["subConcepts"] != []:
            first = True
            for x in self.dictionary[header]["subConcepts"]:
                if first:
                    first = False
                else:
                    subConcepts.append(", ")    
                subConcepts.append(self.getAddr(x)) 
        else:
            subConcepts.attrs["hidden"]=None  
        subCategories = file.find("b", text="Subcategory: ").parent
        if self.dictionary[header]["subCategories"] != []:
            first = True
            for x in self.dictionary[header]["subCategories"]:
                if first:
                    first = False
                else:
                    subCategories.append(", ")    
                subCategories.append(self.getAddr(x)) 
        else:
            subCategories.attrs["hidden"]=None  
        return file

    def getRelations(self, file, relationName):
        relations = file.find("b", text=relationName)
        if relations!= None:
            relations=[x.getText() for x in relations.findNextSiblings("a", recursive=False)]
        else:
            relations=[]
        return relations

    def getWord(self, path):
        file = File().getHTML(path)
        #print(path)
        header = file.find("div", {"id": "dict_container"}).find("h1").find("span").getText()
        content = file.find("pre", {"id": "word_content"}).getText()
        superConcepts = self.getRelations(file, "Superconcept: ")
        superCategories = self.getRelations(file, "Supercategory: ")
        subConcepts = self.getRelations(file, "Subconcept: ")
        subCategories = self.getRelations(file, "Subcategory: ")
        return [file, header, content, superConcepts, superCategories, subConcepts, subCategories]

    def checkWordPage(self, path):
        if path[0]=='/':
            path = path[1:]

        _, header, content, superConcepts, superCategories, subConcepts, subCategories = self.getWord(path)
        if header not in self.dictionary:
            print("page is not in cache")
            return
        if self.dictionary[header]["content"] != content or \
            self.dictionary[header]["superConcepts"] != superConcepts  or \
            self.dictionary[header]["superCategories"] != superCategories  or \
            self.dictionary[header]["subConcepts"] != subConcepts  or \
            self.dictionary[header]["subCategories"] != subCategories:
            print("page content is not the same as in cache")
            return 

            
