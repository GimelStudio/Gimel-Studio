# THIS FILE IS A PART OF GIMEL STUDIO AND IS LICENSED UNDER THE SAME TERMS:
# ----------------------------------------------------------------------------
# Gimel Studio Copyright 2020 Noah Rahm, Correct Syntax. All rights reserved.
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

from GimelStudio import api


class GetChannelNode(api.NodeBase):
    def __init__(self, _id):
        api.NodeBase.__init__(self, _id)

    @property
    def NodeMeta(self):
        meta_info = {
            "label": "Get Channel",
            "author": "Correct Syntax",
            "version": (0, 7, 2),
            "supported_app_version": (0, 5, 0),
            "category": "COLOR",
            "description": "Gets a single channel from the image RGBA channels.",
            "gpu_support": "yes",
        }
        return meta_info

    def NodeInitProps(self):
        p1 = api.ChoiceProp(
            idname="Image Channel",
            default="R",
            label="Image Channel:",
            choices=[
                    'R',
                    'G',
                    'B',
                    'A'
            ]
        )

        self.NodeAddProp(p1)

    def NodeInitParams(self):
        image = api.RenderImageParam("Image")
        self.NodeAddParam(image)

    def NodeEvaluation(self, params, props):
        image1 = params['Image']
        channel = props['Image Channel']

        render_image = api.RenderImage()

        # TODO: There is probably a better way to do this. :)
        if channel == "R":
            result = self.RenderGLSL("./GimelStudio/corenodes/color/get_channel/get_channel_r.glsl", {}, image1)
        elif channel == "G":
            result = self.RenderGLSL("./GimelStudio/corenodes/color/get_channel/get_channel_g.glsl", {}, image1)
        elif channel == "B":
            result = self.RenderGLSL("./GimelStudio/corenodes/color/get_channel/get_channel_b.glsl", {}, image1)
        elif channel == "A":
            result = self.RenderGLSL("./GimelStudio/corenodes/color/get_channel/get_channel_a.glsl", {}, image1)

        render_image.SetAsImage(result)

        return render_image


api.RegisterNode(GetChannelNode, "corenode_getchannel")
