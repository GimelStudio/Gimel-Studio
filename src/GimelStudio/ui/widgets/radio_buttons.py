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
## FILE: radio_buttons.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Defines custom-drawn radio buttons 
## ----------------------------------------------------------------------------

import wx

from GimelStudio.utils import ConvertImageToWx



class ModeRadioButton(object):
    def __init__(
        self, parent, image, modestr='',
        rect=wx.Rect(0, 0, 40, 40), _id=wx.ID_ANY
        ):
        self._parent = parent
        self._image = image
        self._rect = rect
        self._modeString = modestr
        self._isActive = False
        self._isHover = False
        
        if _id == wx.ID_ANY:
            self._id = wx.NewIdRef()
        else:
            self._id = _id

    def GetModeString(self):
        return self._modeString

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

    def SetImage(self, image):
        self._image = image

    def GetImage(self):
        return self._image

    def SetActive(self, isactive):
        self._isActive = isactive

    def GetActive(self):
        return self._isActive

    def SetHover(self, ishover):
        self._isHover = ishover

    def GetHover(self):
        return self._isHover

    def Draw(self, dc):
        dc.ClearId(self.GetId())
        dc.SetId(self.GetId())

        pos = self._parent.GetRadioButtonWidgetsPos()
        self.SetRect(wx.Rect(pos[0], self.GetRect()[1], 40, 40))

        if self.GetActive() == True:
            dc.SetBrush(wx.Brush(wx.Colour('#80b3ffff')))
        elif self.GetHover() == True:
            dc.SetBrush(wx.Brush(wx.Colour('#80b3ffff')))
        else:
            dc.SetBrush(wx.Brush(wx.Colour('#666666ff')))

        dc.DrawRoundedRectangle(self.GetRect(), 2)

        dc.DrawBitmap(
            self.GetImage(),
            self.GetRect()[0],
            self.GetRect()[1],
            True # Use alpha mask
            )

        dc.SetIdBounds(self.GetId(), self.GetRect())
