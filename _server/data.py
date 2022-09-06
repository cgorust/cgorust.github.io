from singleton import Singleton
from file import File

from bs4 import BeautifulSoup
import glob
import copy
from urllib.parse import unquote
import os
from dateutil import parser
from datetime import datetime

class Data(object, metaclass=Singleton):
    dictionary = {}

    def __init__(self):
        self.indexPageTemplate = File().getHTML("_server/template/page.html")
        self.wordPageTemplate = copy.deepcopy(self.indexPageTemplate)
        self.wordPageTemplate.find("main").append(File().getHTML("_server/template/word.html"))

        self.populateDictionary()
        self.checkDictionary()
        self.getSitemap()
        print("data populated")

    def headerToPath(self, header):
        return header.replace(" ", "_").capitalize()


    def getSitemap(self):
        file = File().getHTML("sitemap_index.xml")
        sitemaps = File().getSitemaps(file)
        for s in sitemaps:
            path = s.replace("https://cgorust.com/", "")
            file = File().getHTML(path)
            wordTimes = File().getWordTimes(file)
            for wt in wordTimes:
                pathHeader = unquote(wt[0].replace("https://cgorust.com/dictionary/", ""))
                time = wt[1]
                if pathHeader not in self.dictionary:
                    print("sitemap path not exist " + pathHeader)
                else:
                    self.dictionary[pathHeader]["time"] = parser.parse(time)   
                    #print(pathHeader + ":" + time) 

    def checkDictionary(self):
        for pathHeader in self.dictionary:
            if self.dictionary[pathHeader]["Superconcept"] == [] and \
                self.dictionary[pathHeader]["Supercategory"] == []:
                #print("error pathHeader no superConcept and superCategory: " + pathHeader)
                #!!! need investigate
                pass
            for superConcept in self.dictionary[pathHeader]["Superconcept"]:
                 superConceptPath = self.headerToPath(superConcept)   
                 if superConceptPath not in self.dictionary:
                    print("error pathHeader cannot find superConcept: " + pathHeader + ";" + superConcept)
                 else:   
                    find = False
                    for subConcept in self.dictionary[superConceptPath]["Subconcept"]:
                        if self.headerToPath(subConcept) == pathHeader:
                            find = True
                    if find == False:
                        if "<" not in pathHeader:
                            pass
                            #print("error path superConcpet has no related subconcept: "
                            #    + pathHeader + "," + superConcept)
            for superCategory in self.dictionary[pathHeader]["Supercategory"]:
                 superCategoryPath = self.headerToPath(superCategory)   
                 if superCategoryPath not in self.dictionary:
                    print("error pathHeader cannot find superCategory: " + pathHeader + ";" + superCategory)
                    pass
                 else:   
                    find = False
                    for subCategory in self.dictionary[superCategoryPath]["Subcategory"]:
                        if self.headerToPath(subCategory) == pathHeader:
                            find = True
                    if find == False:
                        print("error path superCategory has no related subcategory: "
                            + pathHeader + "," + subCategory)

                        self.dictionary[pathHeader]["Supercategory"].remove(superCategory)
                        path = "dictionary/" + pathHeader + ".html"
                        newFile = self.applyNewTemplate(self.dictionary[pathHeader]["Header"])
                        #f = open(path, "w")
                        #f.write(str(newFile))
                        #f.close()                             
                        pass

    def populateDictionary(self):
        apply = True
        files = glob.iglob("dictionary/**", recursive=True)
        files = [f for f in files if os.path.isfile(f)]
        for path in files:
            file, header, content, superConcepts, superCategories, subConcepts, subCategories = self.getWord(path)
            pathHeader = self.headerToPath(header)
            self.dictionary[pathHeader] = {}
            if pathHeader != path.replace("dictionary/", "").replace(".html", ""):
                print("Path and header is not match. Path: " + path + "; header: " + header)
                #os.replace(path, "dictionary/"+ self.headerToPath(header) + ".html")

            self.dictionary[pathHeader]["Header"]=header
            self.dictionary[pathHeader]["Content"]=content
            self.dictionary[pathHeader]["Superconcept"]=superConcepts
            self.dictionary[pathHeader]["Supercategory"]=superCategories
            self.dictionary[pathHeader]["Subconcept"]=subConcepts
            self.dictionary[pathHeader]["Subcategory"]=subCategories
            self.dictionary[pathHeader]["time"] = datetime.now()
            if apply:
                newFile = self.applyNewTemplate(header)
                if str(file) == str(newFile):
                    print("Template did no change")
                    apply = False
                else:
                    f = open(path, "w")
                    f.write(str(newFile))
                    f.close()        


    def headerToAddr(self, header):
        return BeautifulSoup("<a href=\"/dictionary/" + self.headerToPath(header) + "\">"+ header +"</a>", 'html.parser')

    def setRelation(self, file, relationName, header):
        relations = File().getRelationNode(file, relationName+ ": ").parent
        #print(self.dictionary[header])
        pathHeader = self.headerToPath(header)
        if self.dictionary[pathHeader][relationName] != []:
            first = True
            for r in self.dictionary[pathHeader][relationName]:
                if first:
                    first = False
                else:
                    relations.append(", ")    
                relations.append(self.headerToAddr(r)) 
        else:
            relations.attrs["hidden"]=None  

    def applyNewTemplate(self, header):
        file = copy.deepcopy(self.wordPageTemplate)
        File().getHeaderNode(file).string=header
        pathHeader = self.headerToPath(header)
        File().getContentNode(file).string=self.dictionary[pathHeader]["Content"]
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
        path = unquote(path)

        _, header, content, superConcepts, superCategories, subConcepts, subCategories = self.getWord(path)
        pathHeader = self.headerToPath(header)
        if pathHeader not in self.dictionary:
            print("page is not in cache")
            return
        if self.dictionary[pathHeader]["Content"] != content or \
            self.dictionary[pathHeader]["Superconcept"] != superConcepts  or \
            self.dictionary[pathHeader]["Supercategory"] != superCategories  or \
            self.dictionary[pathHeader]["Subconcept"] != subConcepts  or \
            self.dictionary[pathHeader]["Subcategory"] != subCategories:
            print("page content is not the same as in cache")
            return 

            
