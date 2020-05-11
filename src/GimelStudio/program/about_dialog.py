## ----------------------------------------------------------------------------
## Gimel Studio Copyright 2020 Noah Rahm, Correct Syntax. All rights reserved.
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##    http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
##
## FILE: about_dialog.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Defines the Gimel Studio about dialog
## ----------------------------------------------------------------------------

import sys

import PIL
import wx
from wx.lib.wordwrap import wordwrap

from GimelStudio.meta import (__NAME__, __AUTHOR__, __VERSION__,
                              __BUILD__, __RELEASE__, __TITLE__)


class AboutGimelStudioDialog(object):
    def __init__(self, parent):
        self._parent = parent
        self._name = __NAME__
        self._title = __TITLE__
        self._author = __AUTHOR__
        self._version = __VERSION__
        self._build = __BUILD__
        self._release = __RELEASE__
        self._pillowVersion = PIL.__version__
        self._wxPythonVersion = wx.VERSION_STRING
        self._pythonVersion = sys.version.split()[0]
    
    def ShowDialog(self):
        info = wx.adv.AboutDialogInfo()
        info.SetName(self._name)
        info.SetVersion("v{0}.{1}".format(self._version, self._release))
        info.SetCopyright("© 2020 {}. All rights reserved.".format(self._author))
        info.SetDescription(
            wordwrap(
                margin=10,
                text="""
Non-destructive (node-based), realtime graphics editing program for Windows and Linux.

This version of Gimel Studio is made possible thanks to the following open-source projects:

- Python {}
- Pillow {}
- wxPython {}
- Numpy 
- Scipy

Praise to our Heavenly Father, YAHWEH for allowing the time and resources to make this software program a reality. 

Please consider giving your feedback through the program menu (Help > Feedback Survey) so that I can work to improve Gimel Studio. :)
                """.format(
                    self._pythonVersion,
                    self._pillowVersion,
                    self._wxPythonVersion
                ),
                width=550, 
                dc=wx.ClientDC(self._parent)
                ))
        info.SetWebSite("https://correctsyntax.com/projects/gimel-studio/", "Visit the Gimel Studio Homepage")

        wx.adv.AboutBox(info)
        
