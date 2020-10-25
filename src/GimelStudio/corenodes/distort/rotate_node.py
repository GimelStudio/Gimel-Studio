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
import wx.lib.agw.cubecolourdialog as CCD
from PIL import Image

from GimelStudio.api import (Color, RenderImage, List, NodeBase,
                            Parameter, Property, RegisterNode)


class NodeDefinition(NodeBase):

    @property
    def NodeIDName(self):
        return "gimelstudiocorenode_rotate"

    @property
    def NodeLabel(self):
        return "Rotate"

    @property
    def NodeCategory(self):
        return "DISTORT"

    @property
    def NodeDescription(self):
        return "Rotates the image."

    @property
    def NodeVersion(self):
        return "1.1"

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software"

    @property
    def NodeProperties(self):
        return [
            Property('Resample',
                prop_type='LIST',
                value=List([
                    'NEAREST',
                    'BILINEAR',
                    'BICUBIC',
                    ], 'NEAREST')
                ),

            Property('Size',
                prop_type='REGLIST',
                value=[256, 256]
                ),

            Property('Angle',
                prop_type='INTEGER',
                value=90
                ),

            Property('Fill Color',
                prop_type='COLOR',
                value=(0, 0, 0, 1)
                ),

            Property('Expand',
                prop_type='BOOLEAN',
                value=True
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

        # Angle
        current_angle_value = self.NodeGetPropValue('Angle')

        angle_label = wx.StaticText(parent, label="Angle:")
        sizer.Add(angle_label, flag=wx.TOP, border=5)

        self.angle_slider = wx.Slider(
            parent, wx.ID_ANY,
            value=current_angle_value,
            minValue=1, maxValue=360,
            style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
            )
        self.angle_slider.SetTickFreq(10)

        sizer.Add(self.angle_slider, flag=wx.EXPAND|wx.ALL, border=5)


        # Resample
        current_resample_value = self.NodeGetPropValue('Resample')

        resample_label = wx.StaticText(parent, label="Resample:")
        sizer.Add(resample_label, flag=wx.TOP, border=5)

        self.resample_combobox = wx.ComboBox(
            parent, wx.ID_ANY,
            value=current_resample_value,
            choices=[
                    'NEAREST',
                    'BILINEAR',
                    'BICUBIC',
                    ],
            style=wx.CB_READONLY
            )
        sizer.Add(self.resample_combobox, flag=wx.EXPAND|wx.ALL, border=5)


        # Color
        current_fillcolor_value = self.NodeGetPropValue('Fill Color')
        self.fillcolordata = wx.ColourData()
        self.fillcolordata.SetColour(current_fillcolor_value)

        fillcolor_label = wx.StaticText(parent, label="Fill color:")
        sizer.Add(fillcolor_label, flag=wx.TOP, border=5)

        color_vbox = wx.BoxSizer(wx.VERTICAL)
        color_hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.fillcolor_txtctrl = wx.TextCtrl(parent)
        self.fillcolor_txtctrl.ChangeValue(str(current_fillcolor_value))
        color_hbox.Add(self.fillcolor_txtctrl, proportion=1)

        self.fillcolor_btn = wx.Button(parent, label="Select...")
        color_hbox.Add(self.fillcolor_btn, flag=wx.LEFT, border=5)
        color_vbox.Add(color_hbox, flag=wx.EXPAND)

        sizer.Add(color_vbox, flag=wx.ALL|wx.EXPAND, border=5)


        # Expand
        current_expand_value = self.NodeGetPropValue('Expand')

        expand_label = wx.StaticText(parent, label="Expand:")
        sizer.Add(expand_label, flag=wx.TOP, border=5)

        self.expand_checkbox = wx.CheckBox(parent, id=wx.ID_ANY, label="Expand image to fit the entire rotated image")
        self.expand_checkbox.SetValue(current_expand_value)
        sizer.Add(self.expand_checkbox, flag=wx.EXPAND|wx.ALL, border=5)


        # Bindings
        parent.Bind(wx.EVT_COMBOBOX, self.OnResampleChange, self.resample_combobox)
        parent.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.OnAngleChange, self.angle_slider)
        parent.Bind(wx.EVT_CHECKBOX, self.OnExpandChange, self.expand_checkbox)
        parent.Bind(wx.EVT_BUTTON, self.OnFillColorChange, self.fillcolor_btn)


    def OnResampleChange(self, event):
        value = event.GetString()
        if not value:
            return
        self.NodePropertiesUpdate('Resample', value)

    def OnAngleChange(self, event):
        self.NodePropertiesUpdate('Angle', self.angle_slider.GetValue())

    def OnExpandChange(self, event):
        self.NodePropertiesUpdate('Expand', event.IsChecked())

    def OnFillColorChange(self, event):
        self.colordialog = CCD.CubeColourDialog(self.parent, self.fillcolordata)
        if self.colordialog.ShowModal() == wx.ID_OK:

            self.colordata = self.colordialog.GetColourData()
            colordata = self.fillcolordata.GetColour()
            self.NodePropertiesUpdate(
                'Fill Color',
                (colordata.Red(),
                 colordata.Green(),
                 colordata.Blue(),
                 colordata.Alpha())
                )
            self.fillcolor_txtctrl.ChangeValue(str((colordata.Red(),
                                                colordata.Green(),
                                                colordata.Blue(),
                                                colordata.Alpha()
                                                )))

    def NodeEvaluation(self, eval_info):
        image1 = eval_info.EvaluateParameter('Image')
        resample = eval_info.EvaluateProperty('Resample')
        angle = eval_info.EvaluateProperty('Angle')
        expand = eval_info.EvaluateProperty('Expand')
        fill_color = eval_info.EvaluateProperty('Fill Color')

        if resample == 'BILINEAR':
            RESAMPLE_VALUE = Image.BILINEAR

        elif resample == 'BICUBIC':
            RESAMPLE_VALUE = Image.BICUBIC

        elif resample == 'LANCZOS':
            RESAMPLE_VALUE = Image.LANCZOS

        else:
            RESAMPLE_VALUE = Image.NEAREST

        image = RenderImage()
        rotated_img = image1.GetImage().rotate(
            angle=int(angle),
            expand=expand,
            fillcolor=tuple(fill_color),
            resample=RESAMPLE_VALUE
        )
        image.SetAsImage(rotated_img)
        self.NodeSetThumb(image.GetImage())
        return image


RegisterNode(NodeDefinition)