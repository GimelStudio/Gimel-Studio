## ----------------------------------------------------------------------------
## Gimel Studio © 2020 Correct Syntax, Noah Rahm. All rights reserved.
##
## FILE: file_dnd.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Drag and Drop files into the node graph feature
## ----------------------------------------------------------------------------

import os
import imghdr
import wx


class NodeGraphFileDrop(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self._window = window

    def OnDropFiles(self, x, y, filenames):
        for filename in filenames:
            try:
                filename_ext = imghdr.what(filename)
                if filename_ext in ['jpg', 'jpeg', 'bmp', 'png']:
                    if os.path.exists(filename) == True:
                        self._window.AddImageNodeFromDrop(filename)
                    else:
                        self.ShowError()

                else:
                    dlg = wx.MessageDialog(
                        None, 
                        "That file type isn't currently supported!", 
                        "Cannot Open File!", 
                        style=wx.ICON_EXCLAMATION
                        )
                    dlg.ShowModal()
                    return False

            except Exception as error:
                self.ShowError(error)

        return True

    def ShowError(self, error=''):
        dlg = wx.MessageDialog(
            None, 
            "Error opening file\n {}!".format(str(error)), 
            "Error!", 
            style=wx.ICON_ERROR
            )
        dlg.ShowModal()
        return False
