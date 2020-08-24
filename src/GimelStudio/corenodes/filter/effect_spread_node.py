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
from PIL import Image

from GimelStudio.api import (Color, RenderImage, List, NodeBase, 
                            Parameter, Property, RegisterNode)

 
class NodeDefinition(NodeBase):
    
    @property
    def NodeIDName(self):
        return "gimelstudiocorenode_effectspread"

    @property
    def NodeLabel(self):
        return "Effect Spread"

    @property
    def NodeCategory(self):
        return "FILTER"

    @property
    def NodeDescription(self):
        return "Randomly spreads the pixels in the image." 

    @property
    def NodeVersion(self):
        return "1.0" 

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software" 

    @property
    def NodeProperties(self):
        return [
            Property('Distance',
                prop_type='INTEGER',
                value=10
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
        current_distance_value = self.NodeGetPropValue('Distance')

        distance_label = wx.StaticText(parent, label="Spread Distance:")
        sizer.Add(distance_label, border=5)

        self.distance_slider = wx.Slider(
            parent, wx.ID_ANY,
            style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
            )
        self.distance_slider.SetTickFreq(5)
        self.distance_slider.SetRange(1, 200)
        self.distance_slider.SetValue(current_distance_value)
        sizer.Add(self.distance_slider, flag=wx.EXPAND|wx.ALL, border=5)

        parent.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.OnDistanceChange, self.distance_slider)

 
    def OnDistanceChange(self, evt):
        self.NodePropertiesUpdate('Distance', self.distance_slider.GetValue())
    
    def NodeEvaluation(self, eval_info):
        image1  = eval_info.EvaluateParameter('Image')
        distance = eval_info.EvaluateProperty('Distance')

        image = RenderImage()
        image.SetAsImage(image1.GetImage().effect_spread(distance))
        self.NodeSetThumb(image.GetImage())
        return image

 
RegisterNode(NodeDefinition)
