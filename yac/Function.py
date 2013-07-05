
import os


class Function(object):

    def __init__(self, name, file, definitionLine):
        self.name = name
        self.file = file
        self.definitionLine = definitionLine

    def getName(self):
        return self.name

    def getFile(self):
        return self.file

    def getDefinitionLine(self):
        return self.definitionLine

    def getDefinitionLineNumber(self):
        cmd = "grep -n -F '" + self.getDefinitionLine().replace("'", "\\'").strip() + "' \"" + self.getFile() + "\""
        f = os.popen(cmd)
        for i in f.readlines():
            if i.find(':') > 0:
                return i[:i.find(':')]
        return '1'
