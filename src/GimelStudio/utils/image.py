## ----------------------------------------------------------------------------
## Gimel Studio Copyright 2019-2020 by Noah Rahm and contributors
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

from PIL import Image
import numpy
from numpy import (amin, amax, ravel, asarray, cast, arange, ones, newaxis,
                   transpose, iscomplexobj, uint8, issubdtype, array)


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


def IsFPExt(path, extentions):
    """ Returns whether the file in the filepath is in the extension/type list given.
    :param path str: file path
    :param extentions list: extension/type list
    :returns boolean:
    """
    is_ext = False
    for ext in extentions:
        if path.endswith(ext):
            is_ext = True
    return is_ext


def GetFileExt(path, add_dot=False):
    """ Returns the filetype extension from the given file path.

    :param str path: file path
    :param boolean add_dot: whether to append a period/dot to the returned extension
    :returns str: filetype extension (e.g: png)
    """
    ext = path.split(".")
    ext.reverse()
    if add_dot == True:
        return ".{}".format(ext[0])
    else:
        return ext[0]


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
        if IsFPExt(export_path, [".png"]):
            bits = 6 # How much should this be lowered??
            compress_level = 7

    # Make sure JPG, JPEG, PCX, EPS files get saved as RGB mode
    if IsFPExt(export_path, [".jpg", ".jpeg", ".pcx", ".eps"]):
        rendered_image = rendered_image.convert("RGB")

    # XBM needs mode 1
    elif IsFPExt(export_path, [".xbm"]):
        rendered_image = rendered_image.convert("1")

    # TIFF doesn't have a quality param
    if IsFPExt(export_path, [".tiff"]):
        rendered_image.save(fp=export_path, optimize=optimize, bits=bits,
                            compress_level=compress_level)
    else:
        rendered_image.save(fp=export_path, quality=quality, optimize=optimize,
                            bits=bits, compress_level=compress_level)




# -------------------------------------------------------------
# Below functions are from taken from scipy 0.15.0
# (scipy.misc.pilutil.py) to support converting from
# np arrays to PIL image and vice-versa.
# -------------------------------------------------------------
# TODO: These don't need to be here. Should be using PIL as these
# are depreciated!

# Returns a byte-scaled image
def bytescale(data, cmin=None, cmax=None, high=255, low=0):
    if data.dtype == uint8:
        return data

    if high < low:
        raise ValueError("`high` should be larger than `low`.")

    if cmin is None:
        cmin = data.min()
    if cmax is None:
        cmax = data.max()

    cscale = cmax - cmin
    if cscale < 0:
        raise ValueError("`cmax` should be larger than `cmin`.")
    elif cscale == 0:
        cscale = 1

    scale = float(high - low) / cscale
    bytedata = (data * 1.0 - cmin) * scale + 0.4999
    bytedata[bytedata > high] = high
    bytedata[bytedata < 0] = 0
    return cast[uint8](bytedata) + cast[uint8](low)


def ArrayFromImage(im, flatten=0):
    """
    Return a copy of a PIL image as a numpy array.

    Parameters
    ----------
    im : PIL image
        Input image.
    flatten : bool
        If true, convert the output to grey-scale.

    Returns
    -------
    fromimage : ndarray
        The different colour bands/channels are stored in the
        third dimension, such that a grey-image is MxN, an
        RGB-image MxNx3 and an RGBA-image MxNx4.

    """
    if not Image.isImageType(im):
        raise TypeError("Input is not a PIL image.")
    if flatten:
        im = im.convert('F')
    elif im.mode == '1':
        # workaround for crash in PIL, see #1613.
        im.convert('L')

    return array(im)


def ArrayToImage(arr, high=255, low=0, cmin=None, cmax=None, pal=None,
            mode=None, channel_axis=None):
    """Takes a numpy array and returns a PIL image.
    The mode of the PIL image depends on the array shape and the `pal` and
    `mode` keywords.

    For 2-D arrays, if `pal` is a valid (N,3) byte-array giving the RGB values
    (from 0 to 255) then ``mode='P'``, otherwise ``mode='L'``, unless mode
    is given as 'F' or 'I' in which case a float and/or integer array is made.

    Notes
    -----
    For 3-D arrays, the `channel_axis` argument tells which dimension of the
    array holds the channel data.

    For 3-D arrays if one of the dimensions is 3, the mode is 'RGB'
    by default or 'YCbCr' if selected.

    The numpy array must be either 2 dimensional or 3 dimensional.

    """
    data = asarray(arr)
    if iscomplexobj(data):
        raise ValueError("Cannot convert a complex-valued array.")
    shape = list(data.shape)
    valid = len(shape) == 2 or ((len(shape) == 3) and
                                ((3 in shape) or (4 in shape)))
    if not valid:
        raise ValueError("'arr' does not have a suitable array shape for "
                         "any mode.")
    if len(shape) == 2:
        shape = (shape[1], shape[0])  # columns show up first
        if mode == 'F':
            data32 = data.astype(numpy.float32)
            image = Image.frombytes(mode, shape, data32.tostring())
            return image
        if mode in [None, 'L', 'P']:
            bytedata = bytescale(data, high=high, low=low,
                                 cmin=cmin, cmax=cmax)
            image = Image.frombytes('L', shape, bytedata.tostring())
            if pal is not None:
                image.putpalette(asarray(pal, dtype=uint8).tostring())
                # Becomes a mode='P' automagically.
            elif mode == 'P':  # default gray-scale
                pal = (arange(0, 256, 1, dtype=uint8)[:, newaxis] *
                       ones((3,), dtype=uint8)[newaxis, :])
                image.putpalette(asarray(pal, dtype=uint8).tostring())
            return image
        if mode == '1':  # high input gives threshold for 1
            bytedata = (data > high)
            image = Image.frombytes('1', shape, bytedata.tostring())
            return image
        if cmin is None:
            cmin = amin(ravel(data))
        if cmax is None:
            cmax = amax(ravel(data))
        data = (data*1.0 - cmin)*(high - low)/(cmax - cmin) + low
        if mode == 'I':
            data32 = data.astype(numpy.uint32)
            image = Image.frombytes(mode, shape, data32.tostring())
        else:
            raise ValueError(_errstr)
        return image

    # if here then 3-d array with a 3 or a 4 in the shape length.
    # Check for 3 in datacube shape --- 'RGB' or 'YCbCr'
    if channel_axis is None:
        if (3 in shape):
            ca = numpy.flatnonzero(asarray(shape) == 3)[0]
        else:
            ca = numpy.flatnonzero(asarray(shape) == 4)
            if len(ca):
                ca = ca[0]
            else:
                raise ValueError("Could not find channel dimension.")
    else:
        ca = channel_axis

    numch = shape[ca]
    if numch not in [3, 4]:
        raise ValueError("Channel axis dimension is not valid.")

    bytedata = bytescale(data, high=high, low=low, cmin=cmin, cmax=cmax)
    if ca == 2:
        strdata = bytedata.tostring()
        shape = (shape[1], shape[0])
    elif ca == 1:
        strdata = transpose(bytedata, (0, 2, 1)).tostring()
        shape = (shape[2], shape[0])
    elif ca == 0:
        strdata = transpose(bytedata, (1, 2, 0)).tostring()
        shape = (shape[2], shape[1])
    if mode is None:
        if numch == 3:
            mode = 'RGB'
        else:
            mode = 'RGBA'

    if mode not in ['RGB', 'RGBA', 'YCbCr', 'CMYK']:
        raise ValueError(_errstr)

    if mode in ['RGB', 'YCbCr']:
        if numch != 3:
            raise ValueError("Invalid array shape for mode.")
    if mode in ['RGBA', 'CMYK']:
        if numch != 4:
            raise ValueError("Invalid array shape for mode.")

    # Here we know data and mode is correct
    image = Image.frombytes(mode, shape, strdata)
    return image
