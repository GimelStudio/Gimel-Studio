## ----------------------------------------------------------------------------
## Gimel Studio © 2020 Correct Syntax, Noah Rahm. All rights reserved.
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