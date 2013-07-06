
import os


class ViewSetting(object):

    def __init__(self, view):
        self.view = view

    def get(self, key):
        if key == 'syntax':
            fileName, fileExtension = os.path.splitext(self.view.file_name())
            if fileExtension.lower() == '.php':
                return 'PHP'
            if fileExtension.lower() == '.py':
                return 'Python'
            raise Exception('Mock Setting: syntax not supported: ' + fileExtension)
        raise Exception('Mock Setting not implemented: ' + str(key))
