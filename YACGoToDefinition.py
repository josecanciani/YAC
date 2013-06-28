# Use CTags to open definitions
# TODOs:
#   Make it work :)
#   should open classes and also can open methods in the future

import sublime_plugin


class YACGoToDefinition(sublime_plugin.TextCommand):

    def run(self, edit):
        print 'hola mundo'
        view = self.view
        region = view.sel()[0]
        print 'substr: ' + view.substr(view.extract_scope(region.begin()))
        # window = sublime.active_window()
        # window.open_file(maybe_path)
