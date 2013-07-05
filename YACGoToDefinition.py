# Use CTags to open definitions
# TODOs:
#   Only works with classes, should also open methods

import sublime_plugin
import sublime
from sublime import status_message
from yac.CTags import *
from yac.Parser import *
from yac.Class import *


# Note: Yac is not YAC because of Sublime's camel case normalization not handling YAC well
class YacGoToDefinitionCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.parser = Parser(self.view)
        word = self.parser.getCurrentPositionSymbol()
        try:
            self.cTags = CTags(self.view)
        except CTagsException as e:
            status_message('YAC: CTags exception: ' + str(e))
        if len(word) > 0:
            if self.parser.isCurrentPositionAMethod():
                currentClass = self.cTags.getClassFromName(self.parser.getClassFromMethodInCurrentPosition())
                if currentClass:
                    results = self.cTags.getMethodsFromClass(currentClass, word)
                    if len(results) > 0:
                        self.showQuickPanel(results)
                        return
            if self.parser.isCurrentPositionAFunction():
                results = self.cTags.getFunctionsFromName(word)
                if len(results) > 0:
                    self.showQuickPanel(results)
                    return
            results = self.cTags.getClassesFromName(word)
            if len(results) > 0:
                self.showQuickPanel(results)
                return
        status_message('YAC: current symbol not found')

    def showQuickPanel(self, items):
        self.items = items
        if len(items) == 1:
            self.goToItem(0)
        else:
            sublime.active_window().show_quick_panel([[item.getName(), self.cTags.getRelativeFilePath(item.getFile())] for item in self.items], self.goToItem)

    def goToItem(self, idx):
        if idx >= 0:
            sublime.active_window().open_file(self.items[idx].getFile() + ':' + self.items[idx].getDefinitionLineNumber(), sublime.ENCODED_POSITION)
