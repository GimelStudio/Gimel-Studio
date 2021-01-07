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

# Imports.---------------------------------------------------------------------
# OpenCV Imports.
try:
    import cv2
except ImportError:
    importErrorHelp = '\n'.join((
        "ImportErrorHelp: OpenCV is not available!",
        "  try:",
        "    pip:",
        "      Python2:",
        "      $ pip install opencv-python==3.4.9.31",
        "      Python3:",
        "      $ pip3 install opencv-python",
        "    Manual Install/Docs WebLinks:",
        "      https://pypi.org/project/opencv-python",
        "      https://github.com/skvark/opencv-python",
    ))
    import traceback
    excMessage = (traceback.format_exc() +
                  '\n' + '~' * 42 + '\n' + importErrorHelp)
    print(excMessage)
# NumPy Imports.
try:
    import numpy as np
except ImportError:
    importErrorHelp = '\n'.join((
        "ImportErrorHelp: NumPy is not available!",
        "  try:",
        "    pip:",
        "      $ pip install numpy",
        "      $ conda install numpy",
        "    Manual Install/Docs WebLinks:",
        "      https://pypi.org/project/numpy/",
        "      https://github.com/numpy/numpy",
        "      https://numpy.org/",
    ))
    import traceback
    excMessage = (traceback.format_exc() +
                  '\n' + '~' * 42 + '\n' + importErrorHelp)
    print(excMessage)

from GimelStudio import api

# FIXME: hack!
from GimelStudio.utils.image import ArrayFromImage, ArrayToImage


class ToAOMapNode(api.NodeBase):
    def __init__(self, _id):
        api.NodeBase.__init__(self, _id)

    def GammaCorrection(self, image, gamma):
        """ Corrects gamma of image. """
        inv_gamma = 1 / gamma
        table = np.array(
            [((i / 255) ** inv_gamma) * 255 for i in range(0, 256)]
        ).astype("uint8")
        return cv2.LUT(image, table)

    def ComputeAOMap(self, image, saturation, brightness, gamma, thresh):
        """ Calculates and returns an ambient occlusion map. """
        t, ao_img = cv2.threshold(image, thresh, 255, cv2.THRESH_TRUNC)
        ao_map = cv2.convertScaleAbs(
            ao_img,
            alpha=saturation,
            beta=brightness
        )
        gc_ao_map = self.GammaCorrection(ao_map, gamma)
        return gc_ao_map

    @property
    def NodeMeta(self):
        meta_info = {
            "label": "To AO Map",
            "author": "Correct Syntax",
            "version": (1, 2, 0),
            "supported_app_version": (0, 5, 0),
            "category": "CONVERT",
            "description": "Converts the image into an ambient occlusion map texture for use in 3D.",
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
        p4 = api.PositiveIntegerProp(
            idname="Threshold",
            default=127,
            min_val=0,
            max_val=255,
            widget=api.SLIDER_WIDGET,
            label="Threshold:",
        )

        self.NodeAddProp(p1)
        self.NodeAddProp(p2)
        self.NodeAddProp(p3)
        self.NodeAddProp(p4)

    def NodeInitParams(self):
        p = api.RenderImageParam('Image')

        self.NodeAddParam(p)

    def NodeEvaluation(self, eval_info):
        image1 = eval_info.EvaluateParameter('Image')
        saturation_val = eval_info.EvaluateProperty('Saturation')
        brightness_val = eval_info.EvaluateProperty('Brightness')
        gamma_val = eval_info.EvaluateProperty('Gamma')
        threshold_val = eval_info.EvaluateProperty('Threshold')

        im = image1.GetImage()
        gray_scale_img = cv2.equalizeHist(cv2.cvtColor(im, cv2.COLOR_BGRA2GRAY))

        generated_ao_map = self.ComputeAOMap(
            gray_scale_img,
            saturation_val,
            brightness_val,
            gamma_val,
            threshold_val
        )

        image = api.RenderImage()
        image.SetAsImage(
            generated_ao_map
        )
        self.NodeSetThumb(image.GetImage())
        return image


api.RegisterNode(ToAOMapNode, "corenode_toaomap")
