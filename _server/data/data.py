from re import I
from lib.singleton import Singleton
from page.sitemapPages import SitemapPages
from page.indexPage import IndexPage
from page.wordPage import WordPage
from model.path import Path
from model.word import Word
from model.config import SITE, SITEMAP

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
        print("Data loaded")
        #self.generateSitemap()
        self.generateIndexPage()

    def checkWord(self, word: Word):
        if word.SuperConcepts == [] and word.SuperCategories == []:
            #print("error: {} has neither superConcept nor superCategory".format(word.Header))
            pass
        for relation in word.SuperConcepts:
            key = Path.headerToKey(relation)   
            if key not in self.dictionary:
                print("error: {}'s link {} not in dictionary".format(word.Header, relation))
                pass
            elif word.Header not in self.dictionary[key].SubConcepts:
                print("error: {}'s link '{}' does not point back".format(word.Header, relation))
        for relation in word.SubConcepts:
            key = Path.headerToKey(relation)   
            if key not in self.dictionary:
                print("error: {}'s link {} not in dictionary".format(word.Header, relation))
                pass
            elif word.Header not in self.dictionary[key].SuperConcepts:
                print("error: {}'s link '{}' does not point back".format(word.Header, relation))
        for relation in word.SuperCategories:
            key = Path.headerToKey(relation)   
            if key not in self.dictionary:
                print("error: {}'s link {} not in dictionary".format(word.Header, relation))
                pass
            elif word.Header not in self.dictionary[key].SubCategories:
                print("error: {}'s link '{}' does not point back".format(word.Header, relation))
        for relation in word.SubCategories:
            key = Path.headerToKey(relation)   
            if key not in self.dictionary:
                print("error: {}'s link {} not in dictionary".format(word.Header, relation))
                pass
            elif word.Header not in self.dictionary[key].SuperCategories:
                print("error: {}'s link '{}' does not point back".format(word.Header, relation))


    def checkDictionary(self):
        for key in self.dictionary:
            self.checkWord(self.dictionary[key])

    def populateDictionary(self):
        applyTemplate = True
        files = glob.iglob("dictionary/**", recursive=True)
        files = [f for f in files if os.path.isfile(f)]
        for path in files:
            page = WordPage(path)
            word = page.getWord()
            key = Path.headerToKey(word.Header)
            if key != Path.pathToKey(path):
                print("error: Path {} and header {} is not match".format(path, word.Header))
            self.dictionary[key]=word
            self.dictionary[key].Time = datetime.now()
            if applyTemplate:
                applyTemplate = page.applyNewTemplate(self.dictionary[key])
                page.save()


    def populateSitemap(self):
        file = SitemapPages("sitemap_index.xml")
        wordTimes = file.getWordTimes()
        for wt in wordTimes:
            key = wt[0]
            time = wt[1]
            if key not in self.dictionary:
                print("sitemap path not exist: " + key)
            else:
                self.dictionary[key].Time = parser.parse(time)   

    def sortByTime(self, li):  
        # key is set to sort using second element of 
        # sublist lambda has been used
        li.sort(key = lambda x: x[1], reverse = True)
        return li

    def getDictWordTimes(self) -> list:
        wordTimes = []
        for key in self.dictionary:
            time = self.dictionary[key].Time.strftime("%Y-%m-%d")
            path = Path.keyToPath(key).replace(".html", "")
            wordTimes.append((path, time))
        wordTimes = self.sortByTime(wordTimes)
        return wordTimes

    def getDictHeaderTimes(self) -> list:
        headerTimes = []
        for key in self.dictionary:
            time = self.dictionary[key].Time.strftime("%Y-%m-%d")
            header = self.dictionary[key].Header
            headerTimes.append((header, time))
        headerTimes = self.sortByTime(headerTimes)
        return headerTimes

    def generateIndexPage(self):
        headerTimes = self.getDictHeaderTimes()
        addrs = ""
        first = True
        for ht in headerTimes:
            h = ht[0]
            if first:
                first = False
            else:
                addrs+=",    "
            addrs += Path.getAddr(h)
        page = IndexPage("index.html")    
        page.generate(addrs)
        page.save()

    def checkWordPage(self, path):
        page = WordPage(path)
        word = page.getWord()
        key = Path.headerToKey(word.Header)
        if key not in self.dictionary:
            print("page %s is not cached", path)
            return
        if self.dictionary[key].Content != word.Content or \
            self.dictionary[key].SubConcepts != word.SubConcepts or \
            self.dictionary[key].SubCategories != word.SubCategories or \
            self.dictionary[key].SubConcepts != word.SubConcepts or \
            self.dictionary[key].SubCategories != word.SubCategories:
            print("page %s content is diffrent from cache", path)
            return 

            
