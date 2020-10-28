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


from PIL import ImageOps

from GimelStudio import api


class InvertNode(api.NodeBase):
    def __init__(self, _id):
        api.NodeBase.__init__(self, _id)

    @property
    def NodeMeta(self):
        meta_info = {
            "label": "Invert",
            "author": "iwoithe",
            "version": (0, 0, 1),
            "supported_app_version": (0, 5, 0),
            "category": "FILTER",
            "description": "Inverts the image.",
        }
        return meta_info

    def NodeInitParams(self):
        image = api.RenderImageParam("Image")
        self.NodeAddParam(image)

    def NodeEvaluation(self, eval_info):
        image1 = eval_info.EvaluateParameter('Image')

        image = api.RenderImage()

        image.SetAsImage(ImageOps.invert(image1.GetImage().convert("RGB")))

        self.NodeSetThumb(image.GetImage())
        return image


api.RegisterNode(InvertNode, "corenode_invert")