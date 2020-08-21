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
## FILE: export.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the image export options tab of the Image Viewport
## ----------------------------------------------------------------------------


import os

import wx
import wx.adv
from PIL import Image

from GimelStudio.utils import (ConvertImageToWx, ExportRenderedImageToFile, 
                                DrawCheckerBoard)
from GimelStudio.file_support import SupportFTSave
from GimelStudio.datafiles.icons import *



class ExportOptionsPnl(wx.StaticBox):
    def __init__(self, parent, label="Export Options", size=wx.DefaultSize):
        wx.StaticBox.__init__(self, parent, label=label, size=size)

        # This gets the recommended amount of border space to use for items
        # within in the static box for the current platform.
        top_bd, other_bd = self.GetBordersForSizer()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(top_bd)

        self._exportForWebCheckBox = wx.CheckBox(self, label="Export for web")
        self._opimizeImageCheckBox = wx.CheckBox(self, label="Optimize image (if available)")

        self._imageQualitySliderLbl = wx.StaticText(self, -1, "Image quality (if available)")
        self._imageQualitySlider = wx.Slider(
            self, value=75, minValue=0, maxValue=95, size=(250, -1),
            style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
            )
        self._imageQualitySlider.SetTickFreq(5)

        sizer.Add(self._exportForWebCheckBox, flag=wx.LEFT|wx.TOP, border=other_bd+10)
        sizer.Add((1, 5))
        sizer.Add(self._opimizeImageCheckBox, flag=wx.LEFT, border=other_bd+10)
        sizer.Add((1, 20))
        sizer.Add(self._imageQualitySliderLbl, flag=wx.LEFT, border=other_bd+10)
        sizer.Add(self._imageQualitySlider, flag=wx.LEFT, border=other_bd+10)

        self.SetSizer(sizer)

    def GetExportForWebValue(self):
        return self._exportForWebCheckBox.GetValue()

    def GetOpimizeImageValue(self):
        return self._opimizeImageCheckBox.GetValue()

    def GetImageQualityValue(self):
        return self._imageQualitySlider.GetValue()



class ImagePreviewPnl(wx.StaticBox):
    def __init__(self, parent, label="Image Preview", size=wx.DefaultSize):
        wx.StaticBox.__init__(self, parent, label=label, size=size)

        # This gets the recommended amount of border space to use for items
        # within in the static box for the current platform.
        top_bd, other_bd = self.GetBordersForSizer()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(top_bd)

        self._imgPreview = wx.StaticBitmap(self, -1, wx.Bitmap(100, 100))

        sizer.Add((1, 1), 1)
        sizer.Add(
            self._imgPreview, 
            flag=wx.ALIGN_CENTER_HORIZONTAL| wx.ALL | wx.ADJUST_MINSIZE,
            border=other_bd+10)
        sizer.Add((1, 1), 1)

        self.SetSizer(sizer)
        self.Refresh()

    def UpdatePreviewImage(self, image):
        img = ConvertImageToWx(image)
        img = wx.Bitmap.ConvertToImage(img)
        img_scale = self._CalculateScale(img.GetWidth(), img.GetHeight())
        img.Rescale(img_scale[0],img_scale[1])
        self._imgPreview.SetBitmap(wx.Bitmap(img))
        self.Layout()
        self.Refresh()

    def _CalculateScale(self, w, h):
        h_ratio = h/self.Size[0]
        w_ratio = w/self.Size[1]

        if h_ratio > w_ratio:
            return (w/h_ratio,h/h_ratio)
        else:
            return (w/w_ratio,h/w_ratio)



class ImageExportPnl(wx.Panel):
    def __init__(self, parent, size=wx.DefaultSize):
        wx.Panel.__init__(self, parent, size=size)

        self._parent = parent

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.splitter = wx.SplitterWindow(self, -1, style=wx.SP_BORDER|wx.SP_LIVE_UPDATE)
        self.splitter.SetMinimumPaneSize(50)

        self._exportOptionsPnl = ExportOptionsPnl(self.splitter)
        self._imagePreviewPnl = ImagePreviewPnl(self.splitter)

        self.splitter.SplitVertically(self._exportOptionsPnl, self._imagePreviewPnl)

        self.sizer.Add(self.splitter, 1, flag=wx.EXPAND | wx.ALL, border=6)
 
        self.innerSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.exportBtn = wx.Button(self, label="Export Image...")
        self.innerSizer.Add(self.exportBtn)
        self.sizer.Add(self.innerSizer, flag=wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM, border=6)
        
        self.SetSizer(self.sizer)

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_BUTTON, self.OnExportImageBtn)

    def OnSize(self, event):
        size = self.GetSize()
        self.splitter.SetSashPosition(size.x / 2)
        event.Skip()

    def OnExportImageBtn(self, event):
        self.OnExportImage(event)

    def OnExportImage(self, event):
        wildcard = "JPG file (*.jpg)|*.jpg|" \
                   "JPEG file (*.jpeg)|*.jpeg|" \
                   "PNG file (*.png)|*.png|" \
                   "BMP file (*.bmp)|*.bmp|" \
                   "GIF file (*.gif)|*.gif|" \
                   "EPS file (*.eps)|*.eps|" \
                   "PCX file (*.pcx)|*.pcx|" \
                   "XBM file (*.xbm)|*.xbm|" \
                   "WEBP file (*.webp)|*.webp|" \
                   "TGA file (*.tga)|*.tga|" \
                   "TIFF file (*.tiff)|*.tiff|" \
                   "All files (*.*)|*.*"

        dlg = wx.FileDialog(
            self, 
            message="Export rendered image as...", 
            defaultDir=os.getcwd(),
            defaultFile="untitled.png", 
            wildcard=wildcard, 
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
            )

        # This sets the default filter that the user will initially see. 
        # Otherwise, the first filter in the list will be used by default.
        dlg.SetFilterIndex(12)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            filetype = os.path.splitext(path)[1]

            if filetype not in SupportFTSave(list_all=True):
                dlg = wx.MessageDialog(
                    None, 
                    "That file type isn't currently supported!", 
                    "Cannot Save Image!", 
                    style=wx.ICON_EXCLAMATION
                    )
                dlg.ShowModal()    

            else:
                # Export the image with the export options
                ExportRenderedImageToFile(
                    rendered_image=self._parent.GetRenderedImage(), 
                    export_path=path,
                    quality=self._exportOptionsPnl.GetImageQualityValue(), 
                    optimize=self._exportOptionsPnl.GetOpimizeImageValue(), 
                    export_for_web=self._exportOptionsPnl.GetExportForWebValue()
                    )

                notify = wx.adv.NotificationMessage(
                    title="Image Exported Sucessfully",
                    message="Your image was exported to \n {}".format(path),
                    parent=None, flags=wx.ICON_INFORMATION)
                notify.Show(timeout=2) # 1 for short timeout, 100 for long timeout
            
        dlg.Destroy()

    @property
    def ExportOptionsPanel(self):
        return self._exportOptionsPnl

    @property
    def ImagePreviewPanel(self):
        return self._imagePreviewPnl

    def UpdatePreviewImage(self, image):
        """ Wrapper method to update the preview image. """
        if image == None:
            # Default preview image is a transparent 256x256 image
            image = Image.new('RGBA', (256, 256), (0, 0, 0, 1))
        return self._imagePreviewPnl.UpdatePreviewImage(image)
