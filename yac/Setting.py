
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

    def isSupportedSyntax(self):
        return self.getSyntax() in Setting.getSupportedLanguages()

    def getSyntax(self):
        syntax = self.view.settings().get('syntax')
        if syntax.find('PHP') >= 0:
            return 'PHP'
        if syntax.find('Python') >= 0:
            return 'Python'
        return None
