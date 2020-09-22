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

import numpy as np
import scipy.ndimage
import scipy.misc
from PIL import ImageFilter  

from GimelStudio import api

# FIXME: hack!
from GimelStudio.utils.image import ArrayFromImage, ArrayToImage

 
class ToNormalMapNode(api.NodeBase):
    def __init__(self, _id):
        api.NodeBase.__init__(self, _id)

    def SmoothGaussian(self, im, sigma):
        """ Blurs the normals. """
        if sigma == 0:
            return im

        im_smooth = im.astype(float)
        kernel_x = np.arange(-3*sigma,3*sigma+1).astype(float)
        kernel_x = np.exp((-(kernel_x**2))/(2*(sigma**2)))

        im_smooth = scipy.ndimage.convolve(im_smooth, kernel_x[np.newaxis])

        im_smooth = scipy.ndimage.convolve(im_smooth, kernel_x[np.newaxis].T)

        return im_smooth

    def Gradient(self, im_smooth):
        """ Calculates the gradient for the normal map. """
        gradient_x = im_smooth.astype(float)
        gradient_y = im_smooth.astype(float)

        kernel = np.arange(-1,2).astype(float)
        kernel = - kernel / 2

        gradient_x = scipy.ndimage.convolve(gradient_x, kernel[np.newaxis])
        gradient_y = scipy.ndimage.convolve(gradient_y, kernel[np.newaxis].T)

        return gradient_x, gradient_y

    def Sobel(self, im_smooth):
        """ Calculates another type of gradient for the normal map. """
        gradient_x = im_smooth.astype(float)
        gradient_y = im_smooth.astype(float)

        kernel = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])

        gradient_x = scipy.ndimage.convolve(gradient_x, kernel)
        gradient_y = scipy.ndimage.convolve(gradient_y, kernel.T)

        return gradient_x, gradient_y

    def ComputeNormalMap(self, gradient_x, gradient_y, intensity=1):
        """ Calculates the normals of an image and returns a normal map. """
        width = gradient_x.shape[1]
        height = gradient_x.shape[0]
        max_x = np.max(gradient_x)
        max_y = np.max(gradient_y)

        max_value = max_x

        if max_y > max_x:
            max_value = max_y

        normal_map = np.zeros((height, width, 3), dtype=np.float32)

        intensity = 1 / intensity

        strength = max_value / (max_value * intensity)

        normal_map[..., 0] = gradient_x / max_value
        normal_map[..., 1] = gradient_y / max_value
        normal_map[..., 2] = 1 / strength

        norm = np.sqrt(np.power(normal_map[..., 0], 2) + np.power(normal_map[..., 1], 2) + np.power(normal_map[..., 2], 2))

        normal_map[..., 0] /= norm
        normal_map[..., 1] /= norm
        normal_map[..., 2] /= norm

        normal_map *= 0.5
        normal_map += 0.5

        return normal_map

    @property
    def NodeMeta(self):
        meta_info = {
            "label": "To Normal Map",
            "author": "Correct Syntax",
            "version": (2, 2, 0),
            "supported_app_version": (0, 5, 0),
            "category": "CONVERT",
            "description": "Converts the image into a normal map texture for use in 3D.",
        }
        return meta_info

    def NodeInitProps(self):
        p1 = api.PositiveIntegerProp(
            idname="Sigma", 
            default=1, 
            min_val=1, 
            max_val=25, 
            widget=api.SLIDER_WIDGET,
            label="Sigma:",
            )
        p2 = api.PositiveIntegerProp(
            idname="Intensity", 
            default=1, 
            min_val=1, 
            max_val=25, 
            widget=api.SLIDER_WIDGET,
            label="Intensity:",
            )

        self.NodeAddProp(p1)
        self.NodeAddProp(p2)

    def NodeInitParams(self):
        p = api.RenderImageParam('Image')

        self.NodeAddParam(p)

    def NodeEvaluation(self, eval_info):
        image1  = eval_info.EvaluateParameter('Image')
        sigma_val = eval_info.EvaluateProperty('Sigma')
        intensity_val = eval_info.EvaluateProperty('Intensity')

        # Convert the current image data to an array that scipy can use
        im = ArrayFromImage(image1.GetImage())

        # Create the image
        if im.ndim == 3:
            im_grey = np.zeros((im.shape[0],im.shape[1])).astype(float)
            im_grey = (im[...,0] * 0.3 + im[...,1] * 0.6 + im[...,2] * 0.1)
            im = im_grey
        
        im_smooth = self.SmoothGaussian(im, sigma_val)
        sobel_x, sobel_y = self.Sobel(im_smooth)

        # Calculate the normal map
        generated_normal_map = self.ComputeNormalMap(
            sobel_x, 
            sobel_y, 
            intensity_val
            )
        
        image = api.RenderImage()
        image.SetAsImage(
            ArrayToImage(generated_normal_map).convert('RGBA')
            )
        self.NodeSetThumb(image.GetImage())
        return image


api.RegisterNode(ToNormalMapNode, "corenode_tonormalmap")