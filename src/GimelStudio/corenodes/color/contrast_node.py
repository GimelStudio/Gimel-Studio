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
        return "corenode_contrast"

    @property
    def NodeLabel(self):
        return "Contrast"

    @property
    def NodeCategory(self):
        return "COLOR"

    @property
    def NodeDescription(self):
        return "Adjusts the image contrast." 

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
                value=1
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

        contrast_label = wx.StaticText(parent, label="Contrast amount:")
        sizer.Add(contrast_label, border=5)

        self.contrast_slider = wx.Slider(
            parent, wx.ID_ANY, 
            value=current_amount_value,
            minValue=1, maxValue=10,
            style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
            )
        self.contrast_slider.SetTickFreq(1)

        sizer.Add(self.contrast_slider, flag=wx.EXPAND|wx.ALL, border=5)

        parent.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.OnContrastChange, self.contrast_slider)

 
    def OnContrastChange(self, event):
        self.NodePropertiesUpdate('Amount', self.contrast_slider.GetValue())
    
    def NodeEvaluation(self, eval_info):
        image1  = eval_info.EvaluateParameter('Image')
        contrast_amount = eval_info.EvaluateProperty('Amount')

        image = RenderImage()
        enhancer = ImageEnhance.Contrast(image1.GetImage())
        image.SetAsImage(enhancer.enhance(contrast_amount).convert('RGBA'))
        self.NodeSetThumb(image.GetImage())
        return image

 
RegisterNode(NodeDefinition)
