## ----------------------------------------------------------------------------
## Gimel Studio © 2020 CorrectSyntax Software, Noah Rahm. All rights reserved.
##
## FILE: wire.py
## AUTHOR(S): Noah Rahm
## PURPOSE: -
## ----------------------------------------------------------------------------

import wx


class Wire(object):
    """ Wire for connecting nodes. """
    def __init__(self, pnt1, pnt2, srcplug, dstplug, dir_, 
        isactive=False, curvature=0, drawshadow=True):
        self._pnt1 = pnt1
        self._pnt2 = pnt2
        self._id = wx.NewIdRef()
        self._dir = dir_
        self._srcPlug = srcplug
        self._dstPlug = dstplug
        self._isActive = isactive
        self._curvature = curvature
        self._drawShadow = drawshadow

    def GetPoint1(self):
        return self._pnt1

    def SetPoint1(self, pnt):
        self._pnt1 = pnt

    def GetPoint2(self):
        return self._pnt2

    def SetPoint2(self, pnt):
        self._pnt2 = pnt

    def GetId(self):
        return self._id

    def SetId(self, id_):
        self._id = id_

    def GetSrcPlug(self):
        return self._srcPlug

    def SetSrcPlug(self, plug):
        self._srcPlug = plug

    def GetDstPlug(self):
        return self._dstPlug

    def SetDstPlug(self, plug):
        self._dstPlug = plug

    def IsActive(self):
        return self._isActive

    def SetActive(self, is_active):
        self._isActive = is_active

    def GetCurvature(self):
        return self._curvature

    def SetCurvature(self, curvature):
        self._curvature = curvature

    def GetDrawShadow(self):
        return self._drawShadow

    def SetDrawShadow(self, draw_shadow=True):
        self._drawShadow = draw_shadow

    # TODO: is this being used?
    def GetRect(self):
        minX = min(self._pnt1[0], self._pnt2[0])
        minY = min(self._pnt1[1], self._pnt2[1])
        size = self._pnt2 - self._pnt1
        rect = wx.Rect(minX - 10, minY, abs(size[0]) + 20, abs(size[1]))
        return rect.Inflate(2, 2)

    def Draw(self, dc): 
        """ Draw the wire. 
        :param dc: the wx DC to draw on
        """
        dc.ClearId(self.GetId())
        dc.SetId(self.GetId())

        sign = 1
        # Check if this is plug type IN
        if self._dir == 0:
            sign = -1

        # Curvature of the wire
        curvature = int(self.GetCurvature() * 2)

        if self.GetCurvature() != 0:
            # Draw wire
            pnts = []
            pnts.append(self._pnt1)
            pnts.append(self._pnt1 + wx.Point(curvature * sign, 0))
            pnts.append(self._pnt2 - wx.Point(curvature * sign, 0))
            pnts.append(self._pnt2)

            if self.IsActive() == True:
                dc.SetPen(wx.Pen('#ECECEC', 2))
            else:
                dc.SetPen(wx.Pen('#C1C1C1', 2))
            dc.DrawSpline(pnts)

            # Draw shadow
            if self.GetDrawShadow() == True:
                pnts = []
                pnts.append(self._pnt1)
                pnts.append(self._pnt1 + wx.Point(curvature * sign -5, 0))
                pnts.append(self._pnt2 - wx.Point(curvature * sign +5, 0))
                pnts.append(self._pnt2)

                dc.SetPen(wx.Pen(wx.Colour(0, 0, 0, 43), 8))
                dc.DrawSpline(pnts)

        else:
            # Draw wire
            if self.IsActive() == True:
                dc.SetPen(wx.Pen('#ECECEC', 2))
            else:
                dc.SetPen(wx.Pen('#C1C1C1', 2))
            dc.DrawLine(self._pnt1[0], self._pnt1[1], self._pnt2[0], self._pnt2[1])

            # Draw shadow
            if self.GetDrawShadow() == True:
                dc.SetPen(wx.Pen(wx.Colour(0, 0, 0, 43), 8))
                dc.DrawLine(self._pnt1[0], self._pnt1[1], self._pnt2[0], self._pnt2[1])

        dc.SetIdBounds(self.GetId(), self.GetRect())

