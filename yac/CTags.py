
import os
from Class import Class
from Method import Method
from Setting import Setting


class CTags(object):
    def __init__(self, view, folder=None):
        self.view = view
        self.setting = Setting(self.view)
        if folder is None:
            self.folder = None
            for folder in self.view.window().folders():
                if folder == self.view.file_name()[:len(folder)]:
                    self.folder = folder
        else:
            self.folder = folder
        if self.folder is None:
            raise CTagsException('CTags needs a sublime folder to work')
        self.tagsFile = self.folder + "/.tags" + self.setting.getSyntax()
        if not os.path.exists(self.tagsFile):
            raise CTagsException('CTags file not found')

    @staticmethod
    def rebuild(view, folder=None):
        if folder is None:
            folders = view.window().folders()
        else:
            folders = [folder]
        setting = Setting(view)
        if len(folders) > 0:
            for folder in folders:
                for lang in Setting.getSupportedLanguages():
                    if os.path.exists(setting.get('ctags_path')):
                        cTagsBinary = setting.get('ctags_path')
                    else:
                        # hack for mac testing, during unit tests we cannot load view settings (for now)
                        if os.path.exists('/opt/local/bin/ctags'):
                            cTagsBinary = '/opt/local/bin/ctags'
                        else:
                            raise CTagsException('YAC: ctags binary not found')
                    cTagsFile = os.path.join(folder, '.tags' + lang)
                    if os.path.exists(cTagsFile):
                        os.remove(cTagsFile)
                    cmd = cTagsBinary + ' -R --languages=' + lang + ' -f "' + cTagsFile + '" "' + folder + '"'
                    os.popen(cmd)
        else:
            raise CTagsException('No folders detected')

    def getCTagsFileName(self):
        return self.tagsFile

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

    def _getMethodsFromClass(self, searchClass, prefix=None):
        results = []
        cmd = ''
        if prefix:
            cmd = "grep '^" + prefix + "' '" + self.tagsFile + "' | grep -F \"\t" + searchClass.getClassFile() + "\t\" | grep \"f$\""
        else:
            cmd = "grep -F \"\t" + searchClass.getClassFile() + "\t\" " + self.tagsFile + " | grep \"f$\""
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


class CTagsException(Exception):
    pass
