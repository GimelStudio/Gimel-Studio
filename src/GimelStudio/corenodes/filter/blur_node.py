# THIS FILE IS A PART OF GIMEL STUDIO AND IS LICENSED UNDER THE SAME TERMS:
# ----------------------------------------------------------------------------
# Gimel Studio Copyright 2019-2020 by Noah Rahm and contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------------

import cv2

from GimelStudio import api
from GimelStudio.utils.image import ArrayFromImage, ArrayToImage


class BlurNode(api.NodeBase):
    def __init__(self, _id):
        api.NodeBase.__init__(self, _id)

    @property
    def NodeMeta(self):
        meta_info = {
            "label": "Blur",
            "author": "Correct Syntax",
            "version": (2, 5, 0),
            "supported_app_version": (0, 5, 0),
            "category": "FILTER",
            "description": "Blurs the given image using the specified blur type and kernel.",
        }
        return meta_info

    def NodeInitProps(self):
        self.filter_type = api.ChoiceProp(
            idname="Filter Type",
            default="Box",
            choices=["Box", "Gaussian"],
            label="Filter Type:"
        )
        self.kernel_x = api.PositiveIntegerProp(
            idname="Kernel X",
            default=5,
            min_val=1,
            max_val=500,
            widget=api.SLIDER_WIDGET,
            label="Kernel X:",
        )
        self.kernel_y = api.PositiveIntegerProp(
            idname="Kernel Y",
            default=5,
            min_val=1,
            max_val=500,
            widget=api.SLIDER_WIDGET,
            label="Kernel Y:",
        )
        self.NodeAddProp(self.filter_type)
        self.NodeAddProp(self.kernel_x)
        self.NodeAddProp(self.kernel_y)

    def NodeInitParams(self):
        image = api.RenderImageParam('Image')

        self.NodeAddParam(image)

    def NodeEvaluation(self, eval_info):
        image1 = eval_info.EvaluateParameter('Image')
        kernel_x = eval_info.EvaluateProperty('Kernel X')
        kernel_y = eval_info.EvaluateProperty('Kernel Y')
        filter_type = eval_info.EvaluateProperty('Filter Type')

        image = api.RenderImage()

        img = image1.GetImage()

        if filter_type == "Box":
            output_img = cv2.boxFilter(img, -1, (kernel_x, kernel_y))
        elif filter_type == "Gaussian":

            # Both values must be odd
            if (kernel_x % 2) == 0 and (kernel_y % 2) == 0:
                kernel_y += 1
                kernel_x += 1

            output_img = cv2.GaussianBlur(
                img, (0, 0), sigmaX=kernel_x, sigmaY=kernel_y
            )

        image.SetAsImage(output_img)

        self.NodeSetThumb(image.GetImage())
        return image


api.RegisterNode(BlurNode, "corenode_blur")
