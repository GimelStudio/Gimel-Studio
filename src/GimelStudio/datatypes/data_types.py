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
##
## FILE: data_types.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the main data types
## ----------------------------------------------------------------------------


from PIL import Image


class List(object):
    """ Represents a list of items. """
    def __init__(self, items, default):
        self.items = items
        self.default = default# value 

    def GetItems(self):
        """ Return all of the items.

        :returns: list
        """
        return self.items

    def GetDefault(self):
        """ Get the default value of this List.

        :returns: the default value (string, int, etc)
        """
        return self.default

    def SetAsValue(self, item):
        """ Set the default value of this List.

        :param item: the item to set as the default
        """
        self.value = item


class RenderImage(object):
    """ Represents an image data type for the renderer. """
    def __init__(self, mode='RGBA', size=(256, 256), color=(0, 0, 0, 1)):
        self.img = Image.new(mode, (size[0], size[1]), color)

    def GetImage(self):
        """ Returns the image.

        :returns: PIL ``Image`` object
        """
        return self.img

    def SetAsOpenedImage(self, path):
        """ Sets the image and opens it.

        :param path: image filepath to be opened
        """
        self.img = Image.open(path)

    def SetAsImage(self, image):
        """ Sets the image.

        :param image: PIL ``Image`` object
        """
        self.img = image
        
# UNUSED?        
class Color(object):
    """ Represents a color value with red, green, blue and alpha channels. """
    def __init__(self, red=0.0, green=0.0, blue=0.0, alpha=1.0):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    def GetColors(self):
        return (self.red, self.green, self.blue, self.alpha)
    
    def GetHex(self):
        return self._FromRGBAToHex()

    def _FromRGBAToHex(self):
        return '#%02x%02x%02x' % (
            int(self.red), 
            int(self.green), 
            int(self.blue)
            )
