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
## FILE: sample_color_popup.py
## AUTHOR(S): Noah Rahm
## PURPOSE: -
## ----------------------------------------------------------------------------

import wx

# TODO: UNUSED

class ColorSamplePopup(object):
    def __init__(
        self, parent, rect=wx.Rect(0, 0, 40, 40), _id=wx.ID_ANY
        ):
        self._parent = parent
        self._rect = rect
        self._colorSample = wx.Colour(0, 0, 0, 0)
        self._isActive = False
        self._isHover = False
        
        if _id == wx.ID_ANY:
            self._id = wx.NewIdRef()
        else:
            self._id = _id

    def GetColorSample(self):
        return self._colorSample

    def SetColorSample(self, wx_color):
        self._colorSample = wx_color

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


    def Draw(self, dc):
        dc.ClearId(self.GetId())
        dc.SetId(self.GetId())

        dc.SetBrush(wx.Brush(self.GetColorSample()))
        dc.DrawRoundedRectangle(self.GetRect(), 2)

        dc.SetIdBounds(self.GetId(), self.GetRect())
