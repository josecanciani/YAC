
import sublime_plugin
from sublime import status_message
import unittest
import os
from yac.Setting import *


# Note: Yac is not YAC because of Sublime's camel case normalization not handling YAC well
class YacRunTestsCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        status_message('Running YAC unit tests')
        suite = unittest.defaultTestLoader.loadTestsFromNames(self._findTests())
        if unittest.TextTestRunner().run(suite).wasSuccessful():
            status_message('YAC unit tests run: no errors found')
        else:
            status_message('YAC unit tests run: errors found, see the console for details')

    def _findTests(self):
        fileList = ['yac.CTags_test']
        return fileList
        # FIXME: why this stop giving results when changing a test.py file?
        fileList = []
        for root, subFolders, files in os.walk(os.path.join(Setting.getProjectPath(), 'yac')):
            for file in files:
                if file[len(file)-len('_test.py'):] == '_test.py':
                    f = os.path.join(root, file)[len(root)+1:]
                    fileList.append('yac.' + f[:len(f)-3].replace('/', '.'))
        return fileList
