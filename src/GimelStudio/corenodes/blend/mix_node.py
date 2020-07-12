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
from PIL import Image, ImageChops, ImageOps

from GimelStudio.api import (Color, RenderImage, List, NodeBase,
                            Parameter, Property, RegisterNode)
 

class NodeDefinition(NodeBase):

    @property
    def NodeIDName(self):
        return "gimelstudiocorenode_mix"

    @property
    def NodeLabel(self):
        return "Mix"

    @property
    def NodeCategory(self):
        return "BLEND"

    @property
    def NodeDescription(self):
        return "Blends two images together using the specified blend type." 

    @property
    def NodeVersion(self):
        return "1.8"  

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software" 

    @property
    def NodeParameters(self):
        return [
            Parameter('Image',
                param_type='RENDERIMAGE',
                default_value=RenderImage('RGBA', (256, 256), (0, 0, 0, 1))
                ),
            Parameter('Overlay',
                param_type='RENDERIMAGE',
                default_value=RenderImage('RGBA', (256, 256), (0, 0, 0, 1))
                ),
        ]

    @property
    def NodeProperties(self):
        return [
            Property('Blend Mode',
                prop_type='LIST',
                value=List(
                    items=[
                        'ADD',
                        'ADD MODULO',
                        'SUBTRACT',
                        'SUBTRACT MODULO',
                        'MULTIPLY',
                        'SCREEN',
                        'DIFFERENCE',
                        'DARKER',
                        'LIGHTER',
                        'SOFT LIGHT',
                        'HARD LIGHT',
                        'OVERLAY'
                    ], 
                    default='MULTIPLY'
                    )
                ),
        ]

    def NodePropertiesUI(self, node, parent, sizer):
        
        # Resample
        current_blend_type_value = self.NodeGetPropValue('Blend Mode')

        blendmodelabel = wx.StaticText(parent, label="Blend Mode:")
        sizer.Add(blendmodelabel, flag=wx.LEFT|wx.TOP, border=5)

        self.blendmodecombobox = wx.ComboBox(parent, 
            id=wx.ID_ANY, 
            value=current_blend_type_value, 
            choices=[
                    'ADD',
                    'ADD MODULO',
                    'SUBTRACT',
                    'SUBTRACT MODULO',
                    'MULTIPLY',
                    'SCREEN',
                    'DIFFERENCE',
                    'DARKER',
                    'LIGHTER',
                    'SOFT LIGHT',
                    'HARD LIGHT',
                    'OVERLAY'
                ], 
            style=wx.CB_READONLY
            )
        sizer.Add(self.blendmodecombobox, flag=wx.TOP|wx.EXPAND, border=5)

        # Bindings
        parent.Bind(wx.EVT_COMBOBOX, self.EvtChoice, self.blendmodecombobox)

    def EvtChoice(self, evt):
        value = evt.GetString()
        if not value:
            return
        self.NodePropertiesUpdate('Blend Mode', value)

    def NodeEvaluation(self, eval_info):
        image1 = eval_info.EvaluateParameter('Image')
        image2 = eval_info.EvaluateParameter('Overlay')
        blendmode = eval_info.EvaluateProperty('Blend Mode')

        image = RenderImage() 
        main_image = image1.GetImage()
        layer_image = ImageOps.fit(image2.GetImage(), main_image.size)

        if blendmode == 'ADD':
            img = ImageChops.add(main_image, layer_image)

        elif blendmode == 'ADD MODULO':
            img = ImageChops.add_modulo(main_image, layer_image)

        elif blendmode == 'SUBTRACT':
            img = ImageChops.subtract(main_image, layer_image)

        elif blendmode == 'SUBTRACT MODULO':
            img = ImageChops.subtract_modulo(main_image, layer_image)

        elif blendmode == 'MULTIPLY':
            img = ImageChops.multiply(main_image, layer_image)

        elif blendmode == 'SCREEN':
            img = ImageChops.screen(main_image, layer_image)

        elif blendmode == 'DIFFERENCE':
            img = ImageChops.difference(main_image, layer_image)
            
        elif blendmode == 'DARKER':
            img = ImageChops.darker(main_image, layer_image)

        elif blendmode == 'LIGHTER':
            img = ImageChops.lighter(main_image, layer_image)

        elif blendmode == 'SOFT LIGHT':
            img = ImageChops.soft_light(main_image, layer_image)

        elif blendmode == 'HARD LIGHT':
            img = ImageChops.hard_light(main_image, layer_image)

        elif blendmode == 'OVERLAY':
            img = ImageChops.overlay(main_image, layer_image)

        image.SetAsImage(img)
        self.NodeSetThumb(image.GetImage())
        return image


RegisterNode(NodeDefinition)