
import os


class Class(object):
    def __init__(self, className, classFile, parentClassName, parentClassFile=None):
        self.className = className
        self.classFile = classFile
        self.parentClassName = parentClassName
        self.parentClassFile = parentClassFile

    def classExists(self):
        return len(self.className) > 0

    def getName(self):
        return self.className

    def getParentClassName(self):
        return self.parentClassName

    def getFile(self):
        return self.classFile

    def getDefinitionLineNumber(self):
        cmd = "grep -n -F 'class " + self.getName() + "' \"" + self.getFile() + "\""
        f = os.popen(cmd)
        for i in f.readlines():
            if i.find(':') > 0:
                return i[:i.find(':')]
        return '1'
