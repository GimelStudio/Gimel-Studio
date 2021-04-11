## THIS FILE IS A PART OF GIMEL STUDIO AND IS LICENSED UNDER THE SAME TERMS:
## ----------------------------------------------------------------------------
## Gimel Studio Copyright 2019-2020 by Noah Rahm and contributors
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
import numpy as np

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
            "version": (0, 0, 2),
            "supported_app_version": (0, 5, 0),
            "category": "DISTORT",
            "description": "Crops the image",
        }
        return meta_info

    def NodeInitProps(self):
        # General
        self.method = api.ChoiceProp(
            idname="Method",
            default="Rectangle",
            choices=["Rectangle", "Circle"],
            label="Method:"
        )

        self.NodeAddProp(self.method)

        # Rectangle
        self.x = api.PositiveIntegerProp(idname="X",
                                         default=0,
                                         min_val=0,
                                         max_val=100000,
                                         widget=api.SPINBOX_WIDGET,
                                         label="X:")

        self.y = api.PositiveIntegerProp(idname="Y",
                                         default=0,
                                         min_val=0,
                                         max_val=100000,
                                         widget=api.SPINBOX_WIDGET,
                                         label="Y:")

        self.width = api.PositiveIntegerProp(idname="Width",
                                             default=255,
                                             min_val=1,
                                             max_val=100000,
                                             widget=api.SPINBOX_WIDGET,
                                             label="Width:")

        self.height = api.PositiveIntegerProp(idname="Height",
                                              default=255,
                                              min_val=1,
                                              max_val=100000,
                                              widget=api.SPINBOX_WIDGET,
                                              label="Height:")

        self.NodeAddProp(self.x)
        self.NodeAddProp(self.y)
        self.NodeAddProp(self.width)
        self.NodeAddProp(self.height)

        # Circle
        self.center = api.SizeProp(idname="Center",
                                   default=[255, 255],
                                   min_val=0,
                                   max_val=100000,
                                   label="Center:",
                                   visible=False)

        self.radius = api.PositiveIntegerProp(idname="Radius",
                                              default=255,
                                              min_val=1,
                                              max_val=100000,
                                              widget=api.SPINBOX_WIDGET,
                                              label="Radius:",
                                              visible=False)

        self.NodeAddProp(self.center)
        self.NodeAddProp(self.radius)

    def WidgetEventHook(self, idname, value):
        if idname == "Method" and value == "Rectangle":
            # Show rectangle properties
            self.x.SetIsVisible(True)
            self.y.SetIsVisible(True)
            self.width.SetIsVisible(True)
            self.height.SetIsVisible(True)
            # Hide circle properties
            self.center.SetIsVisible(False)
            self.radius.SetIsVisible(False)
            self.RefreshPropertyPanel()
        elif idname == "Method" and value == "Circle":
            # Hide rectangle properties
            self.x.SetIsVisible(False)
            self.y.SetIsVisible(False)
            self.width.SetIsVisible(False)
            self.height.SetIsVisible(False)
            # Show circle properties
            self.center.SetIsVisible(True)
            self.radius.SetIsVisible(True)

            self.RefreshPropertyPanel()


    def NodeInitParams(self):
        p = api.RenderImageParam('Image')

        self.NodeAddParam(p)

    def NodeEvaluation(self, eval_info):
        # TODO: Add a circle crop option
        input_image = eval_info.EvaluateParameter('Image')

        method = eval_info.EvaluateProperty("Method")
        # Rectangle
        x = eval_info.EvaluateProperty("X")
        y = eval_info.EvaluateProperty("Y")
        width = eval_info.EvaluateProperty("Width")
        height = eval_info.EvaluateProperty("Height")
        # Circle
        center = eval_info.EvaluateProperty("Center")
        radius = eval_info.EvaluateProperty("Radius")

        input_image_array = ArrayFromImage(input_image.GetImage())
        if method == "Rectangle":
            output_image_array = input_image_array[y:y + height, x:x + width]
        else:
            # Create a blank mask
            mask = np.zeros(shape=input_image_array.data.shape, dtype=np.uint8)
            # Create the circle
            circle_mask_colour = cv2.circle(mask, tuple(center), radius, (255, 255, 255), -1)
            # Convert the mask to gray scale
            circle_mask = cv2.cvtColor(circle_mask_colour, cv2.COLOR_BGR2GRAY)
            # Combine the mask and image
            cropped_img = cv2.bitwise_and(input_image_array, input_image_array, mask=circle_mask)

            # Crop the circle
            circle_rect = cropped_img[center[1] - radius:center[1] + radius, center[0] - radius:center[0] + radius]
            output_image_array = circle_rect

        image = api.RenderImage()

        image.SetAsImage(ArrayToImage(output_image_array).convert("RGBA"))

        self.NodeSetThumb(image.GetImage().convert("RGBA"))
        return image

api.RegisterNode(CropNode, "corenode_crop")