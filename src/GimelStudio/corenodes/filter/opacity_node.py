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

from PIL import ImageEnhance

from GimelStudio import api


class OpacityNode(api.NodeBase):
    def __init__(self, _id):
        api.NodeBase.__init__(self, _id)

    @property
    def NodeMeta(self):
        meta_info = {
            "label": "Opacity",
            "author": "Correct Syntax",
            "version": (1, 1, 0),
            "supported_app_version": (0, 5, 0),
            "category": "FILTER",
            "description": "Reduces the image transparency/opacity.",
        }
        return meta_info

    def NodeInitProps(self):
        p = api.PositiveIntegerProp(
            idname="Opacity",
            default=50,
            min_val=0,
            max_val=100,
            widget=api.SLIDER_WIDGET,
            label="Opacity:",
            )
        self.NodeAddProp(p)

    def NodeInitParams(self):
        p = api.RenderImageParam('Image')

        self.NodeAddParam(p)

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

        image = api.RenderImage()
        image.SetAsImage(img)
        self.NodeSetThumb(image.GetImage())
        return image


api.RegisterNode(OpacityNode, "corenode_opacity")
