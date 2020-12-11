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

from PIL import Image


class RenderImage(object):
    """ Represents an image data type for the renderer. """

    def __init__(self, size=(100, 100), color=(0, 0, 0, 1), packed_data=None):
        self._img = Image.new("RGBA", (size[0], size[1]), color)
        self._packedData = packed_data

    def GetPILImage(self):
        """ Returns the image.

        :returns: PIL ``Image`` object
        """
        return self._img

    def GetImage(self):
        """ Returns the image.

        :returns: PIL ``Image`` object
        """
        return self._img

    def SetAsOpenedImage(self, path):
        """ Sets the image and opens it. If the image is non-existent,
        it will try to get packed data from the file, if possible.

        :param path: image filepath to be opened
        """
        try:
            self._img = Image.open(path)
        except FileNotFoundError:
            if self._packedData is not None:
                self._img = self._packedData
            else:
                print("WARNING: COULD NOT GET PACKED IMAGE DATA!")

    def SetAsImage(self, image):
        """ Sets the image.

        :param image: PIL ``Image`` object
        """
        self._img = image
