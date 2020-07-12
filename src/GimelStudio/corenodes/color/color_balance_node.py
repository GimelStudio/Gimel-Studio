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
from PIL import Image, ImageEnhance

from GimelStudio.api import (Color, RenderImage, List, NodeBase, 
                            Parameter, Property, RegisterNode)

  
class NodeDefinition(NodeBase):
    
    @property
    def NodeIDName(self):
        return "gimelstudiocorenode_colorbalance"

    @property
    def NodeLabel(self):
        return "Color Balance"

    @property
    def NodeCategory(self):
        return "COLOR"

    @property
    def NodeDescription(self):
        return "Adjusts the image color balance." 

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

        colorbalance_label = wx.StaticText(parent, label="Color balance amount:")
        sizer.Add(colorbalance_label, border=5)

        self.colorbalance_slider = wx.Slider(
            parent, wx.ID_ANY, 
            value=current_amount_value,
            minValue=1, maxValue=10,
            style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
            )
        self.colorbalance_slider.SetTickFreq(1)

        sizer.Add(self.colorbalance_slider, flag=wx.EXPAND|wx.ALL, border=5)

        parent.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.OnColorBalanceChange, self.colorbalance_slider)

 
    def OnColorBalanceChange(self, event):
        self.NodePropertiesUpdate('Amount', self.colorbalance_slider.GetValue())
    
    def NodeEvaluation(self, eval_info):
        image1  = eval_info.EvaluateParameter('Image')
        contrast_amount = eval_info.EvaluateProperty('Amount')

        image = RenderImage()
        enhancer = ImageEnhance.Color(image1.GetImage())
        image.SetAsImage(enhancer.enhance(contrast_amount).convert('RGBA'))
        self.NodeSetThumb(image.GetImage())
        return image

 
RegisterNode(NodeDefinition)
