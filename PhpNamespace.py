# -*- coding: utf-8 -*-
'''
Provides PHP namespace insertion in SublimeText

Config summary (see README.md for details):

    # key binding
    { "keys": ["ctrl+alt+n"], "command": "php_namespace" }
²
@author: Alexandre Salomé <alexandre.salome@gmail.com>
@license: MIT (http://www.opensource.org/licenses/mit-license.php)
@since: 2012-03-15
'''

import re, sublime, sublime_plugin, os, json

class PhpNamespaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        # Filename to namespace
        filename = self.view.file_name()

        if (not filename.endswith(".php")):
            sublime.error_message("No .php extension")
            return

        breakwords = [ "src", "lib", "tests"]
        breakwords.extend(sublime.load_settings("Preferences.sublime-settings").get('PhpNamespace_breakwords', []));
        for breakword in breakwords:
            segment = os.sep + breakword + os.sep
            pos = filename.find(segment)
            if (pos != -1):
                break

        if (pos == -1):
            namespace = None
            folders = filename.split(os.sep)
            folders.reverse()

            for folder in folders[1:-1]:
                if (folder[0].upper() == folder[0]):
                    if None == namespace:
                        namespace = folder
                    else:
                        namespace = folder + "\\" + namespace

            if None == namespace:
                sublime.error_message("No folder " + breakwords.join(" or ") + "in file:\n" + filename)
                return
        else:
            className = filename[pos+len(segment):-4].replace("/", "\\")
            namespace = re.sub(r'\\\w+$', '', className)

            # Check if a composer.json file exists
            composerFilename = filename[:pos] + os.sep + "composer.json"
            if os.path.exists(composerFilename):
                json_data=open(composerFilename)
                try:
                    data = json.load(json_data)
                    json_data.close()
                    try:
                        # Iterate through all PSR-4 definitions
                        for (nsPrefix, nsPath) in data["autoload"]["psr-4"].items():
                            # Every namespace prefix should end with \\, but let's be tolerate
                            if not nsPrefix.endswith("\\"):
                                nsPrefix += "\\"
                            # If the filename after the breakword starts with the path for the namespace,
                            # we want to add the namespace prefix to the namespace
                            if filename[pos:].startswith("/" + nsPath):
                                # If we are in the "root" (or breakword) directory, the className consists only of the
                                # className, without a namespace and we want to replace the class name with the
                                # namespace prefix.
                                # Else we have a namespace and we add the prefix at the beginning
                                if className.find("\\") == -1:
                                    namespace = nsPrefix[:-1]
                                else:
                                    namespace = nsPrefix + namespace
                    except KeyError:
                        # If there is no autoload or PSR-4 definition in composer.json
                        pass
                except ValueError:
                    # If composer.json is not valid
                    pass

        sels = self.view.sel()
        for sel in sels:
            self.view.erase(edit, sel)
            self.view.insert(edit, sel.begin(), "namespace " + namespace + ";\n")
