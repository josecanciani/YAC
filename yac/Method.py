
import os


class Method(object):

    def __init__(self, name, classObject, definitionLine):
        self.name = name
        self.classObject = classObject
        self.definitionLine = definitionLine

    def getName(self):
        return self.name

    def getClass(self):
        return self.classObject

    def getDefinitionLine(self):
        return self.definitionLine

    def getDefinitionLineNumber(self):
        cmd = "grep -n -F '" + self.getDefinitionLine().replace("'", "\\'").strip() + "' \"" + self.getClass().getClassFile() + "\""
        f = os.popen(cmd)
        for i in f.readlines():
            if i.find(':') > 0:
                return i[:i.find(':')]
        return '1'
