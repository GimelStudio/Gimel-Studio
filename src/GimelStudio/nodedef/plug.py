## ----------------------------------------------------------------------------
## Gimel Studio © 2020 Correct Syntax, Noah Rahm. All rights reserved.
##
## FILE: plug.py
## AUTHOR(S): Noah Rahm
## PURPOSE: -
## ----------------------------------------------------------------------------

import math
import wx

from .wire import Wire

 
class Plug(object):
    def __init__(self, label, datatype, pos, radius, type_, node):
        self._id = wx.NewIdRef()
        self._label = label # text
        self._node = node
        self._pos = wx.Point(pos[0], pos[1])  # In node space
        self._radius = radius
        self._type = type_
        self._dataType = datatype
        self._wires = []

    def GetId(self):
        return self._id

    def GetLabel(self):
        return self._label

    def SetLabel(self, label):
        self._label = label

    def GetNode(self):
        return self._node

    def SetNode(self, node):
        self._node = node

    def GetPosition(self):
        return self._pos

    def SetPosition(self, pos):
        self._pos = pos

    def GetRadius(self):
        return self._radius

    def GetType(self):
        return self._type

    def SetType(self, type_):
        self._type = type_

    def IsOutputType(self):
        if self.GetType() == 1:
            return True
        else:
            return False

    def GetDataType(self):
        return self._dataType

    def SetDataType(self, data_type):
        self._dataType = data_type

    def GetWires(self):
        return self._wires

    def Draw(self, dc):
        #print(self.GetNode().GetName(), self.GetLabel(), self.GetWires())

        final = self.GetPosition() + self.GetNode().GetRect().GetPosition()
         
        # Set color
        dc.SetPen(wx.Pen(wx.Colour('#373737'), 1))

        datatype = self.GetDataType()
        if datatype == 'image':
            dc.SetBrush(wx.Brush(wx.Colour('#C7C729'), wx.SOLID))
        elif datatype == 'color':
            dc.SetBrush(wx.Brush(wx.Colour('#63C763'), wx.SOLID))
        elif datatype == 'vector':
            dc.SetBrush(wx.Brush(wx.Colour('#6363C7'), wx.SOLID))
        else:
            dc.SetBrush(wx.Brush(wx.Colour('#9B9B9B'), wx.SOLID))

        # Draw the plug
        dc.DrawCircle(final.x, final.y, self.GetRadius())

        tdc = wx.WindowDC(wx.GetApp().GetTopWindow())
        w, h = tdc.GetTextExtent(self.GetLabel())

        # Plug title margin
        if self._type == 0:
            x = final.x + 10 
        else:
            x = final.x - w - 3

        dc.DrawText(self.GetLabel(), x, final.y - h / 2)

    def HitTest(self, pos):
        pnt = pos - self.GetPosition()
        dist = math.sqrt(math.pow(pnt.x, 2) + math.pow(pnt.y, 2))
        
        # Plug hit radius
        if math.fabs(dist) < 10:
            return True

    def Connect(self, dst_plug, render=True):
        #print ('Connecting:', self.GetLabel(), '->', dst_plug.GetLabel())
        # Make the connection
        dst_plug.GetNode().MakeConnection(self, dst_plug, render)

        pt1 = self.GetNode().GetRect().GetPosition() + self.GetPosition()
        pt2 = dst_plug.GetNode().GetRect().GetPosition() + dst_plug.GetPosition()
        wire = Wire(pt1, pt2, self, dst_plug, self.GetType())
        wire.srcNode = self.GetNode()
        wire.dstNode = dst_plug.GetNode()
        wire.srcPlug = self
        wire.dstPlug = dst_plug
        self._wires.append(wire)
        dst_plug.GetWires().append(wire)

        dc = self.GetNode().GetParent().GetPDC()
        wire.Draw(dc)
        self.GetNode().GetParent().RefreshRect(wire.GetRect(), False)

        self.GetNode().GetParent().RefreshGraph()

    def Disconnect(self, connected_node, render=True):
        for wire in self.GetWires():
            # Disconnect
            self.GetNode().MakeDisconnect(wire.srcPlug, wire.dstPlug, render)

            del wire.srcNode# = self.GetNode()
            del wire.dstNode# = dstPlug.GetNode()
            del wire.srcPlug# = self
            del wire.dstPlug# = dstPlug
            self.GetNode().GetParent().RefreshRect(wire.GetRect(), False)
            self._wires = []
            self.GetNode().GetParent().GetPDC().RemoveId(wire.GetId())

        for wire in connected_node.GetWires():
            connected_node.GetNode().GetParent().RefreshRect(wire.GetRect(), False)
            connected_node._wires = []
            self.GetNode().GetParent().GetPDC().RemoveId(wire.GetId())

        self.GetNode().GetParent().RefreshGraph()

        
        
