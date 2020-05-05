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
