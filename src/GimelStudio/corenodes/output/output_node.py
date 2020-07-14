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

from PIL import Image

from GimelStudio.api import (Color, RenderImage, NodeBase, 
                            Parameter, RegisterNode)

class NodeDefinition(NodeBase):

    @property
    def NodeIDName(self):
        return "gimelstudiocorenode_outputcomposite"

    @property
    def NodeLabel(self):
        return "Output"

    @property
    def NodeCategory(self):
        return "OUTPUT"

    @property
    def NodeDescription(self):
        return """The most important node of them all. :) 
        This is registered here for the UI -the evaluation is handled elsewhere.
        This node should not be accessed by outside users.
        """  

    @property
    def NodeVersion(self):
        return "1.2" 

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
        pass


RegisterNode(NodeDefinition)
