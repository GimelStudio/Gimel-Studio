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

import cv2
import wx
from PIL import Image

from GimelStudio.api import (Color, RenderImage, List, NodeBase, 
                            Parameter, Property, RegisterNode)

from GimelStudio.utils.image import ArrayFromImage, ArrayToImage

  
class NodeDefinition(NodeBase):
    
    @property
    def NodeIDName(self):
        return "gimelstudiocorenode_invert"

    @property
    def NodeLabel(self):
        return "Invert"

    @property
    def NodeCategory(self):
        return "COLOR"

    @property
    def NodeDescription(self):
        return "Inverts the channels of an image." 

    @property
    def NodeVersion(self):
        return "1.0" 

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
        ]

    def NodeEvaluation(self, eval_info):
        image1  = eval_info.EvaluateParameter('Image')

        image = RenderImage()
        image.SetAsImage(ArrayToImage(cv2.bitwise_not(ArrayFromImage(image1.GetImage()))).convert('RGBA'))
        self.NodeSetThumb(image.GetImage())
        return image

  
RegisterNode(NodeDefinition)
