
import os
from Class import Class
from Method import Method
from Function import Function
from Setting import Setting


class CTags(object):
    def __init__(self, view):
        self.view = view
        self.setting = Setting(self.view)
        self.folder = None
        for folder in self.view.window().folders():
            if folder == self.view.file_name()[:len(folder)]:
                self.folder = folder
                break
        if self.folder is None:
            raise CTagsException('CTags needs a sublime folder to work')
        self.tagsFile = self.folder + "/.tags" + self.setting.getSyntax()
        if not os.path.exists(self.tagsFile):
            raise CTagsException('CTags file not found: ' + self.tagsFile)

    @staticmethod
    def rebuild(view):
        folders = view.window().folders()
        if len(folders) > 0:
            for folder in folders:
                for lang in Setting.getSupportedLanguages():
                    cTagsBinary = None
                    if os.path.exists('/usr/bin/ctags'):
                        cTagsBinary = '/usr/bin/ctags'
                    if os.path.exists('/opt/local/bin/ctags'):
                        cTagsBinary = '/opt/local/bin/ctags'
                    if cTagsBinary is None:
                        raise CTagsException('YAC: ctags binary not found')
                    cTagsFile = os.path.join(folder, '.tags' + lang)
                    if os.path.exists(cTagsFile):
                        os.remove(cTagsFile)
                    cmd = cTagsBinary + ' -R --languages=' + lang + ' -f "' + cTagsFile + '" "' + folder + '"'
                    os.popen(cmd)
        else:
            raise CTagsException('No folders detected')

    def getRelativeFilePath(self, filePath):
        return filePath[len(os.path.dirname(self.tagsFile))+1:]

    def getClassFromName(self, searchString):
        if searchString:
            return self._getClasses(searchString)[0]
        else:
            return None

    def getClassesFromName(self, searchString):
        if searchString:
            return self._getClasses(searchString)
        else:
            return []

    def _getClasses(self, searchString):
        results = []
        f = os.popen("grep \"^" + searchString + "\" '" + self.tagsFile + "' | grep \"[c|i]$\"")
        for i in f.readlines():
            className = i[:i.find("\t")]
            classFileName = i[i.find("\t")+1:i.find("\t", i.find("\t") + 1)]
            line = i[i.find('/^')+2:i.find('$/;"')]
            if line.find('extends') >= 0:
                parentClassName = line[line.find('extends')+7:].strip().split()[0]
            else:
                parentClassName = None
            results.append(Class(className, classFileName, parentClassName))
        return results

    def _getMethodsFromClass(self, searchClass, prefix=None):
        results = []
        cmd = ''
        if prefix:
            cmd = "grep '^" + prefix + "' '" + self.tagsFile + "' | grep -F \"\t" + searchClass.getFile() + "\t\" | grep \"f$\""
        else:
            cmd = "grep -F \"\t" + searchClass.getFile() + "\t\" " + self.tagsFile + " | grep \"f$\""
        f = os.popen(cmd)
        for i in f.readlines():
            results.append(self._extractMethod(i, searchClass))
        return results

    def _extractMethod(self, tagsLine, classObject):
        name = tagsLine[:tagsLine.find("\t")-1]
        line = tagsLine[tagsLine.find('/^')+2:tagsLine.find('$/;"')]
        line.strip()
        line = line[line.find('function')+8:line.find('{')]
        method = Method(name, classObject, line)
        return method

    def getMethodsFromClass(self, currentClass, prefix=None):
        results = []
        i = 0
        while isinstance(currentClass, Class) and currentClass.classExists():
            i = i + 1
            if i > 10:
                raise Exception('YAC: Recursion limit reached')
            for result in self._getMethodsFromClass(currentClass, prefix):
                results.append(result)
            currentClass = self.getClassFromName(currentClass.getParentClassName())
        return results

    def getFunctionsFromName(self, name):
        results = []
        f = os.popen("grep \"^" + name + "\" '" + self.tagsFile + "' | grep \"f$\"")
        for i in f.readlines():
            functionName = i[:i.find("\t")]
            functionFileName = i[i.find("\t")+1:i.find("\t", i.find("\t") + 1)]
            line = i[i.find('/^')+2:i.find('$/;"')]
            results.append(Function(functionName, functionFileName, line))
        return results


class CTagsException(Exception):
    pass
