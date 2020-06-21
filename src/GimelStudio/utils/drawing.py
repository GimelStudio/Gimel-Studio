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
## FILE: drawing.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Provides utility drawing functions
## ----------------------------------------------------------------------------


import wx


# UNUSED?
def TileBackground(dc, bmp, x,y,w,h):
    """ Tile bmp into the specified rectangle"""
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


def DrawGrid(dc, rect, grid_size=10):
    """ Draws a grid to the specified size. """
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

 
def DrawCheckerBoard(dc, rect, checkcolor, box=1):
    """ Draws a checkerboard pattern on a wx.DC. Used for 
    Alpha channel backgrounds.

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
