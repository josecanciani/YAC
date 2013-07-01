# Tool to rebuild the .tags files

import sublime_plugin
from sublime import status_message
from yac.CTags import *


# Note: Yac is not YAC because of Sublime's camel case normalization not handling YAC well
class YacRebuildCtagsCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        try:
            status_message('Rebuilding CTags files...')
            CTags.rebuild(self.view)
            status_message('CTags files rebuilt')
        except CTagsException as e:
            status_message('CTags exception: ' + str(e))
