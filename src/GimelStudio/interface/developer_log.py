## ----------------------------------------------------------------------------
## Gimel Studio Copyright 2019-2020 by Noah Rahm and contributors
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
## FILE: developer_log.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the Developer Log panel
##
## This file includes code from Mike Driscoll and the wxPython demo
## ----------------------------------------------------------------------------

import sys

import wx
import wx.stc as stc

from GimelStudio import meta


if wx.Platform == '__WXMSW__':
    faces = { 'times': 'Times New Roman',
              'mono' : 'Courier New',
              'helv' : 'Arial',
              'other': 'Comic Sans MS',
              'size' : 10,
              'size2': 8,
             }
else:
    faces = { 'times': 'Times',
              'mono' : 'Courier',
              'helv' : 'Helvetica',
              'other': 'new century schoolbook',
              'size' : 12,
              'size2': 10,
             }


class RedirectText(object):
    def __init__(self, textctrl):
        self.out = textctrl

    def write(self, string):
        self.out.WriteText(string)


class DeveloperLog(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)

        developer_log = LogControl(self, wx.ID_ANY)
        sizer.Add(developer_log, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer)

        redirect = RedirectText(developer_log)

        # Only redirect if APP_DEBUG is not True
        # so that the stdout and stderr go to the
        # Python console during development.
        if meta.APP_DEBUG == False:
            sys.stdout = redirect
            sys.stderr = redirect


class LogControl(stc.StyledTextCtrl):
    def __init__(self, parent, id, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        stc.StyledTextCtrl.__init__(self, parent, id, pos, size, style)

        self.SetLexer(stc.STC_LEX_POWERSHELL)

        self.SetMargins(8, 8)
        self.SetViewWhiteSpace(False)
        self.SetBufferedDraw(True)
        self.SetUseAntiAliasing(True)

        # Reset all to be like the default
        self.StyleClearAll()

        # Global default style
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%(helv)s,size:%(size)d" % faces)
        # Default
        self.StyleSetSpec(stc.STC_P_DEFAULT, "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
        # Number
        self.StyleSetSpec(stc.STC_P_NUMBER, "fore:#007F7F,size:%(size)d" % faces)
        # String
        self.StyleSetSpec(stc.STC_P_STRING, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
        # Single quoted string
        self.StyleSetSpec(stc.STC_P_CHARACTER, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
        # Triple quotes
        self.StyleSetSpec(stc.STC_P_TRIPLE, "fore:#7F0000,size:%(size)d" % faces)
        # Triple double quotes
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:#7F0000,size:%(size)d" % faces)
        # Class name definition
        self.StyleSetSpec(stc.STC_P_CLASSNAME, "fore:#0000FF,bold,underline,size:%(size)d" % faces)
        # Function or method name definition
        self.StyleSetSpec(stc.STC_P_DEFNAME, "fore:#007F7F,bold,size:%(size)d" % faces)
        # Operators
        self.StyleSetSpec(stc.STC_P_OPERATOR, "bold,size:%(size)d" % faces)
        # Identifiers
        self.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
        # End of line where string is not closed
        self.StyleSetSpec(stc.STC_P_STRINGEOL, "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % faces)

        self.SetCaretForeground("Grey")