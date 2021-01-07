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

from GimelStudio import api
from GimelStudio.renderer import EvalInfo


class NoiseImageNode(api.NodeBase):
    def __init__(self, _id):
        api.NodeBase.__init__(self, _id)

    @property
    def NodeMeta(self):
        meta_info = {
            "label": "Noise Image",
            "author": "Correct Syntax",
            "version": (1, 1, 5),
            "supported_app_version": (0, 5, 0),
            "category": "INPUT",
            "description": "Generates a Gaussian noise image centered around 128."
        }
        return meta_info

    def NodeInitProps(self):
        self.sigma_prop = api.PositiveIntegerProp(
            idname="Sigma",
            default=50,
            min_val=1,
            max_val=400,
            widget=api.SLIDER_WIDGET,
            label="Sigma:",
        )
        self.size_prop = api.SizeProp(
            idname="Size",
            default=[255, 255],
            label="Image Size:"
        )

        self.NodeAddProp(self.sigma_prop)
        self.NodeAddProp(self.size_prop)

    def WidgetEventHook(self, idname, value):
        img = self.NodeEvaluation(EvalInfo(self)).GetImage()
        self.NodeSetThumb(img, force_refresh=True)
        self.RefreshPropertyPanel()

    def NodeEvaluation(self, eval_info):
        sigma = eval_info.EvaluateProperty('Sigma')
        imgsize = eval_info.EvaluateProperty('Size')

        image = api.RenderImage()
        image.SetAsImageFromPIL(
            Image.effect_noise((imgsize[0], imgsize[1]), sigma)
        )
        self.NodeSetThumb(image.GetImage())
        return image


api.RegisterNode(NoiseImageNode, "corenode_noiseimage")
