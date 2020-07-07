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
## FILE: image_viewport.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the Image Viewport panel
## ----------------------------------------------------------------------------

import wx
import wx.adv

from PIL import Image

from .viewer_pnl import ImageViewerPnl
from .export_pnl import ImageExportPnl
from GimelStudio.utils import ConvertImageToWx, DrawCheckerBoard
from GimelStudio.datafiles.icons import *



class ImageViewport(wx.Toolbook):
    def __init__(self, parent):
        wx.Toolbook.__init__(self, parent, -1, style=wx.BK_LEFT)

        self._parent = parent
        
        #FIXME
        img_list = [ICON_NODE_IMAGE_DARK, ICON_NODE_IMAGE_LIGHT] 
        il = wx.ImageList(20, 20)
        for x in range(2):
            bmp = img_list[x].GetBitmap()
            il.Add(bmp)
        self.AssignImageList(il)
        
        # Make panels for the list book
        self._imageViewerPanel = ImageViewerPnl(self)
        self._imageExportPanel = ImageExportPnl(self)

        self.AddPage(self._imageViewerPanel, "View", imageId=0)
        self.AddPage(self._imageExportPanel, "Export", imageId=1)

        self.Bind(wx.EVT_TOOLBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_TOOLBOOK_PAGE_CHANGING, self.OnPageChanging)


    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()

        # If the Export Image tab is selected, generate 
        # the preview image.
        if sel == 1:
            self._imageExportPanel.UpdatePreviewImage(self.GetRenderedImage())
        event.Skip()

    def OnPageChanging(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        event.Skip()

    def GetRenderedImage(self):
        return self._parent.GetRenderedImage()

    def UpdateViewerImage(self, image, render_time):
        self._imageViewerPanel.UpdateViewerImage(image, render_time)

            