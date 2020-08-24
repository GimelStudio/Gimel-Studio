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

import wx
import wx.lib.agw.cubecolourdialog as CCD
from PIL import Image

from GimelStudio.api import (Color, RenderImage, List, NodeBase, 
                            Parameter, Property, RegisterNode)

  
class NodeDefinition(NodeBase):
    
    @property
    def NodeIDName(self):
        return "gimelstudiocorenode_colorimage"

    @property
    def NodeLabel(self):
        return "Color Image"

    @property
    def NodeCategory(self):
        return "INPUT"

    @property
    def NodeDescription(self):
        return "Creates a colored image." 

    @property
    def NodeVersion(self):
        return "1.0" 

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software" 

    @property
    def NodeProperties(self):
        return [
            Property('Color 1',
                prop_type='COLOR',
                value=(255, 255, 255, 255)
                ),
            Property('Size',
                prop_type='REGLIST',
                value=[256, 256]
                ),
            ]


    def NodePropertiesUI(self, node, parent, sizer):

        # Color
        current_color1_value = self.NodeGetPropValue('Color 1')
        self.color1data = wx.ColourData()
        self.color1data.SetColour(current_color1_value)

        color1_label = wx.StaticText(parent, label="Color 1:")
        sizer.Add(color1_label, flag=wx.TOP, border=5)

        color1_vbox = wx.BoxSizer(wx.VERTICAL)
        color1_hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.color1txtctrl = wx.TextCtrl(parent)
        self.color1txtctrl.ChangeValue(str(current_color1_value))
        color1_hbox.Add(self.color1txtctrl, proportion=1)
        self.color1btn = wx.Button(parent, label="Select...")
        color1_hbox.Add(self.color1btn, flag=wx.LEFT, border=5)
        color1_vbox.Add(color1_hbox, flag=wx.EXPAND)

        sizer.Add(color1_vbox, flag=wx.ALL|wx.EXPAND, border=5)

        # Size
        current_x_value = self.NodeGetPropValue('Size')[0]

        xsize_label = wx.StaticText(parent, label="X:")
        sizer.Add(xsize_label, flag=wx.TOP, border=5)

        self.xsize_spinctrl = wx.SpinCtrl(
            parent, id=wx.ID_ANY, 
            min=1, max=8000,
            initial=int(current_x_value)
            )
        self.size_x = int(current_x_value)
        sizer.Add(self.xsize_spinctrl, flag=wx.ALL|wx.EXPAND, border=5)


        # Y Size
        current_y_value = self.NodeGetPropValue('Size')[1]

        ysize_label = wx.StaticText(parent, label="Y:")
        sizer.Add(ysize_label, flag=wx.TOP, border=5)

        self.ysize_spinctrl = wx.SpinCtrl(
            parent, id=wx.ID_ANY, 
            min=1, max=8000,
            initial=int(current_y_value)
            )
        self.size_y = int(current_y_value)
        sizer.Add(self.ysize_spinctrl, flag=wx.ALL|wx.EXPAND, border=5)
        
        # Bindings
        parent.Bind(wx.EVT_BUTTON, self.OnColor1Button, self.color1btn)
        parent.Bind(wx.EVT_SPINCTRL, self.OnXSizeChange, self.xsize_spinctrl)
        parent.Bind(wx.EVT_SPINCTRL, self.OnYSizeChange, self.ysize_spinctrl)
        parent.Bind(wx.EVT_TEXT, self.OnXSizeChange, self.xsize_spinctrl)
        parent.Bind(wx.EVT_TEXT, self.OnYSizeChange, self.ysize_spinctrl)


    def OnXSizeChange(self, event):
        self.size_x = self.xsize_spinctrl.GetValue()
        self.NodePropertiesUpdate('Size', self.GetSize())

    def OnYSizeChange(self, event):
        self.size_y = self.ysize_spinctrl.GetValue()
        self.NodePropertiesUpdate('Size', self.GetSize())

    def GetSize(self):
        return [self.size_x, self.size_y]

    def OnColor1Button(self, event):
        self.color1dialog = CCD.CubeColourDialog(self.parent, self.color1data)
        if self.color1dialog.ShowModal() == wx.ID_OK:

            self.color1data = self.color1dialog.GetColourData()
            colordata = self.color1data.GetColour()
            self.NodePropertiesUpdate(
                'Color 1',
                (colordata.Red(),
                 colordata.Green(),
                 colordata.Blue(),
                 colordata.Alpha())
                )
            self.color1txtctrl.ChangeValue(str((colordata.Red(),
                                            colordata.Green(),
                                            colordata.Blue(),
                                            colordata.Alpha()
                                            )))

    
    def NodeEvaluation(self, eval_info):
        color1 = eval_info.EvaluateProperty('Color 1')
        imgsize = eval_info.EvaluateProperty('Size')

        image = RenderImage()
        image.SetAsImage(Image.new("RGBA", (imgsize[0], imgsize[1]), color1))
        self.NodeSetThumb(image.GetImage())
        return image

 
RegisterNode(NodeDefinition)