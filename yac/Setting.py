
import sublime
import re
import os


class Setting(object):

    def __init__(self, view):
        self.view = view

    @staticmethod
    def getProjectPath():
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @staticmethod
    def getResourcesPath():
        return os.path.join(Setting.getProjectPath(), 'resources')

    @staticmethod
    def getSupportedLanguages():
        return ['PHP']

    def _getDefaults(self):
        return sublime.load_settings("YAC.sublime-settings")

    def get(self, key, default=None):
        try:
            s = self.view.settings()
            if s.has("yac_%s" % key):
                return s.get("yac_%s" % key)
        except:
            pass
        return self._getDefaults().get(key, default)

    def isCompletingMethods(self):
        wholeRegion = sublime.Region(0, self.view.size())
        pos = self.view.sel()[0].begin()
        text = self.view.substr(wholeRegion)
        words = re.split('(\W+)', text[:pos])
        if len(words) > 1:
            if words[len(words)-2] in ('->', '.', '::'):
                return True
        return False

    def isSupportedSyntax(self):
        return self.getSyntax() in Setting.getSupportedLanguages()

    def getSyntax(self):
        syntax = self.view.settings().get('syntax')
        if syntax.find('PHP') > 0:
            return 'PHP'
        if syntax.find('Python') > 0:
            return 'Python'
        return None
