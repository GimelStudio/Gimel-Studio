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
from PIL import Image, ImageFilter

from GimelStudio.api import (Color, RenderImage, List, NodeBase, ParameterDefinition,
                         PropertyDefinition, RegisterNode)

 
class NodeDefinition(NodeBase):
    
    @property
    def NodeIDName(self):
        return "corenode_blur"

    @property
    def NodeLabel(self):
        return "Blur"

    @property
    def NodeCategory(self):
        return "FILTER"

    @property
    def NodeDescription(self):
        return "Blurs the given image using the specified blur radius." 

    @property
    def NodeVersion(self):
        return "2.1" 

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software" 

    @property
    def NodeProperties(self):
        return [
            PropertyDefinition('Radius',
                               prop_type='INTEGER',
                               value=2
                               ),
            ]

    @property
    def NodeParameters(self):
        return [
            ParameterDefinition('Image',
                                param_type='RENDERIMAGE',
                                default_value=RenderImage('RGBA', (256, 256), (0, 0, 0, 1))),
        ]

   
    def NodePropertiesUI(self, node, parent, sizer):
        current_radius_value = self.NodeGetPropertyValue('Radius')

        radius_label = wx.StaticText(parent, label="Blur Radius:")
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
        self.NodePropertiesUpdate('Radius', self.radiusspinctrl.GetValue())
    
    def NodeEvaluation(self, eval_info):
        image1  = eval_info.EvaluateParameter('Image')
        radius = eval_info.EvaluateProperty('Radius')
        
        image = RenderImage()
        image.SetAsImage(image1.GetImage().filter(
            ImageFilter.GaussianBlur(radius)
            ).convert('RGBA'))
        self.NodeSetThumb(image.GetImage())
        return image

 
RegisterNode(NodeDefinition)
