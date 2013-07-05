# Extends Sublime Text autocompletion to find matches in .ctags
# files. By default, Sublime only considers words from the current file.
# Current support: methods (f kind of ctags)
# TODOs:
#   Check support for PHP's namespaces
#   Check support for JS

import sublime_plugin
import sublime
from sublime import status_message
from yac.Class import *
from yac.CTags import *
from yac.Setting import *
from yac.Parser import *


class YACAutoComplete(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):
        results = []
        try:
            cTags = CTags(view)
        except CTagsException as e:
            status_message('YAC: CTags exception: ' + str(e))
            return results
        setting = Setting(view)
        parser = Parser(view)
        if not parser.isCurrentPositionAMethod() or not view.window().folders():
            return results
        if not setting.isSupportedSyntax():
            status_message('YAC: auto complete not supported for language "' + setting.getSyntax() + '"')
            return results
        currentClass = cTags.getClassFromName(parser.getClassFromMethodInCurrentPosition())
        results = cTags.getMethodsFromClass(currentClass, prefix)
        if len(results):
            results = [(result.getDefinitionLine().strip(), result.getDefinitionLine.strip().replace('$', '\$')) for result in results]
            return (results, sublime.INHIBIT_EXPLICIT_COMPLETIONS)
        else:
            return results
