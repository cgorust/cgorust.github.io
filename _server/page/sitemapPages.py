from page.page import Page
from model.path import Path
from model.config import SITE, SITEMAP

from datetime import datetime

class SitemapPages(Page):
    pages = []

    def __init__(self, path):
        super().__init__(path)
        sitemaps = self.page.find_all("loc")
        urls = [s.getText() for s in sitemaps]
        for url in urls:
            url = url.replace(SITE, "")
            page = Page(url)
            type(self).pages.append(page)
            
    def getWordTimes(self) -> list:
        wordTimes = []
        for page in type(self).pages:
            urls = page.getRoot().find_all("url")
            for url in urls:
                loc = url.find("loc").getText()
                key = Path.pathToKey(loc.replace(SITE + "dictionary/", ""))
                lastmod = url.find("lastmod").getText()
                #print("key:{},lastmod:{}".format(key, lastmod))
                wordTimes.append((key, lastmod))
        return wordTimes


    def generateSitemap(self, wordTimes):
        SIZE = 38000
        PARTS = int(len(wordTimes)/SIZE)+1

        content = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n"
        content += "<sitemapindex xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n"
        for part in range(PARTS):
            content += "  <sitemap>\n"
            content += "    <loc>" + SITE + "sitemap_" + str(part*SIZE) + ".xml</loc>\n"
            content += "    <lastmod>" + datetime.now().strftime("%Y-%m-%d") + "</lastmod>\n"
            content += "  </sitemap>\n"
        content += "</sitemapindex>"
        f = open(SITEMAP, "w")
        f.write(content)
        f.close()             

        for part in range(PARTS):
            file =  "sitemap_" + str(part*SIZE) + ".xml"
            f = open(file, "w")
            content = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n"
            content += "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n"
            for i in range(SIZE):
                j = part*SIZE + i
                if j == len(wordTimes):
                    break
                content +=  "  <url>\n"
                content += "    <loc>" + SITE + wordTimes[j][0] + "</loc>\n"
                content += "    <lastmod>" +  wordTimes[j][1] + "</lastmod>\n"
                content +=  "  </url>\n"
            f.write(content)
            f.close()             
