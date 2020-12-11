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


class CompositeNode(api.NodeBase):
    def __init__(self, _id):
        api.NodeBase.__init__(self, _id)

    @property
    def NodeMeta(self):
        meta_info = {
            "label": "Composite",
            "author": "Correct Syntax",
            "version": (1, 1, 0),
            "supported_app_version": (0, 5, 0),
            "category": "BLEND",
            "description": "Creates composite image by blending images using a transparency mask.",
        }
        return meta_info

    def NodeInitParams(self):
        p1 = api.RenderImageParam('Image 1')
        p2 = api.RenderImageParam('Image 2')
        p3 = api.RenderImageParam('Alpha Mask')

        self.NodeAddParam(p1)
        self.NodeAddParam(p2)
        self.NodeAddParam(p3)

    def NodeEvaluation(self, eval_info):
        image1 = eval_info.EvaluateParameter('Image 1')
        image2 = eval_info.EvaluateParameter('Image 2')
        mask = eval_info.EvaluateParameter('Alpha Mask')

        image = api.RenderImage()
        main_image = image1.GetImage()
        layer_image = ImageOps.fit(image2.GetImage(), main_image.size)
        mask_image = ImageOps.fit(mask.GetImage(), main_image.size).convert('RGBA')

        image.SetAsImage(Image.composite(main_image, layer_image, mask_image))
        self.NodeSetThumb(image.GetImage())
        return image


api.RegisterNode(CompositeNode, "corenode_composite")
