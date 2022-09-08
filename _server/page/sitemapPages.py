from page.page import Page

SITE = "https://cgorust.com/"

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
            
    def getWordTimes(self):
        wordTimes = []
        for page in type(self).pages:
            urls = page.getRoot().find_all("url")
            for url in urls:
                loc = url.find("loc").getText()
                loc = self.unescapePath(loc.replace(SITE + "dictionary/", ""))
                lastmod = url.find("lastmod").getText()
                wordTimes.append((loc, lastmod))
        return wordTimes

