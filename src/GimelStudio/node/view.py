# ----------------------------------------------------------------------------
# Gimel Studio Copyright 2019-2020 by Noah Rahm and contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# FILE: view.py
# AUTHOR(S): Noah Rahm
# PURPOSE: Define the view, which handles the drawing of the node, etc.
# ----------------------------------------------------------------------------

import wx

from GimelStudio import utils
from GimelStudio.datafiles.icons import *


class NodeView(object):
    """ Handles the graphical side of the node. """

    def __init__(self, _id):
        # _viewData is purposely set to None here to avoid confusion of
        # whether these are the startup default values -these are
        # actually updated from the node model on app init so it doesn't
        # make sense to put any default values here!
        self._viewData = {}

    def GetId(self):
        return self._viewData['id']

    def GetType(self):
        return self._viewData['type']

    def GetHeaderColor(self):
        return self._viewData['header_color']

    def GetColor(self):
        return self._viewData['color']

    def GetSocketColor(self):
        return self._viewData['socket_color']

    def GetTextColor(self):
        return self._viewData['text_color']

    def GetBorderColor(self):
        return self._viewData['border_color']

    def IsMuted(self):
        return self._viewData['muted']

    def IsSelected(self):
        return self._viewData['selected']

    def IsActive(self):
        return self._viewData['active']

    def IsOutput(self):
        return self._viewData['is_output']

    def GetSize(self):
        return self._viewData['size']

    def GetPosition(self):
        return self._viewData['position']

    def GetLabel(self):
        return self._viewData['label']

    def GetSockets(self):
        return self._viewData['sockets']

    def GetThumbImage(self):
        return self._viewData['thumbnail']

    def GetLastSocketCoords(self):
        return self._viewData['last_socket_coords']

    @property
    def ViewData(self):
        """ Return the node view data attributes (properties).

        :returns dict: {property_name: property_value}
        """
        return self._viewData

    def GetRect(self):
        return wx.Rect(
            self.GetPosition()[0], self.GetPosition()[1],
            self.GetSize()[0], self.GetSize()[1]
        )

    def Draw(self, dc):
        dc.ClearId(self.GetId())
        dc.SetId(self.GetId())

        thumb = self.GetThumbImage()

        x, y, w, h = self.GetRect()

        # Main body of the node
        dc.SetPen(wx.Pen(wx.Colour(self.GetBorderColor()), 2))
        dc.SetBrush(wx.Brush(wx.Colour(self.GetColor()), wx.SOLID))
        dc.DrawRoundedRectangle(x, y, w, h, 4)

        # Node header
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.Brush(wx.Colour(self.GetHeaderColor()), wx.SOLID))
        dc.DrawRoundedRectangle(x + 1, y + 1, w - 3, 24, 2)

        # Node text
        dc.SetTextForeground(wx.Colour(self.GetTextColor()))
        dc.DrawText(utils.TruncateText(self.GetLabel()), x + 6, y + 3)

        # Thumbnail
        thumbnail_width = round((w - 10) / 1.1)
        thumbnail_height = thumb.size[1]

        _x = thumbnail_width / 2.0 - thumb.size[0] / 2.0
        _y = thumbnail_height / 2.0 - thumb.size[1] / 2.0

        thumb_rect = wx.Rect(x + ((w - thumbnail_width) / 2),
                             y + _y + 20 + self.GetLastSocketCoords(),
                             thumbnail_width,
                             thumbnail_height)

        # Draw thumbnail border and background
        dc.SetPen(wx.Pen(wx.Colour("#2B2B2B"), 1))
        dc.SetBrush(wx.Brush(ICON_BRUSH_CHECKERBOARD.GetBitmap()))
        dc.DrawRectangle(thumb_rect)

        # Draw thumbnail image
        dc.DrawBitmap(
            wx.Bitmap(utils.ConvertImageToWx(thumb)),
            x + _x + ((w - thumbnail_width) / 2),
            y + _y + 20 + self.GetLastSocketCoords(),
            True
        )

        # Sockets
        for socket in self.GetSockets():
            socket.Draw(dc)

        dc.SetIdBounds(self.GetId(), self.GetRect())
