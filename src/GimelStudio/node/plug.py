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
## FILE: plug.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the node plug class
##
## This file includes code that was modified from wxnodegraph 
## (https://github.com/Derfies/wxnodegraph) which is licensed under the MIT 
## License, Copyright 2016
## ----------------------------------------------------------------------------

import math
import wx

from .wire import Wire
from GimelStudio.stylesheet import *

 
class Plug(object):
    def __init__(self, label, datatype, pos, radius, type_, node):
        self._id = wx.NewIdRef()
        self._label = label 
        self._node = node
        self._pos = wx.Point(pos[0], pos[1])  # In node space
        self._radius = radius
        self._type = type_
        self._dataType = datatype
        self._wires = []

    @property
    def Theme(self):
        return self.GetNode().Theme

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
        dc.SetPen(wx.Pen(wx.Colour(self.Theme["node_plug_border"]), 2))

        datatype = self.GetDataType()
        if datatype == "RENDERIMAGE":
            dc.SetBrush(wx.Brush(wx.Colour('#C7C729'), wx.SOLID))

        # Other data-type that have not been defined in the API, yet...
        elif datatype == "COLOR":
            dc.SetBrush(wx.Brush(wx.Colour('#63C763'), wx.SOLID))
        elif datatype == "VECTOR":
            dc.SetBrush(wx.Brush(wx.Colour('#6363C7'), wx.SOLID))
        else:
            dc.SetBrush(wx.Brush(wx.Colour('#9B9B9B'), wx.SOLID))

        # Draw the plug
        dc.DrawCircle(final.x, final.y, self.GetRadius())

        tdc = wx.WindowDC(wx.GetApp().GetTopWindow())
        w, h = tdc.GetTextExtent(self.GetLabel())

        # Plug title margin
        if self._type == 0:
            x = final.x + 12 
        else:
            x = final.x - w - 18

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
        wire = Wire(self, pt1, pt2, self, dst_plug, self.GetType())
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
