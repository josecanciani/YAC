
import os
from Class import Class


class CTags:
    def __init__(self, view):
        self.tagsFile = view.window().folders()[0] + "/.tags"

    def getCTagsFileName(self):
        return self.tagsFile

    def cTagsFileExists(self):
        return os.path.exists(self.tagsFile)

    def getClassFromFile(self, searchString):
        if searchString:
            return self._getClass("grep -F '" + searchString + "' '" + self.tagsFile + "' | grep \"c$\"")
        else:
            return None

    def getClassFromName(self, searchString):
        if searchString:
            return self._getClass("grep \"^" + searchString + "\" '" + self.tagsFile + "' | grep \"c$\"")
        else:
            return None

    def _getClass(self, cmd):
        f = os.popen(cmd)
        for i in f.readlines():
            className = i[:i.find("\t")]
            classFileName = i[i.find("\t")+1:i.find("\t", i.find("\t") + 1)]
            line = i[i.find('/^')+2:i.find('$/;"')]
            if line.find('extends') >= 0:
                parentClassName = line[line.find('extends')+7:].strip().split()[0]
            else:
                parentClassName = None
            return Class(className, classFileName, parentClassName)

    def getMethodsFromClass(self, prefix, searchClass):
        results = []
        f = os.popen("grep '^" + prefix + "' '" + self.tagsFile + "' | grep -F \"\t" + searchClass.getClassFile() + "\t\" | grep \"f$\"")
        for i in f.readlines():
            symbol = self._extractFunction(i)
            results.append(symbol)
        return results

    def _extractFunction(self, tagsLine):
        line = tagsLine[tagsLine.find('/^')+2:tagsLine.find('$/;"')]
        line.strip()
        line = line[line.find('function')+8:line.find('{')]
        return line.strip()
