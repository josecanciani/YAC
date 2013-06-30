
import sublime_plugin
from sublime import status_message
import unittest
import os


# Note: Yac is not YAC because of Sublime's camel case normalization not handling YAC well
class YacRunTestsCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        suite = unittest.defaultTestLoader.loadTestsFromNames(self._findTests())
        if unittest.TextTestRunner().run(suite).wasSuccessful():
            status_message('YAC unit tests run: no errors found')
        else:
            status_message('YAC unit tests run: errors found, see the console for details')

    def _findTests(self):
        fileList = []
        for root, subFolders, files in os.walk('yac'):
            for file in files:
                if file[len(file)-len('_test.py'):] == '_test.py':
                    f = os.path.join(root, file)
                    fileList.append(f[:len(f)-3].replace('/', '.'))
        return fileList
