## ----------------------------------------------------------------------------
## Gimel Studio © 2020 Correct Syntax, Noah Rahm. All rights reserved.
##
## FILE: drawing.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Provide utility drawing functions
## ----------------------------------------------------------------------------


import wx


def TileBackground(dc, bmp, x,y,w,h):
    """Tile bmp into the specified rectangle"""
    bw = bmp.GetWidth()
    bh = bmp.GetHeight()

    dc.SetClippingRegion(x,y,w,h)

    # adjust so 0,0 so we always match with a tiling starting at 0,0
    dx = x % bw
    x = x - dx
    w = w + dx

    dy = y % bh
    y = y - dy
    h = h + dy

    tx = x
    x2 = x+w
    y2 = y+h

    while tx < x2:
        ty = y
        while ty < y2:
            dc.DrawBitmap(bmp, tx, ty)
            ty += bh
        tx += bw

# UNUSED?
def GetCheckeredBitmap(blocksize=8, ntiles=4, rgb0=b'\xFF', rgb1=b'\xCC'):
    """
    Creates a square RGB checkered bitmap using the two specified colors.

    The bitmap returned will have width = height = blocksize*ntiles*2

    :param int `blocksize`:  the number of pixels in each solid color square
    :param int `ntiles1`:  the number of tiles along width and height.  Each
        tile is 2x2 blocks.
    :param `rbg0`: the first color, as 3-character bytes object.
    :param `rgb1`: the second color, as 3-character bytes object. If only 1
        character is provided, it is treated as a grey value.

    :return: :class:`wx.Bitmap`

    """
    assert isinstance(rgb0, bytes)
    assert isinstance(rgb1, bytes)

    size = blocksize*ntiles*2

    if len(rgb0)==1:
        rgb0 = rgb0 * 3
    if len(rgb1)==1:
        rgb1 = rgb1 * 3

    strip0 = (rgb0*blocksize + rgb1*blocksize)*(ntiles*blocksize)
    strip1 = (rgb1*blocksize + rgb0*blocksize)*(ntiles*blocksize)
    band = strip0 + strip1
    data = band * ntiles
    return wx.Bitmap.FromBuffer(size, size, data)


def DrawGrid(dc, rect, grid_size=10):
    """ 
    Draws a grid to the specified size.
    """
    left = int(rect[0]) - (int(rect[0]) % grid_size)
    top = int(rect[1]) - (int(rect[1]) % grid_size)

    # Vertical lines
    x = left
    while x < rect[2]:
        x += grid_size
        dc.DrawLine(x, rect[1], x, rect[3])

    # Horizontal lines
    y = top
    while y < rect[3]:
        y += grid_size
        dc.DrawLine(rect[0], y, rect[2], y)

 
def DrawCheckerBoard(dc, rect, checkcolor, box=5):
    """
    Draws a checkerboard pattern on a wx.DC. Used 
    for Alpha channel backgrounds.

    NOTE: Seems to only work with the wx.DC and NOT
    the wx.PseudoDC
    """
    y = rect.y
    dc.SetPen(wx.Pen(checkcolor))
    dc.SetBrush(wx.Brush(checkcolor)) 
    dc.SetClippingRegion(rect)

    while y < rect.height:
        x = box*((y//box)%2) + 2
        while x < rect.width:
            dc.DrawRectangle(x, y, box, box)
            x += box*2
        y += box
