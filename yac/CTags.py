
import os
from Class import Class
from Setting import Setting


class CTags(object):
    def __init__(self, view):
        self.view = view
        self.setting = Setting(self.view)
        self.folder = None
        for folder in self.view.window().folders():
            if folder == self.view.file_name()[:len(folder)]:
                self.folder = folder
        if self.folder is None:
            raise CTagsException('CTags needs a sublime folder to work')
        self.tagsFile = self.folder + "/.tags" + self.setting.getSyntax()
        if not os.path.exists(self.tagsFile):
            raise CTagsException('CTags file not found')

    @staticmethod
    def rebuild(view):
        folders = view.window().folders()
        setting = Setting(view)
        if len(folders) > 0:
            for folder in folders:
                for lang in Setting.getSupportedLanguages():
                    os.popen(setting.get('ctags_path') + ' -R --languages=' + lang + ' -f "' + folder + '/.tags' + lang + '" "' + folder + '"')
        else:
            raise CTagsException('No folders detected')

    def getCTagsFileName(self):
        return self.tagsFile

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


class CTagsException(Exception):
    pass
