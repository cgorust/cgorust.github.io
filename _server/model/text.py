import html

class Text:
    @classmethod
    def isHtmlEncodedText(cls, text) -> str:
        newText = html.unescape(text)
        if newText == text:
            return False
        return True

    @classmethod
    def htmlEncodeText(cls, text) -> str:
        if cls.isHtmlEncodedText(text):
            return text
        text = html.escape(text)
        return text

    @classmethod
    def htmlDecodeText(cls, text) -> str:
        if not cls.isHtmlEncodedText(text):
            return text
        text = html.unescape(text)
        return text
