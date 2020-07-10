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
        return "corenode_opacity"

    @property
    def NodeLabel(self):
        return "Opacity"

    @property
    def NodeCategory(self):
        return "FILTER"

    @property
    def NodeDescription(self):
        return "Reduces the image transparency/opacity." 

    @property
    def NodeVersion(self):
        return "1.0" 

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software" 

    @property
    def NodeProperties(self):
        return [
            Property('Opacity',
                prop_type='INTEGER',
                value=50
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
        current_radius_value = self.NodeGetPropValue('Opacity')

        radius_label = wx.StaticText(parent, label="Opacity:")
        sizer.Add(radius_label, border=5)

        self.radiusspinctrl = wx.Slider(
            parent, 100, 25, 1, 100,
            style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
            )
        self.radiusspinctrl.SetTickFreq(5)

        self.radiusspinctrl.SetRange(1, 100)
        self.radiusspinctrl.SetValue(current_radius_value)
        sizer.Add(self.radiusspinctrl, flag=wx.EXPAND|wx.ALL, border=5)

        parent.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.OnRadiusSpin, self.radiusspinctrl)

 
    def OnRadiusSpin(self, evt):
        self.NodePropertiesUpdate('Opacity', self.radiusspinctrl.GetValue())
    
    def NodeEvaluation(self, eval_info):
        image1  = eval_info.EvaluateParameter('Image')
        opacity = eval_info.EvaluateProperty('Opacity')

        img = image1.GetImage().convert("RGBA")
 
        # Make correction for slider range of 1-100
        image_opacity = (opacity*0.01)

        # Only reduce the opacity if the value is acceptable
        if not image_opacity < 0 or not image_opacity > 1:
            alpha = ImageEnhance.Brightness(img.split()[-1]).enhance(image_opacity)
            img.putalpha(alpha)
        
        image = RenderImage()
        image.SetAsImage(img)
        self.NodeSetThumb(image.GetImage())
        return image

 
RegisterNode(NodeDefinition)
