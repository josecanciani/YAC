
import sublime
import os
from Parser import *


class Setting(object):

    def __init__(self, view):
        self.view = view

    @staticmethod
    def getProjectPath():
        return os.path.join(sublime.packages_path(), 'YAC')

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

    def isSupportedSyntax(self):
        return self.getSyntax() in Setting.getSupportedLanguages()

    def getSyntax(self):
        syntax = self.view.settings().get('syntax')
        if syntax.find('PHP') > 0:
            return 'PHP'
        if syntax.find('Python') > 0:
            return 'Python'
        return None
