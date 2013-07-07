
from Window import *
from ViewSetting import *
from Region import *


class View(object):

    def __init__(self, folder, fileName, position=0):
        self.fileName = fileName
        self.windowObject = Window(folder)
        self.setting = ViewSetting(self)
        self.position = Region(position, position)
        if not os.path.exists(self.fileName):
            raise Exception('mock.View: file not found')
        f = open(fileName, 'r')
        self.text = f.read()

    def sel(self):
        return [self.position]

    def window(self):
        return self.windowObject

    def file_name(self):
        return self.fileName

    def settings(self):
        return self.setting

    def substr(self, region):
        return self.text[region.begin():region.end()]

    def size(self):
        return len(self.text)

    def word(self, position):
        words = self.text.split()
        characters = -1
        for word in words:
            characters += len(word)
            if characters >= position:
                return word
        return None
