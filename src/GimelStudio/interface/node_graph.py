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

import math
import wx
import wx.adv

from GimelStudio.utils import DrawGrid
from GimelStudio.registry import CreateNode
from GimelStudio.node import Wire


ID_SELECTION_BBOX = wx.NewIdRef()



class NodeGraph(wx.ScrolledCanvas):
    def __init__(self, parent, size=wx.DefaultSize):
        wx.ScrolledCanvas.__init__(self, parent, size=size)
        
        self._parent = parent

        # Set Node Graph to 10000x10000 pixels max
        self._maxWidth = 10000
        self._maxHeight = 10000
 
        self._nodes = {}
        self._selectedNodes = []
        self._activeNode = None

        self._srcNode = None
        self._srcPlug = None
        self._tmpWire = None
        #self._bboxRect = None
        #self._bboxStart = None
        self._middlePnt = None
        self._nodePreviewToggled = False

        self._nodeMenuItemIdMapping = {}

        self._pdc = wx.adv.PseudoDC()
        self._drawGrid = True

        # Handle scrolling
        self.SetScrollbars(1, 1, self._maxWidth, self._maxHeight, 5000, 5000)

        # Nodegraph Bindings
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: None)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleDown)
        self.Bind(wx.EVT_MIDDLE_UP, self.OnMiddleUp)

        self.Bind(wx.EVT_SIZE, self.OnSize)

 
    def _DrawGridBackground(self, dc, rect):
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.Brush(wx.Colour('#525960'), wx.CROSS_HATCH))
        dc.DrawRectangle(rect)

    def OnPaint(self, event):
        """ Node Graph paint event handler. """
        dc = wx.BufferedPaintDC(self)
        dc = wx.GCDC(dc)

        dc.SetBackground(wx.Brush(wx.Colour("#505050")))
        dc.Clear()

        rect = self.GetViewableWindowRegion()
        self.DoPrepareDC(dc)
  
        # Draw the grid background
        if self.ShouldDrawGrid() == True:
            self._DrawGridBackground(dc, rect)

        self._pdc.DrawToDCClipped(dc, rect)

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
        
        Use after ``.Draw()`` calls:

            node.Draw(self._pdc)
            self.RefreshGraph()
        """
        rect = wx.Rect(0, 0, self._maxWidth, self._maxHeight)
        self.RefreshRect(rect, True) # False
        self.Refresh()



    def OnSize(self, event):
        """ Panel resize event handler. """
        self.RefreshGraph()



    def OnLeftDown(self, event):
        pnt = event.GetPosition()
        winpnt = self.ConvertCoords(pnt)
        self._srcNode = self.NodeHitTest(winpnt)


        # The node has been clicked
        if self._srcNode != None:
            self._HandleNodeSelection()


            # Handle plugs and wires
            self._srcPlug = self._srcNode.HitTest(winpnt.x, winpnt.y)
            if self._srcPlug != None:
                # Handle disconnecting and connecting plugs
                #if len(self._srcPlug.GetWires()) < 3:# == []:

                # Do not allow connections from anything except
                # the output socket
                if self._srcPlug.IsOutputType() == True:
                    pnt1 = self._srcNode.GetPosition() \
                            + self._srcPlug.GetPosition()
                    
                    self._tmpWire = Wire(
                        self,
                        pnt1, 
                        pnt, 
                        None, 
                        None, 
                        self._srcPlug.GetType(),
                        curvature=8
                        )

                #else:
                # Do not allow disconnections from the output socket
                elif self._srcPlug.IsOutputType() != True:
                    wires = self._srcPlug.GetWires()
                    dst = wires[0].dstPlug
                    self._srcPlug = wires[0].srcPlug
                    dst.Disconnect(
                        self,
                        self._srcPlug,
                        render=True
                        )

                    # Create the temp wire again
                    pnt = event.GetPosition()
                    winpnt = self.ConvertCoords(pnt)
                    pnt1 = self._srcPlug.GetNode().GetPosition() \
                            + self._srcPlug.GetPosition()

                    # Draw the temp wire with the new values
                    self._tmpWire = Wire(
                        self,
                        pnt1, 
                        pnt, 
                        None, 
                        None, 
                        self._srcPlug.GetType(),
                        curvature=8
                        )

                    # Important: we re-assign the source node variable
                    self._srcNode = self._srcPlug.GetNode()

                            
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


        if not event.LeftIsDown() or self._srcNode == None:
            return

        # Move the node
        if self._srcNode.IsMuted() != True:
            if self._srcPlug == None:
                dpnt = pnt - self._lastPnt
                self._pdc.TranslateId(self._srcNode.GetId(), dpnt[0], dpnt[1])
                rect = self._pdc.GetIdBounds(self._srcNode.GetId())
                self._lastPnt = pnt
                self._srcNode.SetRect(rect)

                # Redraw the wires
                if self._srcNode.GetSockets() != []:
                    for plug in self._srcNode.GetSockets():
                        for wire in plug.GetWires(): 
                            pnt1 = wire.srcNode.GetPosition() \
                                    + wire.srcPlug.GetPosition()
                            pnt2 = wire.dstNode.GetPosition() \
                                    + wire.dstPlug.GetPosition()
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
                dstplug = dstnode.HitTest(winpnt.x, winpnt.y)
                
                # Make sure not to allow the same datatype or 
                # 'plug type' of sockets to be connected! 
                if dstplug != None \
                    and self._srcPlug.GetType() != dstplug.GetType() \
                    and self._srcNode.GetId() != dstnode.GetId() \
                    and self._srcPlug.GetDataType() == dstplug.GetDataType():
                    
                    # Only allow a single node to be
                    # connected to any one socket.
                    if len(dstplug.GetWires()) < 1:
                        self._srcPlug.Connect(
                            self,
                            dstplug,
                            render=False
                            )
                        
                    # If there is already a connection,
                    # but a wire is "dropped" into the plug
                    # disconnect the last connection and
                    # connect the current wire.
                    else:
                        wires = dstplug.GetWires()
                        dst = wires[0].dstPlug
                        src = wires[0].srcPlug
                        dst.Disconnect(self, src, render=False)
                        self._srcPlug.Connect(
                            self,
                            dstplug, 
                            render=True
                            )
 
        # We can erase the temp wire.
        if self._tmpWire != None:
            rect = self._pdc.GetIdBounds(self._tmpWire.GetId())
            self._pdc.RemoveId(self._tmpWire.GetId()) 

        # Reset all values 
        self._srcNode = None
        self._srcPlug = None
        self._tmpWire = None

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
        """ Event that updates the cursor. """
        winpnt = self.ConvertCoords(event.GetPosition())
        self._middlePnt = winpnt

        # Update mouse cursor
        self.SetCursor(wx.Cursor(wx.CURSOR_SIZING))

    def OnMiddleUp(self, event):
        """ Event that resets the cursor. """
        # Reset mouse cursor
        self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))

    @property
    def NodePropertiesPanel(self):
        return self._parent._nodePropertyPanel

    # @property
    # def Theme(self):
    #     return self._parent.Theme

    # @property
    # def UserPrefs(self):
    #     return self._parent.GetUserPrefManager()

    def GetParent(self):
        return self._parent

    def GetNodes(self):
        """ Returns a list of all the nodes in the current 
        graph. Used by the render engine to access the nodes. 
        """
        return self._nodes

    def GetSelectedNodes(self):
        return self._selectedNodes

    def SetSelectedNodes(self, selectednodes):
        self._selectedNodes = selectednodes

    def GetActiveNode(self):
        return self._activeNode

    def SetActiveNode(self, activenode):
        self._activeNode = activenode

    def GetPDC(self):
        return self._pdc

    def ShouldDrawGrid(self):
        return self._drawGrid

    def SetShouldDrawGrid(self, draw_grid=True):
        self._drawGrid = draw_grid

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
            self.DeselectNodes()
            return None

    # FIXME
    def DeselectNodes(self):
        # Make sure we deselect everything
        for node in self._selectedNodes:
            node.SetSelected(False)
            node.Draw(self._pdc)
        self._selectedNodes = []

        if self._activeNode != None:
            self._activeNode.SetActive(False)
            self._activeNode.Draw(self._pdc)
            self._activeNode = None


    def UpdateAllNodes(self):
        for nodeId in self.GetNodes():
            self._nodes[nodeId].Draw(self._pdc)
        self.RefreshGraph()

    def AddNode(self, name="", _id=wx.ID_ANY, pos=wx.Point(0, 0), where="DEFAULT"):
        """ Adds a node of the given name to the Node Graph. 

        :param name: the node IDName string to add to the Node Graph. If this is an
        empty string (default), it will default to the core Input Image node.
        :param _id: id of the node. Creates a new id if not specified
        :param pos: ``wx.Point`` position to add the node to the Node Graph
        :param where: flag specifying different positioning for adding the node.
        This value can be a string of either:
        DEFAULT (default): position the node based on the ``pos`` param
        CURSOR: position the node based on the current cursor position
        """

        if where == "CURSOR":
            pos = self.ConvertCoords(
                self.ScreenToClient(wx.GetMousePosition())
                )

        # If the name param is an empty string, default to
        # the core Input Image node. 
        # if name == "":
        #     name = "gimelstudiocorenode_image" # Yes, this is hard-coded...

        #node = self.GetNodeRegistry().CreateNode(self, name, pos, _id)
         
        #print(pos, "pos")
            
        node = CreateNode(self, name, pos, _id)
        node_id = node.GetId()
        node.Draw(self._pdc)
        self._nodes[node_id] = node
        self.RefreshGraph()
        return node

