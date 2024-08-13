#
#

from html.parser import HTMLParser

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
    # def unknown_decl(self, data):
    #     print('\n')
    #     print('Unknown data decl') 
    #     print('\n')
    #     print(data)
    #     print('\n')
    # def handle_startendtag(self, tags, attrs):
    #     print('\n')
    #     print('handle start end') 
    #     print('\n')
    #     print(tags)
    #     print('\n')
    #     print(attrs)
    #     print('\n')
    # def handle_charref(self, name):
    #     print('\n')
    #     print('handle char ref') 
    #     print('\n')
    #     print(name)
    #     print('\n')
    # def handle_entityref(self, name):
    #     print('\n')
    #     print('handle entity ref') 
    #     print('\n')
    #     print(name)
    #     print('\n')

        
