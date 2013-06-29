# Use CTags to open definitions
# TODOs:
#   Only works with classes, should also open methods

import sublime_plugin
import sublime
from sublime import status_message
from yac.CTags import *


# Note: Yac is not YAC because of Sublime's camel case normalization not handling YAC well
class YacGoToDefinitionCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        wordPoint = self.view.word(self.view.sel()[0])
        word = self.view.substr(wordPoint)
        if len(word) > 0:
            try:
                cTags = CTags(self.view)
                searchClass = cTags.getClassFromName(word)
                if searchClass:
                    window = sublime.active_window()
                    window.open_file(searchClass.getClassFile())
                else:
                    status_message('Symbol not found')
            except CTagsException as e:
                status_message('CTags exception: ' + str(e))
        else:
            status_message('Could not extract word')
