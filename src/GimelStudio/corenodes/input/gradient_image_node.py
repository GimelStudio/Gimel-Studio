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

import os
from PIL import Image, ImageOps

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
        self.size_prop = api.SizeProp(
            idname="Size",
            default=[255, 255],
            label="Image Size:"
            )

        self.NodeAddProp(self.color1_prop)
        self.NodeAddProp(self.color2_prop)
        self.NodeAddProp(self.size_prop)

    def WidgetEventHook(self, idname, value):
        if idname in ["Color 1", "Color 2"]:
            img = self.NodeEvaluation(EvalInfo(self)).GetImage()
            self.NodeSetThumb(img, force_refresh=True)
            self.RefreshPropertyPanel()

    def NodeEvaluation(self, eval_info):
        gradient = 0.5#eval_info.EvaluateProperty('Gradient')
        color1 = eval_info.EvaluateProperty('Color 1')
        color2 = eval_info.EvaluateProperty('Color 2')
        imgsize = eval_info.EvaluateProperty('Size')

        gradientimage = Image.new("L", (imgsize[0], 1))
        for x in range(imgsize[0]):
            gradientimage.putpixel(
                (x, 0), int(225. * (1. - float(gradient) * float(x)/imgsize[0]))
                )

        gradient_image = ImageOps.colorize(
            gradientimage.resize((imgsize[0], imgsize[1])),
            color1, color2
            )
        image = api.RenderImage()
        image.SetAsImage(gradient_image.convert('RGBA'))
        self.NodeSetThumb(image.GetImage())
        return image


api.RegisterNode(GradientImageNode, "corenode_gradientimage")