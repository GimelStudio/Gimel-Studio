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
## FILE: image_viewer.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the image viewport
## ----------------------------------------------------------------------------

import os
import wx

from PIL import Image

from GimelStudio.utils import (ConvertImageToWx, DrawGrid,
                               DrawCheckerBoard)
from GimelStudio.ui.widgets import (ModeRadioButton, GenericImage,
                                    ColorSamplePopup)
from GimelStudio.datafiles.icons import *


# Create IDs
ID_IMAGE = wx.NewIdRef()
ID_INFOTEXT = wx.NewIdRef()

ID_MOVE_MODE_INFOTEXT = wx.NewIdRef()
ID_IMAGEINFO_MODE_INFOTEXT = wx.NewIdRef()

ID_MODERADIOBTN_MOVE = wx.NewIdRef()
ID_MODERADIOBTN_IMAGEINFO = wx.NewIdRef()


class ImageViewport(wx.Panel):
    def __init__(self, parent, size=wx.DefaultSize):
        wx.Panel.__init__(self, parent, size=size)

        self._parent = parent

        self._pdc = wx.adv.PseudoDC()
        self._maxwidth  = size[0]
        self._maxheight = size[1]
        self._size = size
        
        self._factor = 1.0
        self._imageCopy = None
        self._imgMode = 0
        
        self._renderTime = 0.00
        self._globalImageSlot = 1
        self._zoom = '0'
        self._nodesUsed = '0' # TODO: Remove this
        self._sampleColor = wx.Colour(0, 0, 0, 0)
        self._sampleColorPopup = ColorSamplePopup(self)
        self._image = GenericImage(self, Image.new('RGBA', (256, 256)))

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: None)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyEvent)
        self.Bind(wx.EVT_MIDDLE_UP, self.OnMiddleUp)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        
    def OnSize(self, event):
        if self._imageCopy != None:
            self.RefreshViewerImage(self._imageCopy, self._renderTime)

    def OnMiddleDown(self, event):
        pnt = event.GetPosition()
        self.lastPnt = pnt

    def OnMotion(self, event):
        if event.MiddleIsDown():
            self.MoveImage(event)

        if self.GetGlobalMode() == 'MOVE' and event.LeftIsDown():
            self.MoveImage(event)

        if self.GetGlobalMode() == 'IMAGEINFO':
            pass
            # self.SampleImagePixelColor(pnt[0], pnt[1])
            # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            # self._sampleColorPopup.SetColorSample(self.GetCurrentSampleColor())
            # self._sampleColorPopup.Draw(self._pdc)
            # self.RefreshViewer()


        # Hover for buttons
        pnt = event.GetPosition()
        for i in  self._modesDict:
            btn_region = wx.Region(self._modesDict[i].GetRect())
            if btn_region.Contains(pnt[0], pnt[1]):
                self._modesDict[i].SetHover(True)
                self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
            else:
                self._modesDict[i].SetHover(False)
            self._modesDict[i].Draw(self._pdc)  
        self.RefreshViewer()
 



    def OnMiddleUp(self,event):
        self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        self.RefreshViewer()


    def OnLeftDown(self, event):
        pnt = event.GetPosition()

        if self.GetGlobalMode() == 'MOVE':
            self.lastPnt = pnt

        elif self.GetGlobalMode() == 'IMAGEINFO':
            pass
            #self.SampleImagePixelColor(pnt[0], pnt[1])
            


    def OnLeftUp(self, event):
        pnt = event.GetPosition()

        # Handle the radio buttons
        mrb = self.ModeRadioButtonHitTest(pnt)
        if mrb != None:

            # Make the last button unactive
            mode = self._globalMode
            mode.SetActive(False)
            mode.Draw(self._pdc)

            # Make the current button active
            mode = self._modesDict[mrb.GetId()]
            mode.SetActive(True)
            self._globalMode = mode
            mode.Draw(self._pdc)

            self.UpdateInitModeUI()
            
        if self.GetGlobalMode() == 'MOVE':
            self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))

        self.RefreshViewer()
            

    def OnPaint(self, event):
        """ Paint the drawn objects to the screen. """
        dc = wx.BufferedPaintDC(self)
        dc = wx.GCDC(dc)

        dc.SetBackground(wx.Brush('#535353'))
        dc.Clear()

        rect = wx.Rect(0, 0, self.Size[0], self.Size[1])

        # Draw the checkered alpha background
        DrawCheckerBoard(dc, rect, wx.Colour(0, 0, 0, 98), box=10)
        
        self._pdc.DrawToDCClipped(dc, rect)

    def OnKeyEvent(self, event):
        code = event.GetKeyCode()
        if code == wx.WXK_NUMPAD_ADD: # plus (+)
            self.Rescale(1.25)
        elif code == wx.WXK_NUMPAD_SUBTRACT: # minus (-)
            self.Rescale(0.8)

    def OnMouseWheel(self, event):
        factor = 1.25
        if event.GetWheelRotation() < 0:
            factor = 0.8
        self.Rescale(factor)

    def MoveImage(self, event):
        self.SetCursor(wx.Cursor(wx.CURSOR_SIZING))
        pnt = event.GetPosition()
        dPnt = pnt - self.lastPnt
        self._pdc.TranslateId(self._image.GetId(), dPnt[0], dPnt[1])
        
        self.RefreshViewer()
        self.lastPnt = pnt
            
    def SetRenderTime(self, rendertime):
        self._renderTime = rendertime

    def SetZoom(self, zoom):
        self._zoom = zoom

    def SetNodesUsed(self, node_used):
        self._nodesUsed = node_used

    def Rescale(self, factor):
        """ Update the image; to be called from the mouse scroll event. """
        self.UpdateImage(self._imageCopy, factor)
        self.UpdateTopbarInfoText(self._zoom)

#      def SampleImagePixelColor(self, x, y):
#         #x = int(x/int(self._zoom)  )
#         #y = int(y/int(self._zoom)  )

# ##        x, y = self.ClientToScreen(
# ##            wx.Point(x, y)
# ##            )   
#         print(x, y, '<<<<<<??')
#         #try:
#         self._sampleColor = self._image.GetImage().getpixel((x, y))
#         if self._image.GetImage().mode == 'L':
#             print(self._sampleColor)
#             self._sampleColor = (self._sampleColor,)*3
#         else:
#             print(self._sampleColor)
#             self._sampleColor = self._sampleColor[:3] 


                #self.master.code_couleur = self.master.code_couleur[:3] # on enleve le canal alpha
##            self.master.couleur = '#%02x%02x%02x' % self.master.code_couleur
##            self.master.colorbar.maincolor.configure(bg = self.master.couleur)
##        except (IndexError, TypeError):
##            pass

    def UpdateImage(self, img, factor=0):
        """ Update the image by resizing to the correct dimensions. """
        # TODO: Switch to wx.Size instead of PIL?

        # Keep a copy of the image
        self._imageCopy = img.copy()

        # Resize to the zoomed dimensions
        self.width = img.size[0]
        self.height = img.size[1]
        ogHeight = self.height
        ogWidth = self.width

        self._factor = factor*self._factor
        if factor == 0:
            self._factor = 1

            xWin = self.Size[0] - 10
            yWin = self.Size[1] - 10
            winRatio = 1.0*xWin/yWin
            imgRatio = 1.0*self.width/self.height

        else:#TODO
            xWin = self.Size[0] - 100
            yWin = self.Size[1] - 100
            winRatio = 1.0*xWin/yWin
            imgRatio = 1.0*self.width/self.height
        
        mode = 0
        if (ogWidth <=1000 and ogHeight <= 1000) or self._imgMode == 1:
            mode = 1

        # Match the widths
        if imgRatio >= winRatio: 
            self.width = self._factor*xWin
            self.height = self._factor*xWin/imgRatio
            img = img.resize((int(self.width), int(self.height)), mode)

        # Match the heights
        else: 
            self.height = self._factor*yWin
            self.width = self._factor*yWin*imgRatio
            img = img.resize((int(self.width), int(self.height)), mode)
 
        self._zoom = str(int(100*self.width/ogWidth))
        
        self._image.SetImage(img)
        self._image.SetPosition(
            (self.Size[0] - self.width)/2.0,
            (self.Size[1] - self.height)/2.0
            ) 
        self._image.Draw(self._pdc)

        self.RefreshViewer()

        self.Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleDown)

    def UpdateTopbarInfoText(self, zoom):
        """ Update the top info text. """
        self._pdc.ClearId(ID_INFOTEXT)
        self._pdc.SetId(ID_INFOTEXT)
        self._pdc.SetBrush(wx.Brush(wx.Colour(0, 0, 0, 98)))
        self._pdc.DrawRectangle(0, 0, self.Size[0], 26)
        
        text = 'Image Slot: 1 | Render Time: {0} sec. | Zoom: {1}%'.format(
            round(self._renderTime, 3), 
            zoom
            )
        
        self._pdc.SetTextForeground('white')
        self._pdc.DrawText(text, 22, 2)
        print(self.GetGlobalMode())

        if self.GetGlobalMode() == 'IMAGEINFO':
            self.UpdateMoveInfoText()
        else:
            self._pdc.ClearId(ID_MOVE_MODE_INFOTEXT)

    def UpdateMoveInfoText(self):
        """ Update the move info text. """
        self._pdc.ClearId(ID_MOVE_MODE_INFOTEXT)
        self._pdc.SetId(ID_MOVE_MODE_INFOTEXT)
        self._pdc.SetBrush(wx.Brush(wx.Colour(0, 0, 0, 98)))
        print(self.GetImagePosition())
        text = 'Composite Size: {0}x{1}px | Total Nodes: {2}'.format(
            self._imageCopy.size[0],
            self._imageCopy.size[1],
            self._nodesUsed
            )
        
        self._pdc.SetTextForeground('white')
        self._pdc.DrawText(text, 22, self.GetBottomInfoTextPos()[1] - 70)

    def RefreshViewerImage(self, renderimage, rendertime):
        """ Update the image; to be called from the program backend. """
        self.SetRenderTime(rendertime)
        self.UpdateImage(renderimage)
        self.UpdateTopbarInfoText(self._zoom)
        self.UpdateModeRadioButtonWidgets()

    def GetRadioButtonWidgetsPos(self):
        return self.ClientToScreen(
            wx.Point(self.GetClientRect()[2] -50, self.GetClientRect()[2])
            )    

    def GetBottomInfoTextPos(self):
        return self.ClientToScreen(
            wx.Point(self.GetClientRect()[2] -50, self.GetClientRect()[3])
            )   

    def InitModeRadioButtonWidgets(self):
        pos = self.GetRadioButtonWidgetsPos()

        move_mrb = ModeRadioButton(
            self,
            ICON_MODE_MOVE_LIGHT.GetBitmap(),
            'MOVE',
            wx.Rect(pos[0], 40, 40, 40),
            ID_MODERADIOBTN_MOVE
            )
        move_mrb.SetActive(True)

        imageinfo_mrb = ModeRadioButton(
            self,
            ICON_MODE_IMAGEINFO_LIGHT.GetBitmap(),
            'IMAGEINFO',
            wx.Rect(pos[0], 86, 40, 40),
            ID_MODERADIOBTN_IMAGEINFO
            )

        self._modesDict = {
            ID_MODERADIOBTN_MOVE: move_mrb,
            ID_MODERADIOBTN_IMAGEINFO: imageinfo_mrb,
            }

        self._globalMode = move_mrb

    def UpdateInitModeUI(self):
        if self.GetGlobalMode() == 'MOVE':
            pass
            #self.UpdateMoveInfoText()
        elif self.GetGlobalMode() == 'IMAGEINFO':
            self.UpdateMoveInfoText()

        
    def UpdateModeRadioButtonWidgets(self):
        for mrbID in self._modesDict:
            self._modesDict[mrbID].Draw(self._pdc)

    def ModeRadioButtonHitTest(self, pt):
        idxs = self._pdc.FindObjects(pt[0], pt[1], 5)
        hits = [
            idx 
            for idx in idxs
            if idx in self._modesDict
        ]
        if hits != []:
            return self._modesDict[hits[0]]
        else:
            return None



    def GetGlobalMode(self):
        return self._globalMode.GetModeString()

    def GetImagePosition(self):
        return self._image.GetPosition()

    def GetCurrentSampleColor(self):
        return self._sampleColor

    def ResetToDefault(self):
        """ Reset the image viewer to the default. """
        self.SetRenderTime(0.00)
        self.UpdateImage(Image.new('RGBA', (256, 256)))
        self.SetZoom('0')
        self.UpdateTopbarInfoText(self._zoom)
        self.RefreshViewer()
        
    def RefreshViewer(self):
        """ Refresh the image viewer. """
        rect = wx.Rect(0, 0, self.Size[0], self.Size[1])
        self.RefreshRect(rect, False)

