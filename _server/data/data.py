from page.sitemapPages import SitemapPages
from lib.singleton import Singleton
from page.wordPage import WordPage

import glob
import os
from dateutil import parser
from datetime import datetime

class Data(object, metaclass=Singleton):
    dictionary = {}

    def __init__(self):
        self.populateDictionary()
        self.checkDictionary()
        self.getSitemap()

    def headerToPath(self, header):
        return header.replace(" ", "_").capitalize()

    def urlEscape(self, path):
        return path.replace("#", "%23")

    def getSitemap(self):
        file = SitemapPages("sitemap_index.xml")
        wordTimes = file.getWordTimes()
        for wt in wordTimes:
            pathHeader = wt[0]
            time = wt[1]
            if pathHeader not in self.dictionary:
                print("sitemap path not exist " + pathHeader)
            else:
                self.dictionary[pathHeader]["Time"] = parser.parse(time)   

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
                    pass
                 else:   
                    find = False
                    for subConcept in self.dictionary[superConceptPath]["Subconcept"]:
                        if self.headerToPath(subConcept) == pathHeader:
                            find = True
                    if find == False:
                        print("error path superConcpet has no related subconcept: "
                            + pathHeader + "," + superConcept)
                        pass
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
                        #newPage = Page("dictionary/" + pathHeader + ".html")
                        #newPage.applyNewTemplate(self.dictionary[pathHeader])
                        #newPage.save()
                        pass

    def pathToKey(self, path):
        return path.replace("dictionary/", "").replace(".html", "")

    def populateDictionary(self):
        applyTemplate = True
        files = glob.iglob("dictionary/**", recursive=True)
        files = [f for f in files if os.path.isfile(f)]
        for path in files:
            page = WordPage(path)
            word = page.getWord()
            pathHeader = self.headerToPath(word["header"])
            self.dictionary[pathHeader] = {}
            if pathHeader != self.pathToKey(path):
                print("Path and header is not match. Path: " + path + "; header: " + word["header"])
                #os.replace(path, "dictionary/"+ self.headerToPath(header) + ".html")
            self.dictionary[pathHeader]["Header"]=word["Header"]
            self.dictionary[pathHeader]["Content"]=word["Content"]
            self.dictionary[pathHeader]["Superconcept"]=word["Superconcept"]
            self.dictionary[pathHeader]["Supercategory"]=word["Supercategory"]
            self.dictionary[pathHeader]["Subconcept"]=word["Subconcept"]
            self.dictionary[pathHeader]["Subcategory"]=word["Subcategory"]
            self.dictionary[pathHeader]["Time"] = datetime.now()

            if applyTemplate:
                applyTemplate = page.applyNewTemplate()
                page.save()

    def checkWordPage(self, path):
        word = WordPage(path).getWord()
        pathHeader = self.headerToPath(word["header"])
        if pathHeader not in self.dictionary:
            print("page is not cached:" + path)
            return
        if self.dictionary[pathHeader]["Content"] != word["content"] or \
            self.dictionary[pathHeader]["Superconcept"] != word["superConcepts"]  or \
            self.dictionary[pathHeader]["Supercategory"] != word["superCategories"]  or \
            self.dictionary[pathHeader]["Subconcept"] != word["subConcepts"]  or \
            self.dictionary[pathHeader]["Subcategory"] != word["subCategories"]:
            print("page content is diffrent from cache" + path)
            return 

            
