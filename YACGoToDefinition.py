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
        window = sublime.active_window()
        parser = Parser(self.view)
        word = parser.getCurrentPositionSymbol()
        try:
            cTags = CTags(self.view)
        except CTagsException as e:
            status_message('YAC: CTags exception: ' + str(e))
        if len(word) > 0:
            if parser.isCurrentPositionAMethod():
                currentClass = cTags.getClassFromName(parser.getClassFromMethodInCurrentPosition())
                if currentClass:
                    results = cTags.getMethodsFromClass(currentClass, word)
                    if len(results) > 0:
                        window.open_file(results[0].getClass().getClassFile() + ':' + results[0].getDefinitionLineNumber(), sublime.ENCODED_POSITION)
            if word[0].isupper():
                searchClass = cTags.getClassFromName(word)
                if searchClass:
                    window.open_file(searchClass.getClassFile() + ':' + searchClass.getDefinitionLineNumber(), sublime.ENCODED_POSITION)
        status_message('YAC: current symbol not found')
