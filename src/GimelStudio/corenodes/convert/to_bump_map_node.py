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

import cv2
import numpy as np

from GimelStudio import api

# FIXME: hack! 
from GimelStudio.utils.image import ArrayFromImage, ArrayToImage


class ToBumpMapNode(api.NodeBase):
    def __init__(self, _id):
        api.NodeBase.__init__(self, _id)

    def GammaCorrection(self, image, gamma):
        """ Corrects gamma of image. """
        inv_gamma = 1 / gamma
        table = np.array(
            [((i / 255) ** inv_gamma) * 255 for i in range(0, 256)]
            ).astype("uint8")
        return cv2.LUT(image, table)   

    def ComputeBumpMap(self, image, saturation, brightness, gamma):
        """ Calculates and returns a bump map. """
        gray_scale_img = cv2.bitwise_not(image)
        bump_map = cv2.convertScaleAbs(
            gray_scale_img, 
            alpha=saturation, 
            beta=brightness
            )
        gc_bump_map = self.GammaCorrection(bump_map, gamma)
        return gc_bump_map

    @property
    def NodeMeta(self):
        meta_info = {
            "label": "To Bump Map",
            "author": "Correct Syntax",
            "version": (1, 2, 0),
            "supported_app_version": (0, 5, 0),
            "category": "CONVERT",
            "description": "Converts the image into a bump map texture for use in 3D.",
        }
        return meta_info

    def NodeInitProps(self):
        p1 = api.PositiveIntegerProp(
            idname="Saturation", 
            default=1, 
            min_val=1, 
            max_val=50, 
            widget=api.SLIDER_WIDGET,
            label="Saturation:",
            )
        p2 = api.PositiveIntegerProp(
            idname="Brightness", 
            default=0, 
            min_val=0, 
            max_val=50, 
            widget=api.SLIDER_WIDGET,
            label="Brightness:",
            )
        p3 = api.PositiveIntegerProp(
            idname="Gamma", 
            default=1, 
            min_val=1, 
            max_val=50, 
            widget=api.SLIDER_WIDGET,
            label="Gamma:",
            )

        self.NodeAddProp(p1)
        self.NodeAddProp(p2)
        self.NodeAddProp(p3)

    def NodeInitParams(self):
        p = api.RenderImageParam('Image')

        self.NodeAddParam(p)

    def NodeEvaluation(self, eval_info):
        image1  = eval_info.EvaluateParameter('Image')
        saturation_val = eval_info.EvaluateProperty('Saturation')
        brightness_val = eval_info.EvaluateProperty('Brightness')
        gamma_val = eval_info.EvaluateProperty('Gamma')

        # Convert the current image data to an array 
        # that we can use and greyscale it.
        im = ArrayFromImage(image1.GetImage())
        gray_scale_img = cv2.equalizeHist(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY))

        generated_bump_map = self.ComputeBumpMap(
            gray_scale_img, 
            saturation_val, 
            brightness_val, 
            gamma_val
            )
        
        image = api.RenderImage()
        image.SetAsImage(
            ArrayToImage(generated_bump_map).convert('RGBA')
            )
        self.NodeSetThumb(image.GetImage())
        return image

 
api.RegisterNode(ToBumpMapNode, "corenode_tobumpmap")