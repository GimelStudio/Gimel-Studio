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
#
# FILE: datatypes.py
# AUTHOR(S): Noah Rahm
# PURPOSE: Define the main data types
# ----------------------------------------------------------------------------

import cv2
import numpy as np
from PIL import Image
import OpenImageIO as oiio
from OpenImageIO import ImageBuf, ImageSpec, ImageBufAlgo

from GimelStudio.utils import ArrayFromImage, ArrayToImage


class RenderImage(object):
    """ Represents an image data type for the renderer. """

    def __init__(self, size=(100, 100), packed_data=None):
        self._img = np.zeros((size[0], size[1], 4), dtype=np.uint8)
        self._packedData = packed_data

    def GetImage(self):
        """ Returns the image.

        :returns: ``numpy.ndarray`` object
        """
        return self._img

    def GetPILImage(self):
        """ Returns the image as a PIL Image.

        :returns: PIL ``Image`` object
        """
        return ArrayToImage(self._img)

    def SetAsOpenedImage(self, path):
        """ Sets the image and opens it. If the image is non-existent,
        it will try to get packed data from the file, if possible.

        :param path: image filepath to be opened
        """
        try:
            # Open the image as an array
            img_input = oiio.ImageInput.open(path)
            image = img_input.read_image(format="uint8")

            # Enforce RGBA
            if image.shape[2] == 3:
                self._img = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)
            else:
                self._img = image
        except FileNotFoundError:
            if self._packedData is not None:
                self._img = self._packedData
            else:
                print("WARNING: COULD NOT GET PACKED IMAGE DATA!")

    def SetAsImage(self, image):
        """ Sets the render image and converts it to the correct datatype.

        :param image: ``numpy.ndarray``, Pillow ``Image`` object
        """
        img_type = type(image)

        # if img_type == Image:
        #     self._img = ArrayFromImage(image)
        # elif img_type == ImageBuf:
        #     self._img = ImageBuf.get_pixels(image)
        # elif img_type == np.ndarray:
        self._img = image

    def SetAsImageFromPIL(self, image):
        """ Sets the image from a PIL Image.

        :param image: PIL ``Image`` object
        """
        self._img = ArrayFromImage(image)


    # def AsImgType(self, output_type="NDARRAY"):
    #     img_type = type(self._img)
    #     print(img_type)

    #     if output_type
    #     image =

    #     return
