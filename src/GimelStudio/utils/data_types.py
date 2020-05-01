## ----------------------------------------------------------------------------
## Gimel Studio © 2020 Correct Syntax, Noah Rahm. All rights reserved.
##
## FILE: node.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define main data types
## ----------------------------------------------------------------------------

from PIL import Image


class List(object):
    """
    Represents a list of items.
    """
    def __init__(self, items, value):
        self.items = items
        self.value = value

    def GetItems(self):
        return self.items

    def GetValue(self):
        return self.value

    def SetAsValue(self, item):
        self.value = item


class RenderImage(object):
    """
    Represents an image.
    """
    def __init__(self, mode='RGBA', size=(256, 256), color=(0, 0, 0, 1)):
        self.img = Image.new(mode, (size[0], size[1]), color)

    def GetImage(self):
        return self.img

    def SetAsOpenedImage(self, path):
        self.img = Image.open(path)

    def SetAsImage(self, image):
        self.img = image
        
# UNUSED?        
class Color(object):
    """
    Represents a four component color value with red, green, blue and alpha channels.
    """
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
        return '#%02x%02x%02x' % (int(self.red), int(self.green), int(self.blue))
        



    
