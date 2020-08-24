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


# Create IDs
ID_SELECTION_BBOX = wx.NewIdRef()
 
# Max number of nodes that can be added to the menu is 100, currently
CONTEXTMENU_ADDNODE_IDS = wx.NewIdRef(100)

ID_CONTEXTMENU_DELETENODE = wx.NewIdRef()
ID_CONTEXTMENU_DELETENODES = wx.NewIdRef()
ID_CONTEXTMENU_ENABLEDISABLENODE = wx.NewIdRef()
ID_CONTEXTMENU_DUPLICATENODE = wx.NewIdRef()
ID_CONTEXTMENU_DESELECTALLNODES = wx.NewIdRef()
ID_CONTEXTMENU_SELECTALLNODES = wx.NewIdRef() 


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
        self._bboxRect = None
        self._middlePnt = None

        self._nodeMenuItemIdMapping = {}

        self._pdc = wx.adv.PseudoDC()

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

        # Context menu bindings
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)

        self._parent.Bind(
            wx.EVT_MENU, 
            self.OnDeleteNode, 
            id=ID_CONTEXTMENU_DELETENODE
            )
        self._parent.Bind(
            wx.EVT_MENU, 
            self.OnDeleteNodes, 
            id=ID_CONTEXTMENU_DELETENODES
            )
        self._parent.Bind(
            wx.EVT_MENU, 
            self.OnEnableDisableNode, 
            id=ID_CONTEXTMENU_ENABLEDISABLENODE
            )
        self._parent.Bind(
            wx.EVT_MENU, 
            self.OnSelectAllNodes, 
            id=ID_CONTEXTMENU_SELECTALLNODES
            )
        self._parent.Bind(
            wx.EVT_MENU, 
            self.OnDeselectAllNodes, 
            id=ID_CONTEXTMENU_DESELECTALLNODES
            )
        self._parent.Bind(
            wx.EVT_MENU, 
            self.OnDuplicateNode, 
            id=ID_CONTEXTMENU_DUPLICATENODE
            )
        
        # Keyboard shortcut bindings
        self.accel_tbl = wx.AcceleratorTable([(wx.ACCEL_ALT, ord('M'), 
                                              ID_CONTEXTMENU_ENABLEDISABLENODE),
                                              (wx.ACCEL_ALT, ord('X'), 
                                              ID_CONTEXTMENU_DELETENODE),
                                              (wx.ACCEL_SHIFT, ord('X'), 
                                              ID_CONTEXTMENU_DELETENODES),
                                              (wx.ACCEL_SHIFT, ord('D'), 
                                              ID_CONTEXTMENU_DUPLICATENODE)
                                             ])
        self._parent.SetAcceleratorTable(self.accel_tbl)


    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        dc = wx.GCDC(dc)

        dc.SetBackground(wx.Brush(wx.Colour(self.Theme["node_graph_bg"])))
        dc.Clear()

        rect = self.GetViewableWindowRegion()
        self.DoPrepareDC(dc)

        # Draw the grid background if the active UI theme allows it
        if self.Theme["node_graph_grid"] == "true":
            self._DrawGridBackground(dc, rect)

        self._pdc.DrawToDCClipped(dc, rect)

    def _DrawGridBackground(self, dc, rect):
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
        
        Use after ``.Draw()`` calls:

            node.Draw(self._pdc)
            self.RefreshGraph()
        """
        rect = wx.Rect(0, 0, self._maxWidth, self._maxHeight)
        self.RefreshRect(rect, False)
        self.Refresh()


    def OnSelectMenuItem(self, event):
        """ Event when an "Add Node" menu item is selected, which adds the
        node to the Node Graph.
        """
        self.AddNode(self._nodeMenuItemIdMapping[event.GetId()], where="CURSOR")

        
    def OnContextMenu(self, event):
        """ Event to create Node Graph context menu on left click. """

        # Context menu
        contextmenu = wx.Menu()

        # Add node submenu
        addnodemenu = wx.Menu()

        # Add submenus
        inputnodemenu = wx.Menu()
        distortnodemenu = wx.Menu()
        valuenodemenu = wx.Menu()
        filternodemenu = wx.Menu()
        blendnodemenu = wx.Menu()
        colornodemenu = wx.Menu()
        convertnodemenu = wx.Menu()
        othernodemenu = wx.Menu()
        
        # List nodes in menu
        nodes = self.GetNodeRegistry().GetAvailableNodes()

        i = 0
        for node_name in nodes:
            node_obj = nodes[node_name]()
            node_category = node_obj.NodeCategory
            node_label = node_obj.NodeLabel

            if node_category == "INPUT":
                inputnodemenu.Append(CONTEXTMENU_ADDNODE_IDS[i], node_label)
            elif node_category == "DISTORT":
                distortnodemenu.Append(CONTEXTMENU_ADDNODE_IDS[i], node_label)
            elif node_category == "VALUE":
                valuenodemenu.Append(CONTEXTMENU_ADDNODE_IDS[i], node_label)
            elif node_category == "FILTER":
                filternodemenu.Append(CONTEXTMENU_ADDNODE_IDS[i], node_label)
            elif node_category == "BLEND":
                blendnodemenu.Append(CONTEXTMENU_ADDNODE_IDS[i], node_label)
            elif node_category == "COLOR":
                colornodemenu.Append(CONTEXTMENU_ADDNODE_IDS[i], node_label)
            elif node_category == "CONVERT":
                convertnodemenu.Append(CONTEXTMENU_ADDNODE_IDS[i], node_label)
            else:
                othernodemenu.Append(CONTEXTMENU_ADDNODE_IDS[i], node_label)

            self._nodeMenuItemIdMapping[CONTEXTMENU_ADDNODE_IDS[i]] = node_name
            self.Bind(
                wx.EVT_MENU, 
                self.OnSelectMenuItem, 
                id=CONTEXTMENU_ADDNODE_IDS[i]
                )
            i += 1

        addnodemenu.AppendSubMenu(inputnodemenu, "Input")
        addnodemenu.AppendSubMenu(distortnodemenu, "Distort")
        addnodemenu.AppendSubMenu(filternodemenu, "Filter")
        addnodemenu.AppendSubMenu(blendnodemenu, "Blend")
        addnodemenu.AppendSubMenu(colornodemenu, "Color")
        addnodemenu.AppendSubMenu(convertnodemenu, "Convert")
        addnodemenu.AppendSubMenu(valuenodemenu, "Value")
        addnodemenu.AppendSubMenu(othernodemenu, "Other")
         
        contextmenu.Append(wx.ID_ANY, "Add Node", addnodemenu)

        # If there is an active node, then we know
        # that there shouldn't be any other nodes 
        # selected, thus we handle the active node first.
        if self._activeNode != None:
            # Do not allow the output node to be 
            # deleted, duplicated or disabled at all.
            if self._activeNode.IsCompositeOutput() != True:
                contextmenu.Append(
                    ID_CONTEXTMENU_DUPLICATENODE, "Duplicate\tShift+D"
                    )
                contextmenu.Append(
                    ID_CONTEXTMENU_DELETENODE, "Delete\tAlt+X"
                    )
                if self._activeNode.IsDisabled() == True: 
                   contextmenu.Append(
                       ID_CONTEXTMENU_ENABLEDISABLENODE, "Toggle Mute\tAlt+M"
                       )
                else:
                   contextmenu.Append(
                       ID_CONTEXTMENU_ENABLEDISABLENODE, "Toggle Mute\tAlt+M"
                       )
                
        else:
            if self._selectedNodes != []:
               contextmenu.Append(
                   ID_CONTEXTMENU_DELETENODES, "Delete Selected\tShift+X"
                   ) 

        contextmenu.Append(ID_CONTEXTMENU_SELECTALLNODES, "Select All") 
        contextmenu.Append(ID_CONTEXTMENU_DESELECTALLNODES, "Deselect All")

        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(contextmenu)
        contextmenu.Destroy()


    def OnDeleteNodes(self, event):
        """ Event that deletes the selected nodes. """
        self.DeleteNodes()
        self._parent.Render()

    def OnDeleteNode(self, event):
        """ Event that deletes a single selected node. """
        if self._activeNode != None \
            and self._activeNode.IsCompositeOutput() != True:
            self._activeNode.Delete()
            self._activeNode = None

        # Update the properties panel so that the deleted 
        # nodes' properties are not still shown!
        self.NodePropertiesPanel.UpdatePanelContents(self.GetActiveNode())
        
        self.RefreshGraph()
        self._parent.Render()


    def OnEnableDisableNode(self, event):
        """ Event that toggles a node's disabled/enabled state. """
        if self._activeNode.IsDisabled() == True:
            self._activeNode.SetDisabled(False)
        else:
            self._activeNode.SetDisabled(True)
        self._activeNode.Draw(self._pdc)
        self.RefreshGraph()


    def OnSelectAllNodes(self, event):
        """ Event that selects all the nodes in the Node Graph. """
        for node_id in self._nodes:
            node = self._nodes[node_id]
            if node.IsActive() == True:
                node.SetActive(False)
            node.SetSelected(True)
            node.Draw(self._pdc)
            self._selectedNodes.append(node)
        self.RefreshGraph()


    def OnDeselectAllNodes(self, event):
        """ Event that deselects all the currently selected nodes. """
        for node_id in self._nodes:
            node = self._nodes[node_id]
            node.SetSelected(False)
            node.Draw(self._pdc)
        self._selectedNodes = []
        self.RefreshGraph()


    def OnDuplicateNode(self, event): 
        """ Event that duplicates the currently selected node. """
        self.DuplicateNode(self._activeNode)


    def OnLeftDown(self, event):
        pnt = event.GetPosition()
        winpnt = self.ConvertCoords(pnt)
        self._srcNode = self.NodeHitTest(winpnt)

        # Handle adding a node from the node registry 
        # if LEFT mousebtn and the CTRL key are down.
        # TODO: UNUSED AT THE MOMENT!
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
                                self,
                                pnt1, 
                                pnt, 
                                None, 
                                None, 
                                self._srcPlug.GetType(),
                                curvature=self.Theme["node_wire_curving"]
                                )
  
                    else:
                        # Do not allow disconnections from the output socket
                        if self._srcPlug.IsOutputType() != True:
                            wires = self._srcPlug.GetWires()
                            dst = wires[0].dstPlug
                            self._srcPlug = wires[0].srcPlug
                            dst.Disconnect(
                                self._srcPlug,
                                render=self.UserPrefs.GetRendererAutoRender()
                                )

                            # Create the temp wire again
                            pnt = event.GetPosition()
                            winpnt = self.ConvertCoords(pnt)
                            pnt1 = self._srcPlug.GetNode().GetRect().GetPosition() \
                                    + self._srcPlug.GetPosition()

                            # Draw the temp wire with the new values
                            self._tmpWire = Wire(
                                self,
                                pnt1, 
                                pnt, 
                                None, 
                                None, 
                                self._srcPlug.GetType(),
                                curvature=self.Theme["node_wire_curving"]
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

        # Draw box selection bbox
        if event.LeftIsDown() == True \
            and self._srcNode == None and self._bboxStart != None:

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

        # Move the node
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
                            pnt1 = wire.srcNode.GetRect().GetPosition() \
                                    + wire.srcPlug.GetPosition()
                            pnt2 = wire.dstNode.GetRect().GetPosition() \
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
                        self._srcPlug.Connect(
                            dstplug,
                            render=self.UserPrefs.GetRendererAutoRender()
                            )
                        
                    # If there is already a connection,
                    # but a wire is "dropped" into the plug
                    # disconnect the last connection and
                    # connect the current wire.
                    else:
                        wires = dstplug.GetWires()
                        dst = wires[0].dstPlug
                        src = wires[0].srcPlug
                        dst.Disconnect(src, render=False)
                        self._srcPlug.Connect(
                            dstplug, 
                            render=self.UserPrefs.GetRendererAutoRender()
                            )
 
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
        return self._parent.GetNodePropertyPanel()

    @property
    def Theme(self):
        return self._parent.Theme

    @property
    def UserPrefs(self):
        return self._parent.GetUserPrefManager()

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

    def UpdateAllNodes(self):
        for nodeId in self.GetNodes():
            self._nodes[nodeId].Draw(self.GetPDC(), False)
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
        if name == "":
            name = "gimelstudiocorenode_image" # Yes, this is hard-coded...

        node = self.GetNodeRegistry().CreateNode(self, name, pos, _id)
        node_id = node.GetId()

        # Default to toggle the Input node thumb open
        if node.GetCategory() in ["INPUT"]:
            node.SetThumbnailPreviewOpen(redraw=False)
        node.Draw(self._pdc, False)
        self._pdc.SetIdBounds(node_id, node.GetRect())
        self._nodes[node_id] = node
        self.RefreshGraph()
        return node

 
    def DeleteNodes(self):
        """ Delete the currently selected nodes. This will refuse
        to delete the Output Composite node though, for obvious reasons.
        """
        for node in self._selectedNodes:
            if node.IsCompositeOutput() != True:
                node.Delete()
            else:
                # In the case that this is an output node, we 
                # want to deselect it, not delete it. :)
                node.SetSelected(False)
                node.Draw(self._pdc)
        self._selectedNodes = []
        
        if self._activeNode != None \
            and self._activeNode.IsCompositeOutput() != True:

            self._activeNode.Delete()
            self._activeNode = None

        # Update the properties panel so that the deleted 
        # nodes' properties are not still shown!
        self.NodePropertiesPanel.UpdatePanelContents(self.GetActiveNode())
        
        self.RefreshGraph()


    def ResetToDefault(self):
        """ Reset the Node Graph back to default. """
        self._nodes = {}
        self._activeNode = None
        self._selectedNodes = []
        self.GetPDC().RemoveAll()
        self.RefreshGraph()


    def DuplicateNode(self, node):
        """ Duplicates the given ``Node`` object with its properties.
        
        :param node: the ``Node`` object to duplicate
        :returns: the duplicate ``Node`` object
        """

        duplicate_node = self.AddNode(
            node.GetIDName(),  
            _id=wx.ID_ANY, 
            where="CURSOR"
            )

        # Assign the same properties to the duplicate node object
        for prop in node.GetEvaluationData()["properties"]:
            duplicate_node.EditProperties(prop["name"], prop["value"])
 
        self.RefreshGraph()
        return duplicate_node
