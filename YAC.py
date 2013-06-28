# Extends Sublime Text autocompletion to find matches in .ctags
# files. By default, Sublime only considers words from the current file.
# Current support: methods (f kind of ctags)
# TODOs:
#   Check support for PHP's namespaces
#   Check support for JS

import sublime_plugin
import os
import sublime
import re
from sublime import status_message

def get_settings():
    return sublime.load_settings("YAC.sublime-settings")

def get_setting(key, default=None, view=None):
    try:
        if view == None:
            view = sublime.active_window().active_view()
        s = view.settings()
        if s.has("yac_%s" % key):
            return s.get("yac_%s" % key)
    except:
        pass
    return get_settings().get(key, default)

class Class:
    def __init__(self, className, classFile, parentClassName, parentClassFile=None):
        self.className = className
        self.classFile = classFile
        self.parentClassName = parentClassName
        self.parentClassFile = parentClassFile

    def classExists(self):
        return len(self.className) > 0

    def getClassName(self):
        return self.className

    def getParentClassName(self):
        return self.parentClassName

    def getClassFile(self):
        return self.classFile


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


class CTagsAutocomplete(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):
        results = []
        cTags = CTags(view)
        if not self._isCompletingMethods(view) or not view.window().folders():
            return results
        if not self._isSupportedSyntax(view):
            status_message('Auto complete methods not supported for language "' + self._getSyntax(view) + '"')
            return results
        if not cTags.cTagsFileExists():
            status_message('No .tags file found for auto completing methods')
            return results
        currentClass = cTags.getClassFromFile(view.file_name()[len(os.path.dirname(cTags.getCTagsFileName()))+1:])
        i = 0
        while isinstance(currentClass, Class) and currentClass.classExists():
            i = i + 1
            if i > 10:
                raise Exception('Recursion limit reached')
            for result in cTags.getMethodsFromClass(prefix, currentClass):
                results.append(result)
            currentClass = cTags.getClassFromName(currentClass.getParentClassName())

        if len(results):
            results = [(result, result.replace('$', '\$')) for result in results]
            return (results, sublime.INHIBIT_EXPLICIT_COMPLETIONS)
        else:
            return results

    def _isCompletingMethods(self, view):
        wholeRegion = sublime.Region(0, view.size())
        pos = view.sel()[0].begin()
        text = view.substr(wholeRegion)
        words = re.split('(\W+)', text[:pos])
        if len(words) > 1:
            if words[len(words)-2] in ('->', '.', '::'):
                return True
        return False

    def _isSupportedSyntax(self, view):
        return self._getSyntax(view) in ('PHP')

    def _getSyntax(self, view):
        syntax = view.settings().get('syntax')
        if syntax.find('PHP') > 0:
            return 'PHP'
        if syntax.find('Python') > 0:
            return 'Python'
        return None
