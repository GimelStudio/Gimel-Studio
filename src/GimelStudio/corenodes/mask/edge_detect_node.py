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
from PIL import ImageFilter

from GimelStudio import api
from GimelStudio.utils.image import ArrayFromImage, ArrayToImage


class EdgeDetectNode(api.NodeBase):
    def __init__(self, _id):
        api.NodeBase.__init__(self, _id)

    @property
    def NodeMeta(self):
        meta_info = {
            "label": "Edge Detect",
            "author": "iwoithe",
            "version": (0, 0, 1),
            "supported_app_version": (0, 5, 0),
            "category": "MASK",
            "description": "Detects the edges",
        }
        return meta_info

    def NodeInitProps(self):
        self.method = api.ChoiceProp(
            idname="Method",
            default="Canny",
            choices=["Find Edges", "Canny"],
            label="Method:"
        )

        self.lower_threshold = api.PositiveIntegerProp(
            idname="Lower Threshold",
            default=30,
            min_val=0,
            max_val=100,
            widget=api.SLIDER_WIDGET,
            label="Lower Threshold:"
        )

        self.higher_threshold = api.PositiveIntegerProp(
            idname="Higher Threshold",
            default=100,
            min_val=0,
            max_val=100,
            widget=api.SLIDER_WIDGET,
            label="Higher Threshold:"
        )

        self.NodeAddProp(self.method)
        self.NodeAddProp(self.lower_threshold)
        self.NodeAddProp(self.higher_threshold)

    def NodeInitParams(self):
        image = api.RenderImageParam("Image")
        self.NodeAddParam(image)

    def WidgetEventHook(self, idname, value):
        if idname == "Method" and value == "Find Edges":
            self.lower_threshold.SetIsVisible(False)
            self.higher_threshold.SetIsVisible(False)
        else:
            self.lower_threshold.SetIsVisible(True)
            self.higher_threshold.SetIsVisible(True)

        self.RefreshPropertyPanel()

    def NodeEvaluation(self, eval_info):
        input_image = eval_info.EvaluateParameter("Image")
        method = eval_info.EvaluateProperty("Method")
        lower_threshold = eval_info.EvaluateProperty("Lower Threshold")
        higher_threshold = eval_info.EvaluateProperty("Higher Threshold")

        image = api.RenderImage()

        # Consider removing the Pillow method?
        if method == "Find Edges":
            img = input_image.GetPILImage().convert("L").filter(ImageFilter.FIND_EDGES)
            image.SetAsImageFromPIL(img.convert("RGBA"))
        elif method == "Canny":
            input_image_array = input_image.GetImage()
            output_image_array = cv2.Canny(input_image_array, lower_threshold, higher_threshold)
            image.SetAsImage(output_image_array)
        else:
            image.SetAsImage(input_image.GetImage())

        self.NodeSetThumb(image.GetImage())
        return image


api.RegisterNode(EdgeDetectNode, "corenode_edgedetect")
