
import unittest
from Setting import *
from CTags import *
import os


class CTags_test(unittest.TestCase):

    def test_createCTagsFile(self):
        testFolder = os.path.join(Setting.getProjectPath(), 'resources')
        CTags.rebuild(None, testFolder)
        for lang in Setting.getSupportedLanguages():
            self.assertEqual(os.path.exists(os.path.join(testFolder, '.tags' + lang)), True)

if __name__ == '__main__':
    unittest.main()
