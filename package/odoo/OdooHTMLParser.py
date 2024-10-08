#
# Use HTMLParser to translate the html like formatted fields to text
#
# Replace as wierd spaces with normal spaces
# 
# Gert Wijsman
# August 2024
#
# inspriation:
# https://docs.python.org/3/library/html.parser.html
# https://en.wikipedia.org/wiki/Whitespace_character#Unicode
#

import logging
from html.parser import HTMLParser

logger = logging.getLogger(__name__)

# https://en.wikipedia.org/wiki/Whitespace_character#Unicode
charsReplaceBySpace = [
    '\u00a0', # NBSP   : Non-breaking space
    '\u200b', # ZWSP   : Zero width space
    '\u2060', # WJ     : &NoBreak; or Word Joiner
    '\ufeff', # ZWNBSP : Zero width no-break space
    '\u2002', # ENSP   : en space
    '\u2003', # EMSP   : em space
    '\u8203'  # ZWSP   : Zero width space
]

# https://docs.python.org/3/library/html.parser.html
class OdooHTMLParser(HTMLParser):
    text = ""
    def handle_data(self, data):
        d = data
        for c in charsReplaceBySpace:
            d = d.replace(c, ' ')
        d += '\n'
        self.text += d
