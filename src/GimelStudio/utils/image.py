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
## PURPOSE: Provide utility image manipulation, converting, exporting functions
## ----------------------------------------------------------------------------

import wx


def ConvertImageToWx(image):
    """ Converts the given ``PIL Image`` object into a 
    ``wx.Bitmap`` with RGBA. 

    :param image: ``PIL Image`` to convert
    :returns: ``wx.Bitmap``
    """
    bitmap = wx.Bitmap.FromBufferRGBA(
        image.size[0],
        image.size[1], 
        image.convert('RGBA').tobytes()
        )
    return bitmap


def IsFilePathExt(path, ext):
    is_ext = False
    if path.endswith(ext):
        is_ext = True
    return is_ext


def ExportRenderedImageToFile(rendered_image, export_path, 
                            quality=75, optimize=False, export_for_web=False):
    """ Smooths out the various export options for exporting images and
    exports the image to the given file path.

    from the Pillow docs:

        quality
        The image quality, on a scale from 0 (worst) to 95 (best). The default is 75. 
        Values above 95 should be avoided; 100 disables portions of the JPEG 
        compression algorithm, and results in large files with hardly any gain 
        in image quality. 
        
        ^NOTE: For this reason, the "quality" slider value only has a range 0-95

        optimize
        If present and true, indicates that the encoder should make an extra pass 
        over the image in order to select optimal encoder settings.

    :param rendered_image: ``PIL Image`` object to be exported
    :param string export_path: string of the path to export the image to
    :param int quality: the image export quality (see above)
    :param boolean optimize: whether to optimize the exported image (see above)
    :param boolean export_for_web: whether to make optimizations for use on websites, etc
    """

    # Set values to PIL defaults initially
    bits = 8
    compress_level = 6

    if export_for_web == True:
        optimize = True

        # PNG specific
        if IsFilePathExt(export_path, ".png"):
            bits = 6 # How much should this be lowered??
            compress_level = 7 

    # Make sure JPEGs get saved as RGB mode    
    if IsFilePathExt(export_path, ".jpg") or IsFilePathExt(export_path, ".jpeg"):
        rendered_image = rendered_image.convert("RGB")

    rendered_image.save(fp=export_path, quality=quality, optimize=optimize, 
                        bits=bits, compress_level=compress_level)
