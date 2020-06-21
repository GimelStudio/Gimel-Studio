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
## FILE: image.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Provides utility image manipulation/converting functions
## ----------------------------------------------------------------------------

import wx


def ConvertImageToWx(image):
    """ Converts the given PIL image into a wx.Bitmap with RGBA. 

    :param image: PIL Image to convert
    :returns: wx.Bitmap
    """
    bitmap = wx.Bitmap.FromBufferRGBA(
        image.size[0],
        image.size[1], 
        image.convert('RGBA').tobytes()
        )
    return bitmap

