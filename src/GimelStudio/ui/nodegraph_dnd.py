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
## FILE: nodegraph_dnd.py
## AUTHOR(S): Noah Rahm
## PURPOSE: DragnDrop files into the node graph from node registry or file dir
## ----------------------------------------------------------------------------

import os
import imghdr
import wx


class NodeGraphDropTarget(wx.DropTarget):
    def __init__(self, window, *args, **kwargs):
        super(NodeGraphDropTarget, self).__init__(*args, **kwargs)
        self._window = window
        self._composite = wx.DataObjectComposite()
        self._textDropData = wx.TextDataObject()
        self._fileDropData = wx.FileDataObject()
        self._thunderbirdDropData = wx.CustomDataObject('text/x-moz-message')
        self._composite.Add(self._thunderbirdDropData)
        self._composite.Add(self._textDropData)
        self._composite.Add(self._fileDropData)
        self.SetDataObject(self._composite)

    def OnDrop(self, x, y):
        return True

    def OnData(self, x, y, result):
        self.GetData()
        formatType, formatId = self.GetReceivedFormatAndId()
        if formatId == 'text/x-moz-message':
            return self.OnThunderbirdDrop()
        elif formatType in (wx.DF_TEXT, wx.DF_UNICODETEXT):
            return self.OnTextDrop()
        elif formatType == wx.DF_FILENAME:
            return self.OnFileDrop()

    def GetReceivedFormatAndId(self):
        format = self._composite.GetReceivedFormat()
        formatType = format.GetType()
        try:
            formatId = format.GetId() # May throw exception on unknown formats
        except:
            formatId = None
        return formatType, formatId

    def OnThunderbirdDrop(self):
        # Do we need this?
        print(self._thunderbirdDropData.GetData().decode('utf-16'))
        return wx.DragCopy

    def OnTextDrop(self):
        try:
            self._window.AddNodeFromNodeRegistryDrop(self._textDropData.GetText())
        except Exception as error:
            self.ShowError(error)
        return wx.DragCopy

    def OnFileDrop(self):
        for filename in self._fileDropData.GetFilenames():
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

        return wx.DragCopy

    def ShowError(self, error=''):
        dlg = wx.MessageDialog(
            None, 
            "Error \n {}!".format(str(error)), 
            "Error!", 
            style=wx.ICON_ERROR
            )
        dlg.ShowModal()
        return False