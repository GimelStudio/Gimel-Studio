## THIS FILE IS A PART OF GIMEL STUDIO AND IS LICENSED UNDER THE SAME TERMS:
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
## ----------------------------------------------------------------------------

import os
import imghdr

import wx
from PIL import Image

from GimelStudio.api import (Color, RenderImage, NodeBase,
                            Parameter, Property, RegisterNode)

 
class NodeDefinition(NodeBase):
    
    @property
    def NodeIDName(self):
        return "gimelstudiocorenode_image"

    @property
    def NodeLabel(self):
        return "Image"

    @property
    def NodeCategory(self):
        return "INPUT"

    @property
    def NodeDescription(self):
        return "Inputs an image from the specified file path." 

    @property
    def NodeVersion(self):
        return "2.2" 

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software" 

    @property
    def NodeProperties(self): 
        return [
            Property('Path',
                prop_type='FILEPATH',
                value=''
                ),
        ]


    def NodePropertiesUI(self, node, parent, sizer):
        self.parent = parent

        current_value = self.NodeGetPropValue('Path')
 
        pathlabel = wx.StaticText(parent, label="Path:")
        sizer.Add(pathlabel, flag=wx.LEFT|wx.TOP, border=5)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.pathtxtctrl = wx.TextCtrl(parent)
        self.pathtxtctrl.ChangeValue(current_value)
        hbox.Add(self.pathtxtctrl, proportion=1)
        self.browsepathbtn = wx.Button(parent, label="Browse...")
        hbox.Add(self.browsepathbtn, flag=wx.LEFT, border=5)
        vbox.Add(hbox, flag=wx.EXPAND)

        sizer.Add(vbox, flag=wx.ALL|wx.EXPAND, border=5)

        infolabellbl = wx.StaticText(parent, label="Meta: ")
        sizer.Add(infolabellbl, flag=wx.LEFT|wx.TOP, border=5)

        self.infolabellbl = wx.StaticText(parent, label="")
        sizer.Add(self.infolabellbl, flag=wx.LEFT|wx.TOP, border=5)

        if current_value != '':
            self.UpdateInfoLabel(current_value)
            self.infolabellbl.SetLabel(self.GetInfoLabel())

        parent.Bind(wx.EVT_BUTTON, self.OnFilePathButton, self.browsepathbtn)


    def OnFilePathButton(self, evt):
        wildcard = "All files (*.*)|*.*|" \
                   "JPG file (*.jpg)|*.jpg|" \
                   "PNG file (*.png)|*.png|" \
                   "BMP file (*bmp)|*bmp"

        dlg = wx.FileDialog(
            self.parent, message="Choose image...",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW
            )

        # Show the dialog and retrieve the user response. If it is the OK response,
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            paths = dlg.GetPaths() 

            filename_ext = imghdr.what(paths[0])
            if filename_ext in ['jpg', 'jpeg', 'bmp', 'png']:
                self.NodePropertiesUpdate('Path', paths[0])
                self.pathtxtctrl.ChangeValue(paths[0])
                self.UpdateInfoLabel(paths[0])
                self.infolabellbl.SetLabel(self.GetInfoLabel())
            else:
                dlg = wx.MessageDialog(
                    None, 
                    "That file type isn't currently supported!", 
                    "Cannot Open File!", 
                    style=wx.ICON_EXCLAMATION
                    )
                dlg.ShowModal()
                return False       

 
    def UpdateInfoLabel(self, imagepath):
        try:
            img = Image.open(imagepath)
            info_string = "{}x{}px | {} | {}kB".format(
                img.size[0], 
                img.size[1],
                img.mode,
                str(os.path.getsize(imagepath)/1000)
                )
            self.NodeSetThumb(img, force_redraw=True) 
            self.infolabel = info_string
        except FileNotFoundError:
            self.infolabel = 'IMAGE COULD NOT BE FOUND!'


    def GetInfoLabel(self):
        return self.infolabel


    def NodeEvaluation(self, eval_info):
        path = eval_info.EvaluateProperty('Path')
        image = RenderImage()

        if path != '':
            try:
                image.SetAsOpenedImage(path)
                image.SetAsImage(image.GetImage().convert('RGBA'))
            except FileNotFoundError:
                pass

        self.NodeSetThumb(image.GetImage())
        return image 


RegisterNode(NodeDefinition)