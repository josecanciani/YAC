
from Window import *
from ViewSetting import *


class View(object):

    def __init__(self, fileName, folder):
        self.fileName = fileName
        self.windowObject = Window(folder)
        self.setting = ViewSetting(self)

    def window(self):
        return self.windowObject

    def file_name(self):
        return self.fileName

    def settings(self):
        return self.setting
