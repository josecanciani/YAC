
import unittest
from Setting import *
from CTags import *
import os


class CTagsTest(unittest.TestCase):

    def test_createCTagsFile(self):
        CTags.rebuild(None, Setting.getResourcesPath())
        for lang in Setting.getSupportedLanguages():
            self.assertEqual(os.path.exists(os.path.join(Setting.getResourcesPath(), '.tags' + lang)), True)

if __name__ == '__main__':
    unittest.main()
