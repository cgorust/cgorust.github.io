from lib.singleton import Singleton
from page.sitemapPages import SitemapPages
from page.wordPage import WordPage
from model.path import Path

import glob
import os
from dateutil import parser
from datetime import datetime

class Data(object, metaclass=Singleton):
    dictionary = {}

    def __init__(self):
        self.populateDictionary()
        self.checkDictionary()
        self.populateSitemap()
        #self.changeRelations()
        print("Data loaded")

    def populateSitemap(self):
        file = SitemapPages("sitemap_index.xml")
        wordTimes = file.getWordTimes()
        for wt in wordTimes:
            pathHeader = wt[0]
            time = wt[1]
            if pathHeader not in self.dictionary:
                print("sitemap path not exist " + pathHeader)
            else:
                self.dictionary[pathHeader].Time = parser.parse(time)   

    def checkDictionary(self):
        for key in self.dictionary:
            if self.dictionary[key].SuperConcepts == [] and \
                self.dictionary[key].SuperCategories == []:
                #print("error neither superConcept nor superCategory: " + key)
                #!!! need investigate
                pass
            for superConcept in self.dictionary[key].SuperConcepts:
                 superConceptKey = Path.headerToKey(superConcept)   
                 if superConceptKey not in self.dictionary:
                    print("error key cannot find superConcept: " + key + ";" + superConcept)
                    pass
                 else:   
                    find = False
                    for subConcept in self.dictionary[superConceptKey].SubConcepts:
                        if Path.headerToKey(subConcept) == key:
                            find = True
                    if find == False:
                        print("error path superConcept has no related subConcept: "
                            + key + "," + superConcept)
                        pass
            for subConcept in self.dictionary[key].SubConcepts:
                 subConceptKey = Path.headerToKey(subConcept)   
                 if subConceptKey not in self.dictionary:
                    print("error key cannot find subConcept: " + key + ";" + subConcept)
                    pass
                 else:   
                    find = False
                    for superConcept in self.dictionary[subConceptKey].SuperConcepts:
                        if Path.headerToKey(superConcept) == key:
                            find = True
                    if find == False:
                        print("error path subConcept has no related superConcept: "
                            + key + "," + subConcept)
                        pass
            for superCategory in self.dictionary[key].SuperCategories:
                 superCategoryKey = Path.headerToKey(superCategory)   
                 if superCategoryKey not in self.dictionary:
                    print("error key cannot find superCategory: " + key + ";" + superCategory)
                    pass
                 else:   
                    find = False
                    for subCategory in self.dictionary[superCategoryKey].SubCategories:
                        if Path.headerToKey(subCategory) == key:
                            find = True
                    if find == False:
                        print("error path superCategory has no related subcategory: "
                            + key + "," + subCategory)
                        pass
            for subCategory in self.dictionary[key].SubCategories:
                 subCategoryKey = Path.headerToKey(subCategory)   
                 if subCategoryKey not in self.dictionary:
                    print("error key cannot find subCategory: " + key + ";" + subCategory)
                    pass
                 else:   
                    find = False
                    for superCategory in self.dictionary[subCategoryKey].SuperCategories:
                        if Path.headerToKey(superCategory) == key:
                            find = True
                    if find == False:
                        print("error path subCagetory has no related superCategory: "
                            + key + "," + subCategory)
                        pass
                        #self.dictionary[key].SubCategories.remove(subCategory)
                        #newPage = WordPage("dictionary/" + key + ".html")
                        #newPage.applyNewTemplate(self.dictionary[key])
                        #newPage.save()                            


    def populateDictionary(self):
        applyTemplate = True
        files = glob.iglob("dictionary/**", recursive=True)
        files = [f for f in files if os.path.isfile(f)]
        for path in files:
            page = WordPage(path)
            word = page.getWord()
            key = Path.headerToKey(word.Header)
            if key != Path.pathToKey(path):
                print("Path and header is not match. Path: " + path + "; header: " + word.Header)
                #os.replace(path, "dictionary/"+ page.headerToPath(header) + ".html")
            self.dictionary[key]=word
            self.dictionary[key].Time = datetime.now()
            if applyTemplate:
                applyTemplate = page.applyNewTemplate(self.dictionary[key])
                page.save()

    def changeRelations(self):
        files = glob.iglob("dictionary/**", recursive=True)
        files = [f for f in files if os.path.isfile(f)]
        for path in files:
            page = WordPage(path)
            word = page.getWord()
            key = Path.headerToKey(word.Header)
            
            self.checkRelations(word)
            self.dictionary[key] = word
            page.applyNewTemplate(self.dictionary[key])
            page.save()


    def checkRelations(self, word):
        superConcepts = []
        for superConcept in word.SuperConcepts:
                superConceptKey = Path.headerToKey(superConcept)   
                superConcepts.append(self.dictionary[superConceptKey].Header)
        word.SuperConcepts = superConcepts      

        superCategories = []
        for superCategory in word.SuperCategories:
                superCategoryKey = Path.headerToKey(superCategory)   
                superCategories.append(self.dictionary[superCategoryKey].Header)
        word.SuperCategories = superCategories      

        subConcepts = []
        for subConcept in word.SubConcepts:
                subConceptKey = Path.headerToKey(subConcept)   
                subConcepts.append(self.dictionary[subConceptKey].Header)
        word.SubConcepts = subConcepts      

        subCategories = []
        for subCategory in word.SubCategories:
                subCategoryKey = Path.headerToKey(subCategory)   
                subCategories.append(self.dictionary[subCategoryKey].Header)
        word.SubCategories = subCategories   


    def checkWordPage(self, path):
        page = WordPage(path)
        word = page.getWord()
        key = Path.headerToKey(word.Header)
        if key not in self.dictionary:
            print("page is not cached:" + path)
            return
        if self.dictionary[key].Content != word.Content or \
            self.dictionary[key].SubConcepts != word.SubConcepts or \
            self.dictionary[key].SubCategories != word.SubCategories or \
            self.dictionary[key].SubConcepts != word.SubConcepts or \
            self.dictionary[key].SubCategories != word.SubCategories:
            print("page content is diffrent from cache" + path)
            return 

            
