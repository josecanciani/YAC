
import os
import unittest
from yac.mock.View import View
from yac.mock.Setting import Setting

if __name__ == '__main__':

    view = View(os.path.join(Setting.getResourcesPath(), 'test.php'), Setting.getResourcesPath())
    setting = Setting(view)

    fileList = []
    for root, subFolders, files in os.walk(os.path.join(setting.getProjectPath(), 'yac')):
        for file in files:
            if file[len(file)-len('_test.py'):] == '_test.py':
                f = os.path.join(root, file)[len(root)+1:]
                fileList.append('yac.' + f[:len(f)-3].replace('/', '.'))

    suite = unittest.defaultTestLoader.loadTestsFromNames(fileList)
    if unittest.TextTestRunner().run(suite).wasSuccessful():
        print 'YAC: unit tests: no errors found'
    else:
        print 'YAC: unit tests: errors found'
