## ----------------------------------------------------------------------------
## Gimel Studio © 2020 Correct Syntax, Noah Rahm. All rights reserved.
##
## FILE: update_checker.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Checks online to see if there is a newer Gimel Studio release
## ----------------------------------------------------------------------------

import threading
import urllib.request
import re

from GimelStudio.meta import __VERSION__

WEBSITE_URL = "https://correctsyntax.com/gimel-studio-latest-update.txt"

# TODO: Needs a lot of work
class ProgramUpdateChecker(threading.Thread):
    def __init__(self, version):
        threading.Thread.__init__(self, name="updatechecker")

        self._onlineVersion = None
        self._changes = []
        self._checkDone = False
        self._isOk = False

        self.start()

    def run(self):
        try:
#            file = urllib.request.urlopen(WEBSITE_URL)
            file = open('update.txt', 'r') # Open local file for testing
            data = file.read()
        except IOError:
            self._checkDone = True
            return



        ovMatch = re.match(r"(\d+).(\d+).(\d+)?(.+)?", data)
        print(ovMatch.groups()[:3])
        if ovMatch:
            self._onlineVersion = ".".join(ovMatch.groups()[:3])
            print(self._onlineVersion)
        else:
            return

        #self._changes = lines

        self._checkDone = True
        self._isOk = True

    def IsDone(self):
        return self._checkDone

    def IsOk(self):
        return self._isOk

    def IsNewer(self, currentVersion):
        if self.IsDone() and self.IsOk():
            curTup = currentVersion.split(".")
            newTup = self._onlineVersion.split(".")
            return newTup > curTup
        return False

    def GetChanges(self):
        return "\n".join(self._changes)

    def GetVersion(self):
        return self._onlineVersion
