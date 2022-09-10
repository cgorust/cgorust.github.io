from page.page import Page
from model.word import Word
from model.path import Path

import copy
from bs4 import BeautifulSoup

class IndexPage(Page):
    template = {}

    def __init__(self, path):
        super().__init__(path)
        if type(self).template == {}:
            type(self).template = Page("_server/template/page.html")


    def generate(self, words:str):
        self.page = copy.deepcopy(type(self).template.getRoot())
        self.page.find("main").append(BeautifulSoup(words, 'html.parser'))

