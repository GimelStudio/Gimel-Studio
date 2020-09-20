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

from PIL import ImageFilter

from GimelStudio import api

 
class BlurNode(api.NodeBase):
    def __init__(self, _id):
        api.NodeBase.__init__(self, _id)

    @property
    def NodeMeta(self):
        meta_info = {
            "label": "Blur",
            "author": "Correct Syntax",
            "version": (2, 2, 0),
            "supported_app_version": (0, 5, 0),
            "category": "FILTER",
            "description": "Blurs the given image using the specified blur radius.",
        }
        return meta_info

    def NodeInitProps(self):
        p = api.PositiveIntegerProp(
            idname="Radius", 
            default=1, 
            min_val=0, 
            max_val=25, 
            widget=api.SLIDER_WIDGET,
            label="Radius:",
            )
        self.NodeAddProp(p)

    def NodeInitParams(self):
        p = api.RenderImageParam('Image')

        self.NodeAddParam(p)

    def NodeEvaluation(self, eval_info):
        image1 = eval_info.EvaluateParameter('Image')
        radius = eval_info.EvaluateProperty('Radius')

        image = api.RenderImage()
        image.SetAsImage(image1.GetImage().filter(
            ImageFilter.GaussianBlur(radius)
            ).convert('RGBA'))

        self.NodeSetThumb(image.GetImage())
        return image


api.RegisterNode(BlurNode, "corenode_blur")