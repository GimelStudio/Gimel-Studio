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

from PIL import Image, ImageOps

from GimelStudio import api


class AlphaCompositeNode(api.NodeBase):
    def __init__(self, _id):
        api.NodeBase.__init__(self, _id)

    @property
    def NodeMeta(self):
        meta_info = {
            "label": "Alpha Composite",
            "author": "Correct Syntax",
            "version": (1, 2, 0),
            "supported_app_version": (0, 5, 0),
            "category": "BLEND",
            "description": "Creates a new image by interpolating between two input images, using a constant alpha.",
        }
        return meta_info

    def NodeInitParams(self):
        p1 = api.RenderImageParam('Image 1')
        p2 = api.RenderImageParam('Image 2')

        self.NodeAddParam(p1)
        self.NodeAddParam(p2)

    def NodeEvaluation(self, eval_info):
        image1 = eval_info.EvaluateParameter('Image 1')
        image2 = eval_info.EvaluateParameter('Image 2')

        image = api.RenderImage()
        main_image = image1.GetImage()
        layer_image = ImageOps.fit(image2.GetImage(), main_image.size)
        image.SetAsImage(Image.alpha_composite(main_image, layer_image))
        self.NodeSetThumb(image.GetImage())
        return image


api.RegisterNode(AlphaCompositeNode, "corenode_alphacomposite")
