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

import os
from PIL import Image, ImageOps
import OpenImageIO as oiio
from OpenImageIO import ImageBuf, ImageSpec, ImageBufAlgo

from GimelStudio import api
from GimelStudio.renderer import EvalInfo


class GradientImageNode(api.NodeBase):
    def __init__(self, _id):
        api.NodeBase.__init__(self, _id)

    @property
    def NodeMeta(self):
        meta_info = {
            "label": "Gradient Image",
            "author": "Correct Syntax",
            "version": (1, 1, 0),
            "supported_app_version": (0, 5, 0),
            "category": "INPUT",
            "description": "Creates a blank image with a gradient from one color to another."
        }
        return meta_info

    def NodeInitProps(self):
        self.gradienttype_prop = api.ChoiceProp(
            idname="Gradient Type",
            default="Linear",
            label="Gradient Type:",
            choices=[
                    'Linear',
                    'Interpolated',
            ]
        )
        self.color1_prop = api.ColorProp(
            idname="Color 1",
            default=(0, 0, 0, 255),
            label="Gradient Color 1:"
        )
        self.color2_prop = api.ColorProp(
            idname="Color 2",
            default=(255, 255, 255, 255),
            label="Gradient Color 2:"
        )
        self.color3_prop = api.ColorProp(
            idname="Color 3",
            default=(0, 0, 0, 255),
            label="Gradient Color 3:"
        )
        self.color4_prop = api.ColorProp(
            idname="Color 4",
            default=(0, 0, 0, 255),
            label="Gradient Color 4:"
        )
        self.size_prop = api.SizeProp(
            idname="Size",
            default=[255, 255],
            label="Image Size:"
        )

        self.NodeAddProp(self.gradienttype_prop)
        self.NodeAddProp(self.size_prop)
        self.NodeAddProp(self.color1_prop)
        self.NodeAddProp(self.color2_prop)
        self.NodeAddProp(self.color3_prop)
        self.NodeAddProp(self.color4_prop)

        # By default hide color 3 and 4
        self.color3_prop.SetIsVisible(False)
        self.color4_prop.SetIsVisible(False)


    def WidgetEventHook(self, idname, value):
        if idname in ["Gradient Type"] and value == "Linear":
            self.color3_prop.SetIsVisible(False)
            self.color4_prop.SetIsVisible(False)
        else:
            self.color3_prop.SetIsVisible(True)
            self.color4_prop.SetIsVisible(True)

        img = self.NodeEvaluation(EvalInfo(self)).GetImage()
        self.NodeSetThumb(img, force_refresh=True)
        self.RefreshPropertyPanel()

    def NodeEvaluation(self, eval_info):
        gradienttype = eval_info.EvaluateProperty('Gradient Type')
        color1 = eval_info.EvaluateProperty('Color 1')
        color2 = eval_info.EvaluateProperty('Color 2')
        color3 = eval_info.EvaluateProperty('Color 3')
        color4 = eval_info.EvaluateProperty('Color 4')
        imgsize = eval_info.EvaluateProperty('Size')

        if gradienttype == "Linear":
            buf = ImageBuf(ImageSpec(imgsize[0], imgsize[1], 4, oiio.FLOAT))
            ImageBufAlgo.fill(buf, color1, color2)
        elif gradienttype == "Interpolated":
            buf = ImageBuf(ImageSpec(imgsize[0], imgsize[1], 4, oiio.FLOAT))
            ImageBufAlgo.fill(buf, color1, color2, color3, color4)

        gradient_image = ImageBuf.get_pixels(buf).astype("uint8")

        image = api.RenderImage()
        image.SetAsImage(gradient_image)
        self.NodeSetThumb(image.GetImage())
        return image


api.RegisterNode(GradientImageNode, "corenode_gradientimage")
