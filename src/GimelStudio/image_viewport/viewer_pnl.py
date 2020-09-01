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
## FILE: viewer.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the image viewer tab of the Image Viewport
## ----------------------------------------------------------------------------

import wx
import wx.adv

from PIL import Image

from GimelStudio.utils import ConvertImageToWx, DrawCheckerBoard
from GimelStudio.datafiles.icons import *


ID_IMAGE = wx.NewIdRef()
ID_INFOTEXT = wx.NewIdRef()
ID_RENDERTEXT = wx.NewIdRef()


class ViewerImage(object):
    """ Represents the Image Viewport image that is displayed. """
    def __init__(self, parent, image, pos=wx.Point(0, 0), _id=wx.ID_ANY):
        self._parent = parent
        self._image = image
        self._pos = pos
        self._id = _id

        self._rect = wx.Rect(
            self._pos.x, 
            self._pos.y, 
            self._image.Width, 
            self._image.Height
            )

    def GetParent(self):
        return self._parent

    def GetId(self):
        return self._id

    def SetId(self, id_):
        self._id = id_

    def GetRect(self):
        return self._rect

    def SetRect(self, rect):
        self._rect = rect

    def SetPosition(self, x, y):
        self._pos = wx.Point(x, y)

    def GetPosition(self):
        return self._pos

    def SetImage(self, image):
        self._image = image

    def GetImage(self):
        return self._image

    def Draw(self, dc):
        dc.ClearId(self.GetId())
        dc.SetId(self.GetId())

        dc.SetIdBounds(self.GetId(), self.GetRect())

        dc.DrawBitmap(
            self.GetImage(),
            self.GetPosition()[0],
            self.GetPosition()[1],
            True # Use alpha mask
            )


class ImageViewerPnl(wx.Panel):
    def __init__(self, parent, size=wx.DefaultSize):
        wx.Panel.__init__(self, parent, size=size)

        self._parent = parent
        self._maxWidth  = size[0]
        self._maxHeight = size[1]

        self._pdc = wx.adv.PseudoDC()

        self.zoomValue = 0.05
        self._renderTime = 0.00

        default_img = ConvertImageToWx(Image.new('RGBA', (256, 256)))
        self._viewportImage = ViewerImage(self, image=default_img,  _id=ID_IMAGE) 
        self._imageCopy = self._viewportImage.GetImage()

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: None)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMiddleDown)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyEvent)
        self.Bind(wx.EVT_LEFT_UP, self.OnMiddleUp)
        self.Bind(wx.EVT_SIZE, self.OnSize)


    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        dc = wx.GCDC(dc)

        dc.SetBackground(wx.Brush('grey'))
        dc.Clear()

        rect = wx.Rect(0, 0, self.Size[0], self.Size[1])

        # Draw the checkered alpha background
        DrawCheckerBoard(dc, rect, wx.Colour(0, 0, 0, 98), box=8)

        self._pdc.DrawToDC(dc)

    def OnSize(self, event):
        if self._imageCopy != None:
            self._UpdateImage(self._imageCopy)
            self._UpdateInfoText()

    def OnMiddleDown(self, event):
        self._lastPnt = event.GetPosition()

    def OnMiddleUp(self,event):
        self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        self.RefreshViewer()

    def OnMotion(self, event):
        if event.LeftIsDown():
            self.OnMoveImage(event)
            self.RefreshViewer()

    def OnMoveImage(self, event):
        self.SetCursor(wx.Cursor(wx.CURSOR_SIZING))
        pnt = event.GetPosition()
        dpnt = pnt - self._lastPnt
        self._pdc.TranslateId(self._viewportImage.GetId(), dpnt[0], dpnt[1])
        self._viewportImage.SetPosition(dpnt[0], dpnt[1])
        self._lastPnt = pnt


    def OnKeyEvent(self, event):
        """ Event when a key is pushed on the keyboard. """
        code = event.GetKeyCode()

        # plus (+)
        if code == wx.WXK_NUMPAD_ADD: 
            if self.zoomValue < 2.5:
                self.zoomValue += 0.05
            
        # minus (-)
        elif code == wx.WXK_NUMPAD_SUBTRACT: 
            if self.zoomValue > 0.05:
                self.zoomValue -= 0.05
                
        self.ZoomImage()


    def OnMouseWheel(self, event):
        """ Event when the mouse wheel is scrolled. """
        # Zoom in
        if event.GetWheelRotation() > 0:
            if self.zoomValue < 2.5:
                self.zoomValue += 0.05

        # Zoom out
        else:
            if self.zoomValue > 0.05:
                self.zoomValue -= 0.05

        self.ZoomImage()


    def _UpdateImage(self, image):
        """ Update the viewport image. This is intended to be
        an internal method.

        :param image: wx.Bitmap
        """
        # Keep a reference to the original image
        self._imageCopy = image

        image = image.ConvertToImage()

        #img_width = image.Width
        #img_height = image.Height
        #print(img_width, img_height, "|", self._imageCopy.Width, self._imageCopy.Height)

        #win_width = self.Size[0]
        #win_height = self.Size[1]

        # Check to make sure the zoomValue has a valid value, as wxPython's
        # wx.Image.Rescale method needs the width & height > 0
        if 1 > image.Width*self.zoomValue and 1 > image.Height*self.zoomValue:
            self.zoomValue = 0.05

        image.Rescale(
            image.Width*self.zoomValue,
            image.Height*self.zoomValue,
            wx.IMAGE_QUALITY_NEAREST
            )
            
        img = wx.Bitmap(image)
        self._viewportImage.SetImage(img)

        self._viewportImage.SetPosition(
            (self.Size[0] - image.Width)/2.0,
            (self.Size[1] - image.Height)/2.0
            ) 

        self._viewportImage.Draw(self._pdc)
        self.RefreshViewer()


    def _UpdateInfoText(self):
        """ Update the top info text. This is intended to be
        an internal method.
        """
        self._pdc.ClearId(ID_INFOTEXT)
        self._pdc.SetId(ID_INFOTEXT)
        self._pdc.SetBrush(wx.Brush(wx.Colour(0, 0, 0, 120)))
        self._pdc.DrawRectangle(0, 0, self.Size[0], 26)
        
        text = 'Render Finished in {0} sec. | Zoom: {1}%'.format(
            round(self._renderTime, 3), 
            round(self.zoomValue*100)
            )
        self._pdc.SetTextForeground(wx.Colour('white'))
        self._pdc.DrawText(text, 22, 2)
        self.RefreshViewer()

    def UpdateRenderText(self, render=True):
        """ Update the text durring a render. """
        if render == True:
            self._pdc.ClearId(ID_INFOTEXT)
            self._pdc.SetId(ID_INFOTEXT)
            self._pdc.SetBrush(wx.Brush(wx.Colour(0, 0, 0, 120)))
            self._pdc.DrawRectangle(0, 0, self.Size[0], 26)
        
            self._pdc.SetTextForeground(wx.Colour('white'))
            self._pdc.DrawText('Rendering Image...', 22, 2)
            self.RefreshViewer()

    def SetRenderTime(self, render_time):
        self._renderTime = render_time

    def GetRenderTime(self):
        return self._renderTime

    def ZoomImage(self):
        self._UpdateImage(self._imageCopy)
        self._UpdateInfoText()

    def UpdateViewerImage(self, image, render_time):
        """ Update the Image Viewport. This refreshes everything
        in the Viewport.

        :param image: wx.Bitmap
        :param float render_time: float value of the image's render time
        """
        self._UpdateImage(image)
        self.SetRenderTime(render_time)
        self._UpdateInfoText()


    def RefreshViewer(self):
        """ Refresh the Image Viewport. Call to update 
        everything after DC drawing. 
        """
        rect = wx.Rect(0, 0, self.Size[0], self.Size[1])
        self.RefreshRect(rect, False)
