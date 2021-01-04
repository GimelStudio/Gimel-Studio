# ----------------------------------------------------------------------------
# Gimel Studio Copyright 2019-2020 by Noah Rahm and contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# FILE: about_dialog.py
# AUTHOR(S): Noah Rahm
# PURPOSE: Defines the Gimel Studio about dialog
# ----------------------------------------------------------------------------

# TODO: Create better about dialog!

import sys

import wx
import PIL
import scipy
import cv2
import numpy as np
from wx.lib.wordwrap import wordwrap

from GimelStudio import meta


# class AboutDialog(wx.Dialog):
#     def __init__(self, size=wx.Size(700, 1000), *args, **kwds):
#         wx.Dialog.__init__(self, size, *args, **kwds)

#         self.notebook = wx.Notebook(self, -1, style=0)
#         self.notebook_pane_6 = wx.Panel(self.notebook, -1)
#         self.notebook_1_pane_5 = wx.Panel(self.notebook, -1)
#         self.notebook_1_pane_4 = wx.Panel(self.notebook, -1)
#         self.notebook_1_pane_3 = wx.Panel(self.notebook, -1)
#         self.notebook_1_pane_2 = wx.Panel(self.notebook, -1)
#         self.notebook_1_pane_1 = wx.Panel(self.notebook, -1)


#         self.credits_code = wx.TextCtrl(self.notebook_1_pane_1, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
#         self.credits_documentation = wx.TextCtrl(self.notebook_1_pane_2, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
#         self.credits_translation = wx.TextCtrl(self.notebook_1_pane_3, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
#         self.credits_graphics = wx.TextCtrl(self.notebook_1_pane_4, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
#         self.credits_libraries = wx.TextCtrl(self.notebook_1_pane_5, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
#         self.credits_sponsors = wx.TextCtrl(self.notebook_pane_6, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
#         self.close = wx.Button(self, wx.ID_CLOSE, "&Close")

#         self.SetTitle("About Gimel Studio")
#         self.__do_layout()

#         self.Bind(wx.EVT_BUTTON, self.OnClose, id=wx.ID_CLOSE)
#         # end wxGlade


#     def __do_layout(self):
#         # begin wxGlade: wxgCreditsDialog.__do_layout
#         sizer_100 = wx.BoxSizer(wx.VERTICAL)
#         sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
#         sizer_11_copy_3 = wx.BoxSizer(wx.HORIZONTAL)
#         sizer_11_copy_2 = wx.BoxSizer(wx.HORIZONTAL)
#         sizer_11_copy_1 = wx.BoxSizer(wx.HORIZONTAL)
#         sizer_11_copy = wx.BoxSizer(wx.HORIZONTAL)
#         sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
#         sizer_11.Add(self.credits_code, 1, wx.EXPAND, 0)
#         self.notebook_1_pane_1.SetSizer(sizer_11)
#         sizer_11_copy.Add(self.credits_documentation, 1, wx.EXPAND, 0)
#         self.notebook_1_pane_2.SetSizer(sizer_11_copy)
#         sizer_11_copy_1.Add(self.credits_translation, 1, wx.EXPAND, 0)
#         self.notebook_1_pane_3.SetSizer(sizer_11_copy_1)
#         sizer_11_copy_2.Add(self.credits_graphics, 1, wx.EXPAND, 0)
#         self.notebook_1_pane_4.SetSizer(sizer_11_copy_2)
#         sizer_11_copy_3.Add(self.credits_libraries, 1, wx.EXPAND, 0)
#         self.notebook_1_pane_5.SetSizer(sizer_11_copy_3)
#         sizer_1.Add(self.credits_sponsors, 1, wx.EXPAND, 0)
#         self.notebook_pane_6.SetSizer(sizer_1)
#         self.notebook.AddPage(self.notebook_1_pane_1, "Code")
#         self.notebook.AddPage(self.notebook_1_pane_2, "Documentation")
#         self.notebook.AddPage(self.notebook_1_pane_3, "Translation")
#         self.notebook.AddPage(self.notebook_1_pane_5, "Libraries")
#         self.notebook.AddPage(self.notebook_pane_6, "Sponsors")
#         sizer_100.Add(self.notebook, 1, wx.EXPAND, 0)
#         sizer_100.Add(self.close, 0, wx.ALL|wx.ALIGN_RIGHT, 4)
#         self.SetSizer(sizer_100)


#     def OnClose(self,event):
#         self.Destroy()


class AboutDialog(object):
    def __init__(self, parent):
        self._parent = parent
        self._name = meta.APP_NAME
        self._title = meta.APP_TITLE
        self._author = meta.APP_AUTHOR
        self._version = meta.APP_VERSION
        self._versionTag = meta.APP_VERSION_TAG
        self._pillowVersion = PIL.__version__
        self._wxPythonVersion = wx.VERSION_STRING
        self._pythonVersion = sys.version.split()[0]
        self._opencvVersion = cv2.__version__
        self._numpyVersion = np.__version__
        self._scipyVersion = scipy.__version__

    def ShowDialog(self):
        info = wx.adv.AboutDialogInfo()
        info.SetName(self._name)
        info.SetVersion("v{0}.{1}.{2} {3}".format(
            self._version[0], self._version[1], self._version[2], self._versionTag))
        info.SetCopyright("(c) 2019-2021 {}. All rights reserved.".format(self._author))
        info.SetDescription(
            wordwrap(
                margin=10,
                text="""
Non-destructive (node-based), realtime graphics editing program for Windows and Linux.

This version of Gimel Studio is made possible thanks to the following open-source projects:

- Python {0}
- Pillow {1}
- wxPython {2}
- Numpy {3}
- Scipy {4}
- OpenCV {5}

Praise to our Heavenly Father, YAHWEH for allowing the time and resources to make this software program a reality.

Please consider giving your feedback through the program menu (Help > Feedback Survey) so that I can work to improve Gimel Studio. :)
                """.format(
                    self._pythonVersion,
                    self._pillowVersion,
                    self._wxPythonVersion,
                    self._numpyVersion,
                    self._scipyVersion,
                    self._opencvVersion
                ),
                width=550,
                dc=wx.ClientDC(self._parent)
            ))
        info.SetWebSite("https://correctsyntax.com/projects/gimel-studio/", "Visit the Gimel Studio Homepage")

        wx.adv.AboutBox(info)
