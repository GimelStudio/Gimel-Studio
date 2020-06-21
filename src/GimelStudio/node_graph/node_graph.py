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
## FILE: node_graph.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the node graph panel
## ----------------------------------------------------------------------------


# =============================================================================
#                               File Contents
# =============================================================================
# Due to the size of this file, here is a table of contents of how things 
# should be ordered in this file to keep things tidy:
# -----------------------------------------------------------------------------
# 0. Imports & IDs
# 1. Init method(s) 
# 2. Methods dealing with drawing the NodeGraph, coord utils, etc.
# 3. Event handler methods starting with "On". (e.g: OnLeftDown)
# 4. Value methods starting with "Get" or "Set" (e.g: GetParent)
# 5. Other
# -----------------------------------------------------------------------------


import math
import wx
import wx.adv

from GimelStudio.utils import DrawGrid
from GimelStudio.node import Node, Wire



ID_SELECTION_BBOX = wx.NewIdRef()



class NodeGraph(wx.ScrolledCanvas):
    def __init__(self, parent, size=wx.DefaultSize):
        wx.ScrolledWindow.__init__(self, parent, size=size)
 
        self._parent = parent
        self._maxWidth = size[0] #TODO
        self._maxHeight = size[1] #TODO
 
        self._nodes = {}
        self._selectedNodes = []
        self._activeNode = None

        self._srcNode = None
        self._srcPlug = None
        self._tmpWire = None
        self._bboxRect = None
        self._middlePnt = None

        self._pdc = wx.adv.PseudoDC()

        # Handle scrolling
        self.SetScrollbars(1, 1, self._maxWidth, self._maxHeight, 0, 0)

        # Nodegraph Bindings
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: None)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleDown)
        self.Bind(wx.EVT_MIDDLE_UP, self.OnMiddleUp)

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        dc = wx.GCDC(dc)

        dc.SetBackground(wx.Brush(wx.Colour('#F7F7F7')))
        dc.Clear()

        rect = self.GetViewableWindowRegion()
        self.DoPrepareDC(dc)

        #self._DrawGridBackground(dc, rect)
        self._pdc.DrawToDCClipped(dc, rect)

    @staticmethod
    def _DrawGridBackground(dc, rect):
        dc.SetBrush(wx.Brush(wx.Colour('#373737'), wx.CROSS_HATCH))
        dc.DrawRectangle(rect)

    def ConvertCoords(self, pnt):
        """ Convert coords to account for scrolling.

        :param pnt: the given wx.Point coord to convert
        :returns: wx.Point
        """
        xv, yv = self.GetViewStart()
        xd, yd = self.GetScrollPixelsPerUnit()
        return wx.Point(pnt[0] + (xv * xd), pnt[1] + (yv * yd))

    def GetViewableWindowRegion(self):
        """ Get the shown scrolled region of the window based on 
        the current scrolling.

        :returns: wx.Rect
        """
        xv, yv = self.GetViewStart()
        xd, yd = self.GetScrollPixelsPerUnit()
        x, y = (xv * xd, yv * yd)
        rgn = self.GetUpdateRegion()
        rgn.Offset(x, y)
        return rgn.GetBox()  

    def RefreshGraph(self):
        """ Refreshes the nodegraph so that everything is redrawn. 
        
        Use after .Draw() calls:
        >> node.Draw(self._pdc)
        >> self.RefreshGraph()
        """
        rect = wx.Rect(0, 0, self._maxWidth, self._maxHeight)
        #rect =  self.GetViewableWindowRegion()
        self.RefreshRect(rect, False)
        self.Refresh()

    def OnLeftDown(self, event):
        pnt = event.GetPosition()
        winpnt = self.ConvertCoords(pnt)
        self._srcNode = self.NodeHitTest(winpnt)

        # Handle adding a node from the node registry 
        # if LEFT mousebtn and the CTRL key are down.
        selected_item = None#self.GetParent().GetNodeRegistry().GetSelectedItem()
        if wx.GetKeyState(wx.WXK_CONTROL) == True and selected_item != None:
            self.AddNode(selected_item)

        else:
            # The node has been clicked
            if self._srcNode != None:
                self._HandleNodeSelection()

                # Handle plugs and wires
                self._srcPlug = self._srcNode.HitTest(winpnt.x, winpnt.y)
                if self._srcPlug != None:
                    # Handle disconnecting and connecting plugs
                    if self._srcPlug.GetWires() == []:
                        # Do not allow connections from anything except
                        # the output socket
                        if self._srcPlug.IsOutputType() == True:
                            pnt1 = self._srcNode.GetRect().GetPosition() \
                                    + self._srcPlug.GetPosition()
                            self._tmpWire = Wire(
                                pnt1, 
                                pnt, 
                                None, 
                                None, 
                                self._srcPlug.GetType()
                                )

                    else:
                        # Do not allow disconnections from the output socket
                        if self._srcPlug.IsOutputType() != True:
                            wires = self._srcPlug.GetWires()
                            dst = wires[0].dstPlug
                            src = wires[0].srcPlug
                            dst.Disconnect(src)

            else:
                # Start the box select bbox
                self._bboxStart = winpnt

        self._lastPnt = pnt
            
        # Refresh the nodegraph
        self.RefreshGraph()

 
    def OnMotion(self, event):
        pnt = event.GetPosition()
        winpnt = self.ConvertCoords(pnt)

        # If the MMB is down, calculate the scrolling of the graph
        if event.MiddleIsDown() == True:
            self.ScrollNodeGraph(
                winpnt[0] - self._middlePnt[0],
                winpnt[1] - self._middlePnt[1]
                )

        # Draw box selection bbox
        if event.LeftIsDown() == True and self._srcNode == None:
            self._bboxRect = wx.Rect(
                topLeft=self._bboxStart, 
                bottomRight=winpnt
                )
            self._pdc.RemoveId(ID_SELECTION_BBOX)
            self._pdc.SetId(ID_SELECTION_BBOX)

            self._pdc.SetPen(
                wx.Pen(wx.Colour('#C2C2C2'), 2.5, wx.PENSTYLE_SHORT_DASH)
                )
            self._pdc.SetBrush(
                wx.Brush(wx.Colour(100, 100, 100, 56), wx.SOLID)
                )
            self._pdc.DrawRectangle(self._bboxRect)
            
            # This is needed here because the
            # box select must update in realtime.
            self.RefreshGraph()

        if not event.LeftIsDown() or self._srcNode == None:
            return

        if self._srcNode.IsDisabled() != True:
            if self._srcPlug == None:
                dpnt = pnt - self._lastPnt
                self._pdc.TranslateId(self._srcNode.GetId(), dpnt[0], dpnt[1])
                rect = self._pdc.GetIdBounds(self._srcNode.GetId())
                self._lastPnt = pnt
                self._srcNode.SetRect(rect)

                # Redraw the wires
                if self._srcNode.GetPlugs() != []:
                    for plug in self._srcNode.GetPlugs():
                        for wire in plug.GetWires(): 
                            pnt1 = wire.srcNode.GetRect().GetPosition() + wire.srcPlug.GetPosition()
                            pnt2 = wire.dstNode.GetRect().GetPosition() + wire.dstPlug.GetPosition()
                            self.DrawNodeWire(self._pdc, wire, pnt1, pnt2)

            elif self._tmpWire != None:
                # Set the wire to be active when it is being edited.
                self._tmpWire.SetActive(True)
                self.DrawNodeWire(self._pdc, self._tmpWire, pnt2=winpnt)

        # Refresh the nodegraph
        self.RefreshGraph()


    def OnLeftUp(self, event):
        # Attempt to make a connection
        if self._srcNode != None:
            pnt = event.GetPosition()
            winpnt = self.ConvertCoords(pnt)
            dstnode = self.NodeHitTest(winpnt)

            if dstnode != None:
                rect = self._pdc.GetIdBounds(self._srcNode.GetId())
                dstplug = dstnode.HitTest(
                    winpnt.x, winpnt.y, 
                    thumb_btn_active=True
                    )
                
                # Make sure not to allow the same datatype or 
                # 'plug type' of sockets to be connected! 
                if dstplug != None \
                    and self._srcPlug.GetType() != dstplug.GetType() \
                    and self._srcNode.GetId() != dstnode.GetId() \
                    and self._srcPlug.GetDataType() == dstplug.GetDataType():
                    
                    # Only allow a single node to be
                    # connected to any one socket.
                    if len(dstplug.GetWires()) < 1:
                        self._srcPlug.Connect(dstplug)
                        
                    # If there is already a connection,
                    # but a wire is "dropped" into the plug
                    # disconnect the last connection and
                    # connect the current wire.
                    else:
                        wires = dstplug.GetWires()
                        dst = wires[0].dstPlug
                        src = wires[0].srcPlug
                        dst.Disconnect(src, render=False)
                        self._srcPlug.Connect(dstplug)
 
        # We can erase the temp wire.
        if self._tmpWire != None:
            rect = self._pdc.GetIdBounds(self._tmpWire.GetId())
            self._pdc.RemoveId(self._tmpWire.GetId()) 

        # Clear selection bbox and set nodes as selected
        if self._bboxRect != None:
            self._pdc.RemoveId(ID_SELECTION_BBOX)
            self._selectedNodes = self.BoxSelectHitTest(self._bboxRect)
            for node in self._selectedNodes:
                if node.IsSelected() != True and node.IsActive() != True:
                    node.SetSelected(True)
                    node.Draw(self._pdc)

        # Reset all values 
        self._srcNode = None
        self._srcPlug = None
        self._tmpWire = None
        self._bboxRect = None

        # Update the properties panel
        self.NodePropertiesPanel.UpdatePanelContents(self.GetActiveNode())

        # Refresh the nodegraph
        self.RefreshGraph()

 
    def _HandleNodeSelection(self):
        # Set the active node
        if self._activeNode == None:
            self._activeNode = self._srcNode
            self._activeNode.SetActive(True)
            self._activeNode.Draw(self._pdc)
            
        else:
            # We check to make sure this is not just the same
            # node clicked again, then we switch the active states.
            if self._srcNode.GetId() != self._activeNode.GetId():
                self._activeNode.SetActive(False)
                self._activeNode.Draw(self._pdc)
                
                self._activeNode = self._srcNode

                self._activeNode.SetActive(True)
                self._activeNode.Draw(self._pdc)

        # When a node is active, all the selected nodes
        # need to be set to the unselected state.
        if self.GetSelectedNodes() != []:
            for node in self.GetSelectedNodes():
                node.SetSelected(False)
                node.Draw(self._pdc)


    def OnMiddleDown(self, event): 
        winpnt = self.ConvertCoords(event.GetPosition())
        self._middlePnt = winpnt

        # Update mouse cursor
        self.SetCursor(wx.Cursor(wx.CURSOR_SIZING))


    def OnMiddleUp(self, event):
        # Reset mouse cursor
        self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))







    @property
    def NodePropertiesPanel(self):
        return self._parent.GetNodePropertyPanel()

    def GetParent(self):
        return self._parent

    def GetNodes(self):
        """ Returns a list of all the nodes in the current 
        graph. Used by the render engine to access the nodes. """
        return self._nodes

    def GetSelectedNodes(self):
        return self._selectedNodes

    def SetSelectedNodes(self, selectednodes):
        self._selectedNodes = selectednodes

    def GetActiveNode(self):
        return self._activeNode

    def SetActiveNode(self, activenode):
        self._activeNode = activenode

    def GetNodeRegistry(self):
        return self._parent.GetNodeRegistry()

    def GetPDC(self):
        return self._pdc







    @staticmethod
    def GetNodePlug(node, plug):
        return node.GetPlug(plug)

    @staticmethod
    def DrawNodeWire(dc, wire, pnt1=None, pnt2=None):
        if pnt1 != None:
            wire.SetPoint1(pnt1)
        if pnt2 != None:
            wire.SetPoint2(pnt2)
        wire.Draw(dc)


    def ScrollNodeGraph(self, pos_x, pos_y):
        """ Scrolls the scrollbars to the specified position. """
        scrollpos_x = self.GetScrollPos(wx.HORIZONTAL)
        scrollpos_y = self.GetScrollPos(wx.VERTICAL)

        self.Scroll(scrollpos_x-pos_x,
                    scrollpos_y-pos_y
                    )
        self.RefreshGraph()


    def NodeHitTest(self, pnt):
        idxs = self._pdc.FindObjects(pnt[0], pnt[1], 5)
        hits = [
            idx 
            for idx in idxs
            if idx in self._nodes
        ]
        if hits != []:
            return self._nodes[hits[0]]
        else:
            # Make sure we deselect everything
            for node in self._selectedNodes:
                node.SetSelected(False)
                node.Draw(self._pdc)
            self._selectedNodes = []

            if self._activeNode != None:
                self._activeNode.SetActive(False)
                self._activeNode.Draw(self._pdc)
                self._activeNode = None
            return None

    def BoxSelectHitTest(self, bboxrect):
        nodehits = []
        for node in self._nodes.values():
            if bboxrect.Intersects(node.GetRect()) == True:
                nodehits.append(node)

        if nodehits != []:
            return nodehits

        else:
            # Make sure we deselect everything
            for node in self._selectedNodes:
                node.SetSelected(False)
                node.Draw(self._pdc)
            self._selectedNodes = []
            return []



  
    def AddNode(self, _type, _id=wx.ID_ANY, pos=wx.Point(0, 0), 
        fromfile=False, fromdirdnd=False, fromregistrydnd=False):
        """ Adds a node of the given type to the nodegraph. """

        node = self.GetNodeRegistry().CreateNode(self, _type, pos, _id)
        node_id = node.GetId()
        #print('ADDED-> ', nId)
        #if node._category == 'INPUT':
            #node.SetThumbnailPreviewOpen(redraw=False)
        node.Draw(self._pdc, False)
        self._pdc.SetIdBounds(node_id, node.GetRect())
        self._nodes[node_id] = node
        self.RefreshGraph()
        return node
