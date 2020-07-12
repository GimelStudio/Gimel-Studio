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
from PIL import Image, ImageOps

from GimelStudio.api import (Color, RenderImage, List, NodeBase,
                            Parameter, Property, RegisterNode)
 

class NodeDefinition(NodeBase):

    @property
    def NodeIDName(self):
        return "gimelstudiocorenode_alphacomposite"

    @property
    def NodeLabel(self):
        return "Alpha Composite"

    @property
    def NodeCategory(self):
        return "BLEND"

    @property
    def NodeDescription(self):
        return "Alpha composites two images based on the alpha of\n the given mask." 

    @property
    def NodeVersion(self):
        return "1.1"  

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software" 

    @property
    def NodeParameters(self):
        return [
            Parameter('Image 1',
                param_type='RENDERIMAGE',
                default_value=RenderImage('RGBA', (256, 256), (0, 0, 0, 1))
                ),
            Parameter('Image 2',
                param_type='RENDERIMAGE',
                default_value=RenderImage('RGBA', (256, 256), (0, 0, 0, 1))
                ),
            Parameter('Mask',
                param_type='RENDERIMAGE',
                default_value=RenderImage('RGBA', (256, 256), (0, 0, 0, 1))
                ),
        ]

    def NodeEvaluation(self, eval_info):
        image1 = eval_info.EvaluateParameter('Image 1')
        image2 = eval_info.EvaluateParameter('Image 2')
        mask = eval_info.EvaluateParameter('Mask')

        image = RenderImage() 
        main_image = image1.GetImage()
        layer_image = ImageOps.fit(image2.GetImage(), main_image.size)
        mask_image = ImageOps.fit(mask.GetImage(), main_image.size).convert('RGBA')
        
        image.SetAsImage(Image.composite(main_image, layer_image, mask_image))
        self.NodeSetThumb(image.GetImage())
        return image


RegisterNode(NodeDefinition)