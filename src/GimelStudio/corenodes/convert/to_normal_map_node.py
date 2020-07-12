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

import wx
from PIL import Image
import numpy as np
import scipy.ndimage
import scipy.misc

from GimelStudio.api import (Color, RenderImage, List, NodeBase, 
                            Parameter, Property, RegisterNode)

from GimelStudio.utils.image import ArrayFromImage, ArrayToImage

 
class NodeDefinition(NodeBase):
    
    @property
    def NodeIDName(self):
        return "corenode_tonormalmap"

    @property
    def NodeLabel(self):
        return "To Normal Map"

    @property
    def NodeCategory(self):
        return "CONVERT"

    @property
    def NodeDescription(self):
        return "Converts the image into a normal map texture for use in 3D." 

    @property
    def NodeVersion(self):
        return "2.1" 

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software" 

    @property
    def NodeProperties(self):
        return [
            Property('Sigma',
                prop_type='INTEGER',
                value=0
                ),
            Property('Intensity',
                prop_type='INTEGER',
                value=1
                ),
            ]

    @property
    def NodeParameters(self):
        return [
            Parameter('Image',
                param_type='RENDERIMAGE',
                default_value=RenderImage('RGBA', (256, 256), (0, 0, 0, 1))
                ),
        ]

   
    def NodePropertiesUI(self, node, parent, sizer):
        current_sigma_value = self.NodeGetPropValue('Sigma')
        current_intensity_value = self.NodeGetPropValue('Intensity')

        # Sigma
        sigma_label = wx.StaticText(parent, label="Sigma:")
        sizer.Add(sigma_label, border=5)

        self.sigma_slider = wx.Slider(
            parent, wx.ID_ANY, 
            value=current_sigma_value,
            minValue=0, maxValue=8,
            style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
            )
        self.sigma_slider.SetTickFreq(1)

        sizer.Add(self.sigma_slider, flag=wx.EXPAND|wx.ALL, border=5)

        # Intensity
        intensity_label = wx.StaticText(parent, label="Intensity:")
        sizer.Add(intensity_label, border=5)

        self.intensity_slider = wx.Slider(
            parent, wx.ID_ANY, 
            value=current_intensity_value,
            minValue=0, maxValue=6,
            style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
            )
        self.intensity_slider.SetTickFreq(1)

        sizer.Add(self.intensity_slider, flag=wx.EXPAND|wx.ALL, border=5)

        parent.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.OnSigmaChange, self.sigma_slider)
        parent.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.OnIntensityChange, self.intensity_slider)


    def OnSigmaChange(self, event):
        self.NodePropertiesUpdate('Sigma', self.sigma_slider.GetValue())

    def OnIntensityChange(self, event):
        self.NodePropertiesUpdate('Intensity', self.intensity_slider.GetValue())
 
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
        
        image = RenderImage()
        image.SetAsImage(
            ArrayToImage(generated_normal_map).convert('RGBA')
            )
        self.NodeSetThumb(image.GetImage())
        return image

 
RegisterNode(NodeDefinition)
