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
from PIL import Image, ImageOps

from GimelStudio.api import (Color, RenderImage, List, NodeBase, 
                            Parameter, Property, RegisterNode)

  
class NodeDefinition(NodeBase):
    
    @property
    def NodeIDName(self):
        return "corenode_gradientimage"

    @property
    def NodeLabel(self):
        return "Gradient Image"

    @property
    def NodeCategory(self):
        return "INPUT"

    @property
    def NodeDescription(self):
        return "Creates a gradient image." 

    @property
    def NodeVersion(self):
        return "1.2" 

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software" 

    @property
    def NodeProperties(self):
        return [
            Property('Amount',
                prop_type='INTEGER',
                value=1
                ),
            Property('Gradient',
                prop_type='LIST',
                value=List([
                    '0.1',
                    '0.2',
                    '0.5',
                    '0.75',
                    '1.0',
                    '1.5',
                    '2.0'
                    ], '0.5')
                ),
            Property('Color 1',
                prop_type='COLOR',
                value=(255, 255, 255, 255)
                ),
            Property('Color 2',
                prop_type='COLOR',
                value=(0, 0, 0, 1)
                ),
            Property('Size',
                prop_type='REGLIST',
                value=[256, 256]
                ),
            ]


    def NodePropertiesUI(self, node, parent, sizer):

        # Gradient
        current_gradient_value = self.NodeGetPropValue('Gradient')

        gradient_label = wx.StaticText(parent, label="Gradient:")
        sizer.Add(gradient_label, border=5)

        self.gradient_combobox = wx.ComboBox(
            parent, wx.ID_ANY, 
            value=current_gradient_value, 
            choices=[
                    '0.1',
                    '0.2',
                    '0.5',
                    '0.75',
                    '1.0',
                    '1.5',
                    '2.0'
                    ], 
            style=wx.CB_READONLY
            ) 
        sizer.Add(self.gradient_combobox, flag=wx.EXPAND|wx.ALL, border=5)


        # Color 1
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


        # Color 2
        current_color2_value = self.NodeGetPropValue('Color 2')
        self.color2data = wx.ColourData()
        self.color2data.SetColour(current_color1_value)

        color2_label = wx.StaticText(parent, label="Color 2:")
        sizer.Add(color2_label, flag=wx.TOP, border=5)

        color2_vbox = wx.BoxSizer(wx.VERTICAL)
        color2_hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.color2txtctrl = wx.TextCtrl(parent)
        self.color2txtctrl.ChangeValue(str(current_color2_value))
        color2_hbox.Add(self.color2txtctrl, proportion=1)
        self.color2btn = wx.Button(parent, label="Select...")
        color2_hbox.Add(self.color2btn, flag=wx.LEFT, border=5)
        color2_vbox.Add(color2_hbox, flag=wx.EXPAND)

        sizer.Add(color2_vbox, flag=wx.ALL|wx.EXPAND, border=5)


        # X Size
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
        parent.Bind(wx.EVT_COMBOBOX, self.OnGradientChange, self.gradient_combobox)
        parent.Bind(wx.EVT_BUTTON, self.OnColor1Button, self.color1btn)
        parent.Bind(wx.EVT_BUTTON, self.OnColor2Button, self.color2btn)
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

    def OnGradientChange(self, event):
        value = event.GetString()
        if not value:
            return
        self.NodePropertiesUpdate('Gradient', value)

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

    def OnColor2Button(self, event):
        self.color2dialog = CCD.CubeColourDialog(self.parent, self.color2data)
        if self.color2dialog.ShowModal() == wx.ID_OK:

            self.color2data = self.color2dialog.GetColourData()
            colordata = self.color2data.GetColour()
            self.NodePropertiesUpdate(
                'Color 2',
                (colordata.Red(),
                 colordata.Green(),
                 colordata.Blue(),
                 colordata.Alpha())
                )
            self.color2txtctrl.ChangeValue(str((colordata.Red(),
                                            colordata.Green(),
                                            colordata.Blue(),
                                            colordata.Alpha()
                                            )))
    
    def NodeEvaluation(self, eval_info):
        gradientvalue = eval_info.EvaluateProperty('Gradient')
        color1 = eval_info.EvaluateProperty('Color 1')
        color2 = eval_info.EvaluateProperty('Color 2')
        imgsize = eval_info.EvaluateProperty('Size')

        gradientimage = Image.new("L", (imgsize[0], 1))
        for x in range(imgsize[0]):
            gradientimage.putpixel(
                (x, 0), int(225. * (1. - float(gradientvalue) * float(x)/imgsize[0]))
                )

        gradient_image = ImageOps.colorize(
            gradientimage.resize((imgsize[0], imgsize[1])),
            color1, color2
            )
        image = RenderImage()
        image.SetAsImage(gradient_image.convert('RGBA'))
        self.NodeSetThumb(image.GetImage())
        return image

 
RegisterNode(NodeDefinition)