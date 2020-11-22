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
## FILE: image_viewport.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the Image Viewport panel
## ----------------------------------------------------------------------------

import wx
import wx.adv

from PIL import Image

from GimelStudio import utils
from GimelStudio.datafiles.icons import *

from .utils import ZoomPanel


class ImageViewport(ZoomPanel):
    def __init__(self, parent):
        ZoomPanel.__init__(self, parent)

        self._parent = parent
        self._zoom = 100
        self._renderTime = 0.00
        self._rendering = False
        self._viewportImage = utils.ConvertImageToWx(Image.new('RGBA', (256, 256)))

        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyEvent)

    def OnDrawBackground(self, dc):
        dc.SetBackground(wx.Brush('grey'))
        dc.Clear()
        utils.DrawCheckerBoard(dc, self.GetClientRect(), wx.Colour("#424242"), box=8)

    def OnDrawScene(self, dc):
        image = self._viewportImage
        x = (self.Size[0] - image.Width)/2.0
        y = (self.Size[1] - image.Height)/2.0
        dc.DrawBitmap(image, x, y, useMask=False)

    def OnDrawInterface(self, dc):
        gc = wx.GraphicsContext.Create(dc)
        gc.SetBrush(wx.Brush(wx.Colour(0, 0, 0, 110)))
        gc.DrawRectangle(0, 0, self.Size[0], 26)

        self._zoom = round(self.GetScaleX()*100)
        text = self.CreateInfoText(self._renderTime, self._zoom, self._rendering)
        fnt = self._parent.GetFont()
        gc.SetFont(fnt, wx.Colour('white'))
        gc.DrawText(text, 22, 2)

    def OnKeyEvent(self, event):
        code = event.GetKeyCode()
        mouse = wx.Point(self.Size[0]/2, self.Size[1]/2)

        # plus (+)
        if code == wx.WXK_NUMPAD_ADD:
            self.ScenePostScale(1.1, 1.1, mouse[0], mouse[1])
        # minus (-)
        elif code == wx.WXK_NUMPAD_SUBTRACT:
            self.ScenePostScale(0.9, 0.9, mouse[0], mouse[1])
        self.UpdateDrawing()

    def CreateInfoText(self, render_time, zoom, rendering=False):
        if rendering == False:
            info = "Render Finished in {0} sec. | Zoom {1}%".format(render_time, zoom)
        else:
            info = "Rendering image..."
        return info

    def UpdateInfoText(self, rendering=False):
        self._rendering = rendering
        self.UpdateDrawing()

    def UpdateViewerImage(self, image, render_time):
        """ Update the Image Viewport. This refreshes everything
        in the Viewport.

        :param image: wx.Bitmap
        :param float render_time: float value of the image's render time
        """
        self._renderTime = render_time
        self._viewportImage = image
        self.UpdateDrawing()
