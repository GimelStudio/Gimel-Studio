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
## FILE: nr_dnd.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Drag and Drop files into the node graph from the node registry
## ----------------------------------------------------------------------------

import os
import wx


class NodeGraphNodeDrop(wx.TextDropTarget):
    def __init__(self, window):
        wx.TextDropTarget.__init__(self)
        self._window = window

    def OnDropText(self, x, y, data):
        try:
            self._window.AddNodeFromNodeRegistryDrop(data)
        except Exception as error:
            self.ShowError(error)

        return True

    def ShowError(self, error=''):
        dlg = wx.MessageDialog(
            None, 
            "Error \n {}!".format(str(error)), 
            "Error!", 
            style=wx.ICON_ERROR
            )
        dlg.ShowModal()
        return False