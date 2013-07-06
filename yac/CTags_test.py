
import os
import unittest
from CTags import *
from Setting import Setting
from mock.View import *


class CTagsTest(unittest.TestCase):

    def setUp(self):
        self.view = View(os.path.join(Setting.getResourcesPath(), 'test.php'), Setting.getResourcesPath())
        self.setting = Setting(self.view)
        self.cTags = CTags(self.view)

    def test_aaa_createCTagsFile(self):
        CTags.rebuild(self.view)
        for lang in Setting.getSupportedLanguages():
            self.assertEqual(os.path.exists(os.path.join(Setting.getResourcesPath(), '.tags' + lang)), True)

    def test_getClassFromName(self):
        testClass = self.cTags.getClassFromName('TestClass')
        self.assertEqual('TestClass', testClass.getName())
