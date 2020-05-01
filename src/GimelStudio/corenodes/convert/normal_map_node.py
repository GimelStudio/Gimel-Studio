from PIL import Image
import numpy as np
import scipy.ndimage
import scipy.misc
from scipy import ndimage

from GimelStudio.api import (Color, RenderImage, List, ArrayFromImage,
                         ArrayToImage, NodeBase, ParameterDefinition,
                         PropertyDefinition, RegisterNode)

 
class NodeDefinition(NodeBase):
    
    @property
    def NodeName(self):
        return "corenode_tonormalmap"

    @property
    def NodeLabel(self):
        return "To Normal Map"

    @property
    def NodeCategory(self):
        return "CONVERT"

    @property
    def NodeDescription(self):
        return "Converts the given image to a normal map." 

    @property
    def NodeVersion(self):
        return "1.0.2" 

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software" 

    @property
    def NodeProperties(self):
        return [
            
        ]

    @property
    def NodeParameters(self):
        return [
            ParameterDefinition('Image',
                                param_type='image',
                                default_value=RenderImage('RGBA', (256, 256), (0, 0, 0, 1))),
            ParameterDefinition('Sigma',
                                param_type='integer',
                                default_value=1),
            ParameterDefinition('Intensity',
                                param_type='integer',
                                default_value=1),
        ]


 
    def NodePropertiesUI(self, node, ui, parent, sizer):
        self.NodePropertiesHelperInit(node, ui, parent, sizer)


    def smooth_gaussian(self, im, sigma):
        """ Blurs the normals. """
        if sigma == 0:
            return im

        im_smooth = im.astype(float)
        kernel_x = np.arange(-3*sigma,3*sigma+1).astype(float)
        kernel_x = np.exp((-(kernel_x**2))/(2*(sigma**2)))

        im_smooth = scipy.ndimage.convolve(im_smooth, kernel_x[np.newaxis])

        im_smooth = scipy.ndimage.convolve(im_smooth, kernel_x[np.newaxis].T)

        return im_smooth


    def gradient(self, im_smooth):
        """ Calculates the gradient for the normal map. """
        gradient_x = im_smooth.astype(float)
        gradient_y = im_smooth.astype(float)

        kernel = np.arange(-1,2).astype(float)
        kernel = - kernel / 2

        gradient_x = scipy.ndimage.convolve(gradient_x, kernel[np.newaxis])
        gradient_y = scipy.ndimage.convolve(gradient_y, kernel[np.newaxis].T)

        return gradient_x, gradient_y


    def sobel(self, im_smooth):
        """ Calculates another type of gradient for the normal map. """
        gradient_x = im_smooth.astype(float)
        gradient_y = im_smooth.astype(float)

        kernel = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])

        gradient_x = scipy.ndimage.convolve(gradient_x, kernel)
        gradient_y = scipy.ndimage.convolve(gradient_y, kernel.T)

        return gradient_x, gradient_y


    def compute_normal_map(self, gradient_x, gradient_y, intensity=1):
        """ Calcualates the normals of an image. """
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
        image1 = eval_info.EvaluateParameter('Image')

        # Get the values
        Sigma = eval_info.EvaluateParameter('Sigma')
        Intensity = eval_info.EvaluateParameter('Intensity')
 
        # Convert the current image data to an array that scipy can use
        im = ArrayFromImage(image1.GetImage())

        # Create the image
        if im.ndim == 3:
            im_grey = np.zeros((im.shape[0],im.shape[1])).astype(float)
            im_grey = (im[...,0] * 0.3 + im[...,1] * 0.6 + im[...,2] * 0.1)
            im = im_grey
        
        im_smooth = self.smooth_gaussian(im, Sigma)
        sobel_x, sobel_y = self.sobel(im_smooth)

        # Calculate the normal map
        generated_normal_map = self.compute_normal_map(sobel_x, sobel_y, Intensity)
        
        image = RenderImage()
        image.SetAsImage(ArrayToImage(generated_normal_map).convert('RGBA'))
        self.NodeSetThumbnail(image.GetImage())
        return image


RegisterNode(NodeDefinition)
