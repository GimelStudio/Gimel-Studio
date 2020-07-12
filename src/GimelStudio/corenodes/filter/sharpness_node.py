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

import wx
import numpy as np
from PIL import Image, ImageEnhance

from GimelStudio.api import (Color, RenderImage, List, NodeBase, 
                            Parameter, Property, RegisterNode)

  
class NodeDefinition(NodeBase):
    
    @property
    def NodeIDName(self):
        return "gimelstudiocorenode_sharpness"

    @property
    def NodeLabel(self):
        return "Sharpness"

    @property
    def NodeCategory(self):
        return "FILTER"

    @property
    def NodeDescription(self):
        return "Sharpens the image by the given amount." 

    @property
    def NodeVersion(self):
        return "1.1" 

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software" 

    @property
    def NodeProperties(self):
        return [
            Property('Amount',
                prop_type='INTEGER',
                value=4
                ),
            ]

    @property
    def NodeParameters(self):
        return [
            Parameter('Image',
                param_type='RENDERIMAGE',
                default_value=RenderImage('RGBA', (256, 256), (0, 0, 0, 1))
                ),
        ]

   
    def NodePropertiesUI(self, node, parent, sizer):
        current_amount_value = self.NodeGetPropValue('Amount')

        sharpness_label = wx.StaticText(parent, label="Sharpness amount:")
        sizer.Add(sharpness_label, border=5)

        self.sharpness_slider = wx.Slider(
            parent, 100, 25, 1, 100,
            style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
            )
        self.sharpness_slider.SetTickFreq(5)
        self.sharpness_slider.SetRange(1, 100)
        self.sharpness_slider.SetValue(current_amount_value)
        sizer.Add(self.sharpness_slider, flag=wx.EXPAND|wx.ALL, border=5)

        parent.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.OnSharpnessChange, self.sharpness_slider)

 
    def OnSharpnessChange(self, event):
        self.NodePropertiesUpdate('Amount', self.sharpness_slider.GetValue())
    
    def NodeEvaluation(self, eval_info):
        image1  = eval_info.EvaluateParameter('Image')
        sharpness_amount = eval_info.EvaluateProperty('Amount')

        image = RenderImage()
        enhancer = ImageEnhance.Sharpness(image1.GetImage())
        image.SetAsImage(enhancer.enhance(sharpness_amount).convert('RGBA'))
        self.NodeSetThumb(image.GetImage())
        return image

 
RegisterNode(NodeDefinition)
