import os
import copy
import hashlib

import cv2
from PIL import Image
import numpy as np
import moderngl as mg
from array import array


class GPUEngine(object):
    def __init__(self):
        self.glContext = mg.create_standalone_context(require=330)

        self.src_texture = self.glContext.texture((4000, 4000), 4)
        self.dst_texture = self.glContext.texture((4000, 4000), 4)
        self.src_fbo = self.glContext.framebuffer(self.src_texture)
        self.dst_fbo = self.glContext.framebuffer(self.dst_texture)

        self._programs = {}
        self._vaos = {}

        # Fullscreen quad in NDC
        self.vertices = self.glContext.buffer(
            array(
                'f',
                [
                    # Triangle strip creating a fullscreen quad
                    # x, y
                    -1,  1,  # upper left
                    -1, -1, # lower left
                    1, 1, # upper right
                    1, -1, # lower right
                ]
            )
        )

    def GetGLContext(self):
        return self.glContext

    def Swap(self):
        """ Swap the textures. """
        self.src_texture, self.dst_texture = self.dst_texture, self.src_texture
        self.src_fbo, self.dst_fbo = self.dst_fbo, self.src_fbo

    def Write(self, image):
        # do the writing to src_texture here
        image = image.GetImage()
        #print(image.dtype)
        image = image.copy(order='C')
        self.viewport = (0, 0, *image.shape[1::-1])

        self.src_texture.write(image, viewport=self.viewport)
        return self.viewport

    def ReadNumpy(self):
        """ Returns a ``numpy.ndarray`` image. """
        raw = self.dst_fbo.read(components=4, dtype='f1', viewport=self.viewport)

        img = np.frombuffer(raw, dtype='uint8').reshape((self.viewport[3], self.viewport[2], 4))
        return img

    def Render(self, frag_shader, props, image=None):
        if image is not None:
            self.viewport = self.Write(image)
        hash_value = hashlib.md5(copy.copy(frag_shader).encode())
        vao = self._vaos.get(hash_value)

        if vao is None:
            program = self.glContext.program(
                vertex_shader="""
                    #version 330

                    in vec2 in_position;

                    void main() {
                        gl_Position = vec4(in_position, 0.0, 1.0);
                    }
                """,
                fragment_shader=frag_shader,
            )

            vao = self.glContext.vertex_array(
                program,
                [
                    (self.vertices, '2f', 'in_position'),
                ]
            )

            self._programs[hash_value] = program
            self._vaos[hash_value] = vao


        # Pass in values into the shader
        for prop in props:
            value = props[prop]
            if prop in program:
                program[prop] = value


        self.dst_fbo.use()
        self.dst_fbo.clear()
        self.dst_fbo.viewport = self.viewport
        self.src_texture.use(0)
        vao.render(mode=mg.TRIANGLE_STRIP)

    def Release(self):
        self.src_fbo.release()
        self.src_texture.release()
        for prog in self._programs.values():
            prog.release()
        for vao in self._vaos.values():
            vao.release()
        self.vertices.release()