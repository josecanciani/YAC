
import sublime
import sublime_plugin
import os
import sys


# Note: Yac is not YAC because of Sublime's camel case normalization not handling YAC well
class YacRunUnitTestsCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        sublime.status_message('YAC: starting unit tests')
        cmd = sys.executable + ' "' + os.path.join(os.path.join(sublime.packages_path(), 'YAC'), 'runUnitTests.py') + '" 2>&1'
        print cmd
        f = os.popen(cmd)
        for line in f.readlines():
            sys.stdout.write(line)
        sublime.status_message('YAC: unit tests run, check console for details')
