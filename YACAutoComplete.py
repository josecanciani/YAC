# Extends Sublime Text autocompletion to find matches in .ctags
# files. By default, Sublime only considers words from the current file.
# Current support: methods (f kind of ctags)
# TODOs:
#   Check support for PHP's namespaces
#   Check support for JS

import sublime_plugin
import sublime
import os
from sublime import status_message
from yac.Class import *
from yac.CTags import *
from yac.Setting import *


class YACAutoComplete(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):
        results = []
        try:
            cTags = CTags(view)
        except CTagsException as e:
            status_message('CTags exception: ' + str(e))
            return results
        setting = Setting(view)
        if not setting.isCompletingMethods() or not view.window().folders():
            return results
        if not setting.isSupportedSyntax():
            status_message('Auto complete methods not supported for language "' + setting.getSyntax() + '"')
            return results
        currentClass = cTags.getClassFromFile(view.file_name()[len(os.path.dirname(cTags.getCTagsFileName()))+1:])
        i = 0
        while isinstance(currentClass, Class) and currentClass.classExists():
            i = i + 1
            if i > 10:
                raise Exception('Recursion limit reached')
            for result in cTags.getMethodsFromClass(prefix, currentClass):
                results.append(result)
            currentClass = cTags.getClassFromName(currentClass.getParentClassName())

        if len(results):
            results = [(result, result.replace('$', '\$')) for result in results]
            return (results, sublime.INHIBIT_EXPLICIT_COMPLETIONS)
        else:
            return results
