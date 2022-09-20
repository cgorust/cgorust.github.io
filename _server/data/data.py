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
import difflib
import shutil

class Data(object, metaclass=Singleton):
    dictionary = {}

    def __init__(self):
        self.populateDictionary()
        self.checkDictionary()
        print("Data loaded")
        self.populateSitemap()
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
        wordTimes = self.getDictWordTimes()        
        file.generateSitemap(wordTimes)         

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
            addrs+="<span>"
            h = ht[0]
            if first:
                first = False
            else:
                addrs+=",&ensp;"
            addrs += Path.getAddr(h)
            addrs+="</span>"
        page = IndexPage("index.html")    
        page.generate(addrs)
        page.save()

    def checkWordPage(self, path):
        page = WordPage(path)
        word = page.getWord()
        key = Path.headerToKey(word.Header)
        if Path.headerToKey(word.Header) != key:
            print("Error header path mismatch. header " + word.Header + ", key " + key)
        if key not in self.dictionary:
            print("page %s is not cached", path)
            return
        if self.dictionary[key].Content != word.Content or \
            self.dictionary[key].SubConcepts != word.SubConcepts or \
            self.dictionary[key].SubCategories != word.SubCategories or \
            self.dictionary[key].SuperConcepts != word.SuperConcepts or \
            self.dictionary[key].SuperCategories != word.SuperCategories:
            print("page %s content is diffrent from cache", path)
            return 

    def get_close_matches_icase(self, word, possibilities, *args, **kwargs):
        """ Case-insensitive version of difflib.get_close_matches """
        lword = word.lower()
        lpos = {p.lower(): p for p in possibilities}
        lmatches = difflib.get_close_matches(lword, lpos.keys(), *args, **kwargs)
        return [lpos[m] for m in lmatches]
            
    def getDictWords(self, lookup:str) -> str:
        words = []
        for key in self.dictionary:
            words.append(self.dictionary[key].Header)
        
        words = self.get_close_matches_icase(lookup, words, n=10, cutoff=0.4)
        if(len(words)>0):
            if(words[0] == lookup):
                words[0]="<b>" + words[0] + "</b>"
        return "<br>".join(words)


    def checkSaveWord(self, path, main):
        errorMsg = ""
        error = False
        page = WordPage(path, main)
        word = page.getWord()
        word = page.stripWord(word)
        key = Path.headerToKey(word.Header)
        key = key.strip()
        if key == "":
            errorMsg += "Header is empty.<br>"
            error = True
        if word.Content.strip() == "":
            errorMsg += "Content is empty.<br>"
            error = True


        for header in  word.SuperConcepts:
            if Path.headerToKey(header) not in self.dictionary:
                errorMsg += "SuperConcept {} is not in dictionary.<br>".format(header)
                error = True
        for header in  word.SuperCategories:
            if Path.headerToKey(header) not in self.dictionary:
                errorMsg += "SuperCategory {} is not in dictionary.<br>".format(header)
                error = True
        for header in  word.SubConcepts:
            if Path.headerToKey(header) not in self.dictionary:
                errorMsg += "SubConcept {} is not in dictionary.<br>".format(header)
                error = True
        for header in  word.SubCategories:
            if Path.headerToKey(header) not in self.dictionary:
                errorMsg += "SubCategory {} is not in dictionary.<br>".format(header)
                error = True

        if error == True:
            if key not in self.dictionary:
                errorMsg += "header {} is not in dictionary.<br>".format(word.Header)
            return (error, errorMsg)

        return self.saveWord(word)


    def saveWord(self, word):
        errorMsg = ""
        error = False
        key = Path.headerToKey(word.Header)
        if key not in self.dictionary:
            [error, errorMsg] = self.createWord(word)
        else:
            [error, errorMsg] = self.updateWord(word)

        return (error, errorMsg)        

    def createWord(self, word):
        errorMsg = ""
        error = False

        key = Path.headerToKey(word.Header)
        if key in self.dictionary:
            errorMsg += "Cannot create new word. Header {} is in dictionary.<br>".format(word.Header)
            error = True
            return (error, errorMsg)

        for header in  word.SuperConcepts:
            relatedKey = Path.headerToKey(header)
            if self.dictionary[relatedKey].SubConcepts.count(key) == 0: 
                self.dictionary[relatedKey].SubConcepts.append(key)
                page = WordPage("dictionary/" + relatedKey + ".html")
                page.applyNewTemplate(self.dictionary[relatedKey])
                page.save()

        for header in  word.SuperCategories:
            relatedKey = Path.headerToKey(header)
            if self.dictionary[relatedKey].SubConcepts.count(key) == 0: 
                self.dictionary[relatedKey].SubCategories.append(key)
                page = WordPage("dictionary/" + relatedKey + ".html")
                page.applyNewTemplate(self.dictionary[relatedKey])
                page.save()

        for header in  word.SubConcepts:
            relatedKey = Path.headerToKey(header)
            if self.dictionary[relatedKey].SubConcepts.count(key) == 0: 
                self.dictionary[relatedKey].SuperConcepts.append(key)
                page = WordPage("dictionary/" + relatedKey + ".html")
                page.applyNewTemplate(self.dictionary[relatedKey])
                page.save()

        for header in  word.SubCategories:
            relatedKey = Path.headerToKey(header)
            if self.dictionary[relatedKey].SubConcepts.count(key) == 0: 
                self.dictionary[relatedKey].SuperCategories.append(key)
                page = WordPage("dictionary/" + relatedKey + ".html")
                page.applyNewTemplate(self.dictionary[relatedKey])
                page.save()


        self.dictionary[key] = word
        path = "dictionary/" + key + ".html"
        shutil.copyfile("_server/template/page.html", path)
        page = WordPage(path)
        page.applyNewTemplate(self.dictionary[key])
        page.save()
        
        return (error, errorMsg)        

    def updateWord(self, word):
        errorMsg = ""
        error = False

        return (error, errorMsg)        
        