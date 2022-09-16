from model.path import Path

from bs4 import BeautifulSoup

class Word(object):
    __slots__ = (
        "Key"
        , "Header"
        , "Content"
        , "SuperConcepts"
        , "SuperCategories"
        , "SubConcepts"
        , "SubCategories"
        , "Time"
    )
    
    def __init__(self, path: str, header: str, content: str, 
            superConcepts: list, superCategories: list, subConcepts: list, subCategories: list):
        self.Key = Path.pathToKey(path)
        self.Header = header
        self.Content = content
        self.SuperConcepts = superConcepts
        self.SuperCategories = superCategories
        self.SubConcepts = subConcepts
        self.SubCategories = subCategories
        self.Time = None

