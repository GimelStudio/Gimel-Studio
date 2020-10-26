## THIS FILE IS A PART OF GIMEL STUDIO AND IS LICENSED UNDER THE SAME TERMS:
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
## ----------------------------------------------------------------------------

import os

import wx
from PIL import Image

from GimelStudio.api import (Color, RenderImage, List, NodeBase,
                            Parameter, Property, RegisterNode)


class NodeDefinition(NodeBase):

    @property
    def NodeIDName(self):
        return "gimelstudiocorenode_resize"

    @property
    def NodeLabel(self):
        return "Resize"

    @property
    def NodeCategory(self):
        return "DISTORT"

    @property
    def NodeDescription(self):
        return "Resizes the image dimensions."

    @property
    def NodeVersion(self):
        return "1.2"

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software"

    @property
    def NodeProperties(self):
        return [
            Property('Resample',
                prop_type='LIST',
                value=List([
                    'Nearest',
                    'Antialias',
                    'Box',
                    'Bilinear',
                    'Hamming',
                    'Bicubic',
                    'Lanczos'
                    ], 'Nearest')
                ),

            Property('Size',
                prop_type='REGLIST',
                value=[256, 256]
                ),
            ]

    @property
    def NodeParameters(self):
        return [
            Parameter('Image',
                param_type='RENDERIMAGE',
                default_value=RenderImage('RGBA', (256, 256), (0, 0, 0, 1))),
        ]


    def NodePropertiesUI(self, node, parent, sizer):

        # Resample
        current_resample_value = self.NodeGetPropValue('Resample')

        resample_label = wx.StaticText(parent, label="Resample:")
        sizer.Add(resample_label, border=5)

        self.resample_combobox = wx.ComboBox(
            parent, wx.ID_ANY,
            value=current_resample_value,
            choices=[
                    'Nearest',
                    'Antialias',
                    'Box',
                    'Bilinear',
                    'Hamming',
                    'Bicubic',
                    'Lanczos'
                    ],
            style=wx.CB_READONLY
            )
        sizer.Add(self.resample_combobox, flag=wx.EXPAND|wx.ALL, border=5)

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
        parent.Bind(wx.EVT_COMBOBOX, self.OnResampleChange, self.resample_combobox)
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

    def OnResampleChange(self, event):
        value = event.GetString()
        if not value:
            return
        self.NodePropertiesUpdate('Resample', value)


    def NodeEvaluation(self, eval_info):
        image1 = eval_info.EvaluateParameter('Image')

        resample = eval_info.EvaluateProperty('Resample')
        size = eval_info.EvaluateProperty('Size')

        if resample == 'Antialias':
            RESIZE_RESAMPLE = Image.ANTIALIAS

        elif resample == 'Box':
            RESIZE_RESAMPLE = Image.BOX

        elif resample == 'Bilinear':
            RESIZE_RESAMPLE = Image.BILINEAR

        elif resample == 'Hamming':
            RESIZE_RESAMPLE = Image.HAMMING

        elif resample == 'Bicubic':
            RESIZE_RESAMPLE = Image.BICUBIC

        elif resample == 'Lanczos':
            RESIZE_RESAMPLE = Image.LANCZOS

        else:
            RESIZE_RESAMPLE = Image.NEAREST

        image = RenderImage()
        image.SetAsImage(
            image1.GetImage().resize((size[0], size[1]),
            resample=RESIZE_RESAMPLE)
            )
        self.NodeSetThumb(image.GetImage())
        return image


RegisterNode(NodeDefinition)