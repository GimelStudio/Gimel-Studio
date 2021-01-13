## THIS FILE IS A PART OF GIMEL STUDIO AND IS LICENSED UNDER THE SAME TERMS:
## ----------------------------------------------------------------------------
## Gimel Studio Copyright 2019-2021 by Noah Rahm and contributors
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

from GimelStudio import api
from GimelStudio.utils.image import ArrayToImage, ArrayFromImage


class CropNode(api.NodeBase):
    def __init__(self, _id):
        api.NodeBase.__init__(self, _id)

    @property
    def NodeMeta(self):
        meta_info = {
            "label": "Crop",
            "author": "iwoithe",
            "version": (0, 0, 1),
            "supported_app_version": (0, 5, 0),
            "category": "DISTORT",
            "description": "Crops the image",
        }
        return meta_info

    def NodeInitProps(self):
        x = api.PositiveIntegerProp(idname="X",
                                    default=0,
                                    min_val=0,
                                    max_val=100000,
                                    widget=api.SPINBOX_WIDGET,
                                    label="X:")

        y = api.PositiveIntegerProp(idname="Y",
                                    default=0,
                                    min_val=0,
                                    max_val=100000,
                                    widget=api.SPINBOX_WIDGET,
                                    label="Y:")

        width = api.PositiveIntegerProp(idname="Width",
                                    default=255,
                                    min_val=1,
                                    max_val=100000,
                                    widget=api.SPINBOX_WIDGET,
                                    label="Width:")

        height = api.PositiveIntegerProp(idname="Height",
                                    default=255,
                                    min_val=1,
                                    max_val=100000,
                                    widget=api.SPINBOX_WIDGET,
                                    label="Height:")

        self.NodeAddProp(x)
        self.NodeAddProp(y)
        self.NodeAddProp(width)
        self.NodeAddProp(height)

    def NodeInitParams(self):
        p = api.RenderImageParam('Image')

        self.NodeAddParam(p)

    def NodeEvaluation(self, eval_info):
        # TODO: Add a circle crop option
        input_image = eval_info.EvaluateParameter('Image')
        x = eval_info.EvaluateProperty("X")
        y = eval_info.EvaluateProperty("Y")
        width = eval_info.EvaluateProperty("Width")
        height = eval_info.EvaluateProperty("Height")

        input_image_array = ArrayFromImage(input_image.GetImage())
        output_image_array = input_image_array[y:y + height, x:x + width]

        image = api.RenderImage()

        image.SetAsImage(ArrayToImage(output_image_array).convert("RGBA"))

        self.NodeSetThumb(image.GetImage().convert("RGBA"))
        return image

api.RegisterNode(CropNode, "corenode_crop")