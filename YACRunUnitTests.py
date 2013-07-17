
import sublime
import sublime_plugin
import os
import sys


# Note: Yac is not YAC because of Sublime's camel case normalization not handling YAC well
class YacRunUnitTestsCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        sublime.status_message('YAC: starting unit tests')
        print ''
        print 'Running unit tests for YAC'
        print ''
        python = sys.executable
        if not python:
            print 'Warning: python executable is not defined, asumming "python"'
            print ''
            python = 'python'
        cmd = python + ' "' + os.path.join(os.path.join(sublime.packages_path(), 'YAC'), 'runUnitTests.py') + '" 2>&1'
        f = os.popen(cmd)
        for line in f.readlines():
            sys.stdout.write(line)
        sublime.status_message('YAC: unit tests run, check console for details')
