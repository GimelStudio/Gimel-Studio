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
## FILE: radio_buttons.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Defines custom-drawn radio buttons
## ----------------------------------------------------------------------------

import wx

from GimelStudio.utils import ConvertImageToWx


class MenuButton(object):
    def __init__(
        self, parent, image, rect=wx.Rect(0, 0, 56, 56), _id=wx.ID_ANY
        ):
        self._parent = parent
        self._image = image
        self._rect = rect

        if _id == wx.ID_ANY:
            self._id = wx.NewIdRef()
        else:
            self._id = _id

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

    def Draw(self, dc, hide=False):
        dc.ClearId(self.GetId())
        dc.SetId(self.GetId())

        if hide == False:
            pos = self._parent.GetMenuButtonWidgetPos()
            self.SetRect(wx.Rect(pos[0]+4, pos[1]+4, 56, 56))

            dc.SetPen(wx.Pen(wx.Colour((55, 55, 55, 255)), 2))
            dc.SetBrush(wx.Brush(wx.Colour("#6D6F6E")))
            dc.DrawCircle(self.GetRect()[0]+32, self.GetRect()[1]+32, 30)

            dc.DrawBitmap(
                self.GetImage(),
                self.GetRect()[0]+5,
                self.GetRect()[1]+5,
                True # Use alpha mask
                )

        dc.SetIdBounds(self.GetId(), self.GetRect())
