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
import moderngl
import numpy as np
from PIL import Image
from array import array

from GimelStudio import api
from GimelStudio.utils.image import ArrayFromImage, ArrayToImage


# ctx = moderngl.create_standalone_context()

# prog = ctx.program(
#     vertex_shader='''
#         #version 330

#         in vec2 in_vert;
#         in vec3 in_color;

#         out vec3 v_color;

#         void main() {
#             v_color = in_color;
#             gl_Position = vec4(in_vert, 0.0, 1.0);
#         }
#     ''',
#     fragment_shader='''
#         #version 330

#         in vec3 v_color;

#         out vec3 f_color;

#         void main() {
#             f_color = v_color;
#         }
#     ''',
# )

# x = np.linspace(-1.0, 1.0, 50)
# y = np.random.rand(50) - 0.5
# r = np.ones(50)
# g = np.zeros(50)
# b = np.zeros(50)

# vertices = np.dstack([x, y, r, g, b])

# vbo = ctx.buffer(vertices.astype('f4').tobytes())
# vao = ctx.simple_vertex_array(prog, vbo, 'in_vert', 'in_color')

# fbo = ctx.simple_framebuffer((512, 512))
# fbo.use()
# fbo.clear(0.0, 0.0, 0.0, 1.0)
# vao.render(moderngl.LINE_STRIP)

# Image.frombytes('RGB', fbo.size, fbo.read(), 'raw', 'RGB', 0, -1).show()


# class ImageProcessing(moderngl_window.WindowConfig):
#     window_size = 3840 // 2, 2160 // 2
#     resource_dir = Path(__file__).parent.resolve()

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.image_processing = ImageTransformer(self.ctx, self.window_size)


#     def render(self, time, frame_time):
# Uncomment to view in Window
#self.image_processing.render(self.texture, target=self.ctx.screen)


class ImageTransformer:

    def __init__(self, ctx, size, program=None):
        self.ctx = ctx
        self.size = size
        self.program = None
        self.fbo = self.ctx.framebuffer(
            color_attachments=[self.ctx.texture(self.size, 4)]
        )

        # Create some default program if needed
        if not program:
            self.program = self.ctx.program(
                vertex_shader="""
                    #version 330

                    in vec2 in_position;
                    in vec2 in_uv;
                    out vec2 uv;

                    void main() {
                        gl_Position = vec4(in_position, 0.0, 1.0);
                        uv = in_uv;
                    }
                """,
                fragment_shader="""
                    #version 330

                    uniform sampler2D image;
                    in vec2 uv;
                    out vec4 out_color;

                    void main() {
                        vec4 color = texture(image, uv);
                        // do something with color here
                        out_color = vec4(color.r, color.g, 0, color.a);

                    }

                """,
            )

        # Fullscreen quad in NDC
        self.vertices = self.ctx.buffer(
            array(
                'f',
                [
                    # Triangle strip creating a fullscreen quad
                    # x, y, u, v
                    -1, 1, 0, 1,  # upper left
                    -1, -1, 0, 0,  # lower left
                    1, 1, 1, 1,  # upper right
                    1, -1, 1, 0,  # lower right
                ]
            )
        )
        self.quad = self.ctx.vertex_array(
            self.program,
            [
                (self.vertices, '2f 2f', 'in_position', 'in_uv'),
            ]
        )

    def render(self, texture, target=None):
        if target:
            target.use()
        else:
            self.fbo.use()

        texture.use(0)
        self.quad.render(mode=moderngl.TRIANGLE_STRIP)

    def write(self):

        raw = self.fbo.read(components=4, dtype='f1')
        buf = np.frombuffer(raw, dtype='uint8').reshape((*self.fbo.size[1::-1], 4))
        img = cv2.cvtColor(buf, cv2.COLOR_BGR2RGB)
        return img
        #cv2.imwrite("OUTPUT_IMAGE.png", img)


class GLSLNode(api.NodeBase):
    def __init__(self, _id):
        api.NodeBase.__init__(self, _id)

    @property
    def NodeMeta(self):
        meta_info = {
            "label": "GLSL",
            "author": "Correct Syntax",
            "version": (2, 5, 0),
            "supported_app_version": (0, 5, 0),
            "category": "FILTER",
            "description": "GLSL shader",
        }
        return meta_info

    def NodeInitProps(self):
        filter_type = api.ChoiceProp(
            idname="Filter Type",
            default="Gaussian",
            choices=["Box", "Gaussian"],
            label="Filter Type:"
        )
        kernel_size = api.PositiveIntegerProp(
            idname="Kernel Size",
            default=1,
            min_val=1,
            max_val=400,
            widget=api.SLIDER_WIDGET,
            label="Kernel Size:",
        )
        kernel_x = api.PositiveIntegerProp(
            idname="Kernel X",
            default=1,
            min_val=1,
            max_val=1600,
            widget=api.SLIDER_WIDGET,
            label="Kernel X:",
        )
        kernel_y = api.PositiveIntegerProp(
            idname="Kernel Y",
            default=1,
            min_val=1,
            max_val=1600,
            widget=api.SLIDER_WIDGET,
            label="Kernel Y:",
        )
        self.NodeAddProp(filter_type)
        self.NodeAddProp(kernel_size)
        self.NodeAddProp(kernel_x)
        self.NodeAddProp(kernel_y)

    def NodeInitParams(self):
        image = api.RenderImageParam('Image')

        self.NodeAddParam(image)

    def NodeEvaluation(self, eval_info):
        image1 = eval_info.EvaluateParameter('Image')
        kernel_size = eval_info.EvaluateProperty('Kernel Size')
        kernel_x = eval_info.EvaluateProperty('Kernel X')
        kernel_y = eval_info.EvaluateProperty('Kernel Y')
        filter_type = eval_info.EvaluateProperty('Filter Type')

        image = api.RenderImage()

        img = ArrayFromImage(image1.GetImage())
        img = img.copy(order='C')

        ctx = moderngl.create_standalone_context()

        texture = ctx.texture(img.shape[1::-1], img.shape[2], img)

        window_size = 3840 // 2, 2160 // 2
        image_processing = ImageTransformer(ctx, window_size)

        # Headless
        image_processing.render(texture)
        output_img = image_processing.write()

        image.SetAsImage(ArrayToImage(output_img).convert('RGBA'))

        self.NodeSetThumb(image.GetImage())
        return image


api.RegisterNode(GLSLNode, "corenode_glsl")
