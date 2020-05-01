## ----------------------------------------------------------------------------
## Gimel Studio © 2020 Correct Syntax, Noah Rahm. All rights reserved.
##
## FILE: sample_color_popup.py
## AUTHOR(S): Noah Rahm
## PURPOSE: -
## ----------------------------------------------------------------------------

import wx



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
