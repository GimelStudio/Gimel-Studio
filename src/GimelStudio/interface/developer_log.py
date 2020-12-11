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
# FILE: developer_log.py
# AUTHOR(S): Noah Rahm
# PURPOSE: Define the Developer Log panel
#
# This file includes code from Mike Driscoll and the wxPython demo
# ----------------------------------------------------------------------------

import sys

import wx

from GimelStudio import meta


class RedirectText(object):
    def __init__(self, textctrl):
        self.out = textctrl

    def write(self, string):
        self.out.WriteText(string)


class DeveloperLog(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)

        developer_log = wx.TextCtrl(self,
                                    wx.ID_ANY, style=wx.TE_READONLY | wx.TE_MULTILINE)
        sizer.Add(developer_log, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(sizer)

        developer_log.SetBackgroundColour("black")
        developer_log.SetForegroundColour("white")

        redirect = RedirectText(developer_log)

        # Only redirect if APP_DEBUG is not True
        # so that the stdout and stderr go to the
        # Python console during development.
        if meta.APP_DEBUG == False:
            sys.stdout = redirect
            sys.stderr = redirect
