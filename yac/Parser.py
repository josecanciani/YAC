
import re
try:
    from sublime import Region
except ImportError:
    from mock.Region import Region


class Parser(object):

    def __init__(self, view):
        self.view = view
        self.text = self.view.substr(Region(0, self.view.size()))
        self.position = self.view.sel()[0].begin()

    def getCurrentPositionSymbol(self):
        point = self.view.word(self.view.sel()[0])
        return self.view.substr(point)

    def isCurrentPositionAMethod(self):
        words = re.split('(\W+)', self.text[:self.position])
        if len(words) > 1:
            if words[len(words)-2] in ('->', '.', '::'):
                return True
        return False

    def isCurrentPositionAFunction(self):
        words = re.split('(\W+)', self.text[:self.position])
        if len(words) > 2:
            if len(words[len(words)-2]) > 0 and words[len(words)-2][-1:].isspace():
                return True
        return False

    def getClassFromMethodInCurrentPosition(self):
        words = [word.strip() for word in re.split('(\W+)', self.text[:self.position]) if word.strip() and word.strip() != '$']  # remove $ from php variables
        if len(words) > 1:
            if words[len(words)-2] in ('->', '.', '::'):
                symbol = words[len(words)-3]
                #  ClassName.pp?
                if symbol[0].isupper():
                    return symbol
                #  this class?
                if symbol in ('self', 'static', 'this'):
                    for pos in range(len(words)-4, -1, -1):
                        if words[pos] == 'class':
                            return words[pos + 1]
                #  default to a variable, try to determine class
                for pos in range(len(words)-4, -1, -1):
                    if words[pos] == symbol:
                        if words[pos + 1] == '=':
                            if words[pos + 2] == 'new':
                                return words[pos + 3]
                            if words[pos + 2][0].isupper():
                                return words[pos + 2]
                        if words[pos - 1][0].isupper():
                            return words[pos - 1]
        return None
