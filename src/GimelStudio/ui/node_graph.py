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
## PURPOSE: Define the node graph
## ----------------------------------------------------------------------------

import math
import wx
import wx.adv

from GimelStudio.utils import DrawGrid
from GimelStudio.nodedef import Wire
from GimelStudio.nodedef import Node
from GimelStudio.nodedef import CreateNode, NODE_REGISTRY
from GimelStudio.nodedef import NodeFrame

# Create IDs
ID_CONTEXTMENU_ADDIMAGENODE = wx.NewIdRef()
ID_CONTEXTMENU_ADDGRADIENTIMAGENODE = wx.NewIdRef()
ID_CONTEXTMENU_ADDASSETNODE = wx.NewIdRef()

ID_CONTEXTMENU_ADDGAUSSIANBLURNODE = wx.NewIdRef()
ID_CONTEXTMENU_ADDRESIZENODE = wx.NewIdRef()
ID_CONTEXTMENU_ADDINTEGERNODE = wx.NewIdRef()
ID_CONTEXTMENU_ADDMIXNODE = wx.NewIdRef()
ID_CONTEXTMENU_ADDALPHACOMPOSITENODE = wx.NewIdRef()
ID_CONTEXTMENU_ADDNORMALMAPNODE = wx.NewIdRef()

ID_CONTEXTMENU_DELETENODE = wx.NewIdRef()
ID_CONTEXTMENU_ENABLEDISABLENODE = wx.NewIdRef()
ID_CONTEXTMENU_DUPLICATENODE = wx.NewIdRef()
ID_CONTEXTMENU_DESELECTALLNODES = wx.NewIdRef()
ID_CONTEXTMENU_SELECTALLNODES = wx.NewIdRef() 
ID_CONTEXTMENU_ADDNODEFRAME = wx.NewIdRef()
ID_CONTEXTMENU_DELETENODEFRAME = wx.NewIdRef()

ID_SELECTION_BBOX = wx.NewIdRef()


class NodeGraph(wx.ScrolledCanvas):
    def __init__(self, parent, propertiesframe, project, size=wx.DefaultSize):
        wx.ScrolledWindow.__init__(self, parent, size=size)
 
        self._parent = parent
        self._propertiesframe = propertiesframe
        self._project = project

        self._maxwidth = size[0]
        self._maxheight = size[1]
 
        self._nodes = {}
        self._selectednodes = []
        self._activenode = None
        self._nodeframes = {}
        self._selectednodeframe = None

        self._srcnode = None#srcNode
        self._srcplug = None#srcPlug
        self._tmpwire = None#tmpWire
        self._bboxRect = None
        self._middlePnt = None
        self._zoomValue = 1.0
        self._zoomFactor = 1.0

        self._zoom = 0
        
        # Create a PseudoDC to record our drawing
        self._pdc = wx.adv.PseudoDC()

        # Handle scrolling
        self.SetScrollbars(1, 1, self._maxwidth, self._maxheight, 0, 0)

        # Nodegraph Bindings
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: None)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDoubleClick)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseScroll)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleDown)
        self.Bind(wx.EVT_MIDDLE_UP, self.OnMiddleUp)

        # Context menu bindings
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
        self.Bind(wx.EVT_MENU, self.OnAddImageNode, id=ID_CONTEXTMENU_ADDIMAGENODE)
        self.Bind(wx.EVT_MENU, self.OnAddGradientImageNode, id=ID_CONTEXTMENU_ADDGRADIENTIMAGENODE)
        self.Bind(wx.EVT_MENU, self.OnAddAssetNode, id=ID_CONTEXTMENU_ADDASSETNODE)

        self.Bind(wx.EVT_MENU, self.OnAddGaussianBlurNode, id=ID_CONTEXTMENU_ADDGAUSSIANBLURNODE)
        self.Bind(wx.EVT_MENU, self.OnAddResizeNode, id=ID_CONTEXTMENU_ADDRESIZENODE)
        self.Bind(wx.EVT_MENU, self.OnAddIntegerNode, id=ID_CONTEXTMENU_ADDINTEGERNODE)
        self.Bind(wx.EVT_MENU, self.OnAddMixNode, id=ID_CONTEXTMENU_ADDMIXNODE)
        self.Bind(wx.EVT_MENU, self.OnAddAlphaCompositeNode, id=ID_CONTEXTMENU_ADDALPHACOMPOSITENODE)
        self.Bind(wx.EVT_MENU, self.OnAddNormalMapNode, id=ID_CONTEXTMENU_ADDNORMALMAPNODE)

        self.Bind(wx.EVT_MENU, self.OnDeleteNodes, id=ID_CONTEXTMENU_DELETENODE)
        self.Bind(wx.EVT_MENU, self.OnEnableDisableNode, id=ID_CONTEXTMENU_ENABLEDISABLENODE)
        self.Bind(wx.EVT_MENU, self.OnSelectAllNodes, id=ID_CONTEXTMENU_SELECTALLNODES)
        self.Bind(wx.EVT_MENU, self.OnDeselectAllNodes, id=ID_CONTEXTMENU_DESELECTALLNODES)
        self.Bind(wx.EVT_MENU, self.OnAddNodeFrame, id=ID_CONTEXTMENU_ADDNODEFRAME)
        self.Bind(wx.EVT_MENU, self.OnDeleteNodeFrame, id=ID_CONTEXTMENU_DELETENODEFRAME)


        self.Bind(wx.EVT_MENU, self.OnDuplicateNode, id=ID_CONTEXTMENU_DUPLICATENODE)
        #self.Bind(wx.EVT_MENU, self.OnResetNode, id=15)

        

    def OnAddImageNode(self, event):
        self.AddNode('corenode_image')

    def OnAddGradientImageNode(self, event):
        self.AddNode('corenode_gradientimage')

    def OnAddAssetNode(self, event):
        self.AddNode('corenode_asset')

    def OnAddGaussianBlurNode(self, event):
        self.AddNode('corenode_gaussianblur')
        
    def OnAddResizeNode(self, event):
        self.AddNode('corenode_resize')

    def OnAddIntegerNode(self, event):
        self.AddNode('integer')

    def OnAddMixNode(self, event):
        self.AddNode('corenode_mix')

    def OnAddAlphaCompositeNode(self, event):
        self.AddNode('corenode_alphacomposite')

    def OnAddNormalMapNode(self, event):
        self.AddNode('corenode_tonormalmap')

    def OnContextMenu(self, evt):
        # Context menu
        contextmenu = wx.Menu()

        # Add node submenu
        addnodemenu = wx.Menu()

        inputnodemenu = wx.Menu()
        inputnodemenu.Append(ID_CONTEXTMENU_ADDIMAGENODE, "Image")
        inputnodemenu.Append(ID_CONTEXTMENU_ADDASSETNODE, "Asset")
        inputnodemenu.Append(ID_CONTEXTMENU_ADDGRADIENTIMAGENODE, "Gradient Image")

        distortnodemenu = wx.Menu()
        distortnodemenu.Append(ID_CONTEXTMENU_ADDRESIZENODE, "Resize")

        valuenodemenu = wx.Menu()
        #valuenodemenu.Append(ID_CONTEXTMENU_ADDINTEGERNODE, "Integer")

        filternodemenu = wx.Menu()
        filternodemenu.Append(ID_CONTEXTMENU_ADDGAUSSIANBLURNODE, "Gaussian Blur")

        blendnodemenu = wx.Menu()
        blendnodemenu.Append(ID_CONTEXTMENU_ADDMIXNODE, "Mix")
        blendnodemenu.Append(ID_CONTEXTMENU_ADDALPHACOMPOSITENODE, "Alpha Composite")

        colornodemenu = wx.Menu()
        #colornodemenu.Append(101, "")

        outputnodemenu = wx.Menu()
        #outputnodemenu.Append(121, "")

        convertnodemenu = wx.Menu()
        convertnodemenu.Append(ID_CONTEXTMENU_ADDNORMALMAPNODE, "To Normal Map")

        addnodemenu.AppendSubMenu(inputnodemenu, "Input")
        addnodemenu.AppendSubMenu(distortnodemenu, "Distort")
        addnodemenu.AppendSubMenu(valuenodemenu, "Value")
        addnodemenu.AppendSubMenu(filternodemenu, "Filter")
        addnodemenu.AppendSubMenu(blendnodemenu, "Blend")
        addnodemenu.AppendSubMenu(colornodemenu, "Color")
        addnodemenu.AppendSubMenu(outputnodemenu, "Output")
        addnodemenu.AppendSubMenu(convertnodemenu, "Convert")
        
        contextmenu.Append(wx.ID_ANY, "Add Node", addnodemenu)

        # Context menu items
        contextmenu.Append(ID_CONTEXTMENU_ADDNODEFRAME, "Add Node Frame")

        if self._selectednodeframe != None:
            contextmenu.Append(ID_CONTEXTMENU_DELETENODEFRAME, "Delete Node Frame") 

        contextmenu.Append(ID_CONTEXTMENU_SELECTALLNODES, "Select All Nodes") 
        contextmenu.Append(ID_CONTEXTMENU_DESELECTALLNODES, "Deselect All Nodes")

        # If there is an active node, then we know
        # that there shouldn't be any other nodes 
        # selected, thus we handle the active node first.
        if self._activenode != None:
            # Do not allow the output node to be 
            # deleted, duplicated or disabled at all.
            if self._activenode.IsCompositeNode() != True:
                contextmenu.Append(ID_CONTEXTMENU_DELETENODE, "Delete Node")
                if self._activenode.IsDisabled() == True: 
                   contextmenu.Append(ID_CONTEXTMENU_ENABLEDISABLENODE, "Enable Node")
                else:
                   contextmenu.Append(ID_CONTEXTMENU_ENABLEDISABLENODE, "Disable Node")
                contextmenu.Append(ID_CONTEXTMENU_DUPLICATENODE, "Duplicate Node")

        else:
            if self._selectednodes != []:
               contextmenu.Append(ID_CONTEXTMENU_DELETENODE, "Delete Nodes") 
            else:
                pass

        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(contextmenu)
        contextmenu.Destroy()
 
    def OnPaint(self, event):
        _dc = wx.BufferedPaintDC(self)
        dc = wx.GCDC(_dc)

        # We need to clear the dc BEFORE calling PrepareDC.
        dc.SetBackground(wx.Brush(wx.Colour('#505050')))
        dc.Clear()

        # Use DoPrepareDC to set position correctly.
        self.DoPrepareDC(dc)

        # Create a clipping rect from our position and size
        # and the Update Region.
        xv, yv = self.GetViewStart()
        dx, dy = self.GetScrollPixelsPerUnit()
        x, y = (xv * dx, yv * dy)
        rgn = self.GetUpdateRegion()
        rgn.Offset(x, y)
        r = rgn.GetBox()  

        # Draw the grid background
        self._DrawGridBackground(dc, r)

        #dc.SetUserScale(self.GetMouseScrollValue(), self.GetMouseScrollValue())

        # Draw to the dc using the calculated clipping rect.
        self._pdc.DrawToDCClipped(dc, r)

    def OnMouseScroll(self, event):
        """ TODO: NEEDS WORK """
        factor = 1.25
        if event.GetWheelRotation() < 0:
            factor = 0.8

        self._zoomFactor = factor*self._zoomFactor
        if self._zoomFactor > 1.3:
            #print("max")
            self._zoomFactor = 1.3
        else:
            if self._zoomFactor < 0.6:
                #print("min")
                self._zoomFactor = 0.6
        self.SetMouseScrollValue(self._zoomFactor)
        self.RefreshGraph()


    def OnLeftDoubleClick(self, event):
        if wx.GetKeyState(wx.WXK_ALT) == True:
            self._selectednodeframe.EditColorDialog()
            self._selectednodeframe.Draw(self._pdc)

        else:
            self._selectednodeframe.EditTextDialog()
            self._selectednodeframe.Draw(self._pdc)

        self.RefreshGraph()
        
    def OnLeftDown(self, event):
        pnt2 = event.GetPosition()
        winpnt = self.ConvertCoords(pnt2)

        # Handle adding a node from the node registry 
        # if LEFT mousebtn and the CTRL key are down.
        selected_item = self.GetParent().GetNodeRegistry().GetSelectedItem()
        if wx.GetKeyState(wx.WXK_CONTROL) == True and selected_item != None:
            self.AddNode(selected_item)

        else:
            self._srcnode = self.NodeHitTest(winpnt)
            if self._srcnode != None:
                # Handle active node selection
                if self._activenode == None:
                    self._activenode = self._srcnode
                    self._activenode.SetActive(True)
                    self._activenode.Draw(self._pdc)
                    
                else:  
                    if self._srcnode.GetId() != self._activenode.GetId():
                        self._activenode.SetActive(False)
                        self._activenode.Draw(self._pdc)
                        
                        self._activenode = self._srcnode

                        self._activenode.SetActive(True)
                        self._activenode.Draw(self._pdc)

                # Deselect node frame
                if self._selectednodeframe != None:
                    self._selectednodeframe.SetSelected(False)
                    self._selectednodeframe = None

                if self._selectednodes != []:
                    for node in self._selectednodes:
                        node.SetSelected(False)
                        node.Draw(self._pdc)

                # Handle plugs and wires
                self._srcplug = self._srcnode.HitTest(winpnt.x, winpnt.y)
                if self._srcplug != None:
                    # Handle disconnecting and connecting plugs
                    if self._srcplug.GetWires() == []:
                        # Do not allow connections from anything except
                        # the output socket
                        if self._srcplug.IsOutputType() == True:
                            pnt1 = self._srcnode.GetRect().GetPosition() \
                                 + self._srcplug.GetPosition()
                            self._tmpwire = Wire(
                                pnt1, 
                                pnt2, 
                                None, 
                                None, 
                                self._srcplug.GetType()
                                )

                    else:
                        # Do not allow disconnections from the output socket
                        if self._srcplug.IsOutputType() != True:
                            wires = self._srcplug.GetWires()
                            dst = wires[0].dstPlug
                            src = wires[0].srcPlug
                            dst.Disconnect(src)

            else:
                nodeframe = self.NodeFrameHitTest(winpnt)
                if nodeframe != None:
                    # Handle node frame selection
                    if self._selectednodeframe == None:
                        self._selectednodeframe = nodeframe
                        self._selectednodeframe.SetSelected(True)
                        self._selectednodeframe.Draw(self._pdc)
                        
                    else:  
                        if nodeframe.GetId() != self._selectednodeframe.GetId():
                            self._selectednodeframe.SetSelected(False)
                            self._selectednodeframe.Draw(self._pdc)
                            
                            self._selectednodeframe = nodeframe

                            self._selectednodeframe.SetSelected(True)
                            self._selectednodeframe.Draw(self._pdc)

                # Start bbox
                self._bboxStart = winpnt

            self._lastpnt = pnt2 
            
            # Refresh the nodegraph
            self.RefreshGraph()


    def OnMotion(self, event):
        # Calculate scrolling of graph
        if event.MiddleIsDown() == True:
            winpnt = self.ConvertCoords(event.GetPosition())
            self.ScrollNodeGraph(
                winpnt[0] - self._middlePnt[0],
                winpnt[1] - self._middlePnt[1]
                )
            
        # Draw selection bbox
        if event.LeftIsDown() == True \
           and self._srcnode == None \
           and self._selectednodeframe == None:
            self._bboxRect = wx.Rect(
                topLeft=self._bboxStart, 
                bottomRight=self.ConvertCoords(event.GetPosition())
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

        pnt = event.GetPosition()
        winpnt = self.ConvertCoords(pnt)
        
        # Move the selected node frame
        if event.LeftIsDown() == True and self._selectednodeframe != None:
            dpnt = pnt - self._lastpnt
            self._pdc.TranslateId(
                self._selectednodeframe.GetId(), 
                dpnt[0], dpnt[1]
                )
            r = self._pdc.GetIdBounds(self._selectednodeframe.GetId())
            self._lastpnt = pnt
            self._selectednodeframe.SetRect(r)
            self.RefreshGraph()
            

        if not event.LeftIsDown() or self._srcnode == None:
            return

        if self._srcnode.IsDisabled() != True:
            if self._srcplug == None:
                dpnt = pnt - self._lastpnt
                self._pdc.TranslateId(self._srcnode.GetId(), dpnt[0], dpnt[1])
                r = self._pdc.GetIdBounds(self._srcnode.GetId())
                self._lastpnt = pnt
                self._srcnode.SetRect(r)

                # Redraw the wires
                if self._srcnode.GetPlugs() != []:
                    for plug in self._srcnode.GetPlugs():
                        for wire in plug.GetWires(): 
                            pnt1 = wire.srcNode.GetRect().GetPosition() \ 
                            + wire.srcPlug.GetPosition()
                            pnt2 = wire.dstNode.GetRect().GetPosition() \ 
                            + wire.dstPlug.GetPosition()
                            self._DrawNodeWire(wire, pnt1, pnt2)

            elif self._tmpwire != None:
                # Set the wire to be active when it is being edited.
                self._tmpwire.SetActive(True)
                self._DrawNodeWire(self._tmpwire, pnt2=winpnt)

        # Refresh the nodegraph
        self.RefreshGraph()


    def OnLeftUp(self, event):
        # Attempt to make a connection
        if self._srcnode != None:
            pnt = event.GetPosition()
            winpnt = self.ConvertCoords(pnt)
            dstnode = self.NodeHitTest(winpnt)
            if dstnode != None:
                rect = self._pdc.GetIdBounds(self._srcnode.GetId())
                dstplug = dstnode.HitTest(
                    winpnt.x, winpnt.y, 
                    thumb_btn_active=True
                    )
                
                # Make sure not to allow the same datatype or 
                # 'plug type' of sockets to be connected! 
                if dstplug != None \
                    and self._srcplug.GetType() != dstplug.GetType() \
                    and self._srcnode.GetId() != dstnode.GetId() \
                    and self._srcplug.GetDataType() == dstplug.GetDataType():
                    
                    # Only allow a single node to be
                    # connected to any one socket.
                    if len(dstplug.GetWires()) < 1:
                        self._srcplug.Connect(dstplug)
                        
                    # If there is already a connection,
                    # but a wire is "dropped" into the plug
                    # disconnect the last connection and
                    # connect the current wire.
                    else:
                        wires = dstplug.GetWires()
                        dst = wires[0].dstPlug
                        src = wires[0].srcPlug
                        dst.Disconnect(src, render=False)
                        self._srcplug.Connect(dstplug)
 
        # We can erase the temp wire.
        if self._tmpwire != None:
            rect = self._pdc.GetIdBounds(self._tmpwire.GetId())
            self._pdc.RemoveId(self._tmpwire.GetId()) 

        # Clear selection bbox and set nodes as selected
        if self._bboxRect != None:
            self._pdc.RemoveId(ID_SELECTION_BBOX)
            self._selectednodes = self.BoxSelectHitTest(self._bboxRect)
            for node in self._selectednodes:
                if node.IsSelected() != True and node.IsActive() != True:
                    node.SetSelected(True)
                    node.Draw(self._pdc)
        
        # Reset all values 
        self._srcnode = None
        self._srcplug = None
        self._tmpwire = None
        self._bboxRect = None

        # Update the properties panel
        self._propertiesframe.UpdatePanelContents(self._activenode)

        # Refresh the nodegraph
        self.RefreshGraph()


    def OnMiddleDown(self, event): 
        winpnt = self.ConvertCoords(event.GetPosition())
        self._middlePnt = winpnt

        # Update mosue cursor
        self.SetCursor(wx.Cursor(wx.CURSOR_SIZING))


    def OnMiddleUp(self, event):
        # Reset mouse cursor
        self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))


    def ScrollNodeGraph(self, pos_x, pos_y):
        scrollpos_x = self.GetScrollPos(wx.HORIZONTAL)
        scrollpos_y = self.GetScrollPos(wx.VERTICAL)

        self.Scroll(scrollpos_x-pos_x,
                    scrollpos_y-pos_y
                    )
        self.RefreshGraph()
        
    def GetParent(self):
        return self._parent

    def GetMouseScrollValue(self):
        return self._zoomValue

    def SetMouseScrollValue(self, value):
        self._zoomValue = value

    def GetZoomFactor(self):
        return self._zoomFactor 

    def GetNodes(self):
        """ Returns a list of all the nodes in the current 
        graph. Used by the render engine to access the nodes. """
        return self._nodes

    def GetPDC(self):
        return self._pdc

    def GetSelectedNodes(self):
        return self._selectednodes

    def GetActiveNode(self):
        return self._activenode

    def GetNodePlug(self, node, plug):
        return node.GetPlug(plug)

    def ConvertCoords(self, pnt):
        xView, yView = self.GetViewStart()
        xDelta, yDelta = self.GetScrollPixelsPerUnit()
        return wx.Point(pnt[0] + (xView * xDelta), pnt[1] + (yView * yDelta))
        #print(self.GetZoomFactor())
        # return wx.Point(
        #     (pnt[0] + ((xView * xDelta)+ 1.0 +self.GetZoomFactor())) , 
        #     (pnt[1] + ((yView * yDelta)+ 1.0 + self.GetZoomFactor())))

    def OffsetRect(self, r):
        xView, yView = self.GetViewStart()
        xDelta, yDelta = self.GetScrollPixelsPerUnit()

    def RefreshGraph(self):
        """ Refreshes the nodegraph so that everything is redrawn. """
        rect = wx.Rect(0, 0, self._maxwidth, self._maxheight)
        self.OffsetRect(rect)
        self.RefreshRect(rect, False)
        self.Refresh()

    def OnDeleteNodes(self, event):
        self.DeleteNodes()
        self._parent.Render()

    def OnEnableDisableNode(self, event):
        if self._activenode.IsDisabled() == True:
            self._activenode.SetDisabled(False)
        else:
            self._activenode.SetDisabled(True)
        self._activenode.Draw(self._pdc)
        self.RefreshGraph()

    def OnSelectAllNodes(self, event):
        for nodeId in self._nodes:
            node = self._nodes[nodeId]
            if node.IsActive() == True:
                node.SetActive(False)
            node.SetSelected(True)
            node.Draw(self._pdc)
            self._selectednodes.append(node)
        self.RefreshGraph()

    def OnDeselectAllNodes(self, event):
        for nodeId in self._nodes:
            node = self._nodes[nodeId]
            node.SetSelected(False)
            node.Draw(self._pdc)
        self._selectednodes = []
        self.RefreshGraph()

    def OnDuplicateNode(self, event): 
        self.DuplicateNode(self._activenode)

    def DuplicateNode(self, node):
        pos = self.ConvertCoords(self.ScreenToClient(wx.GetMousePosition()))
        duplicate_node = CreateNode(self, node.GetName(), wx.ID_ANY, pos)
        nId = duplicate_node.GetId()

        # Assign the same properties to the duplicate
        duplicate_node._evalData["properties"] = node._evalData["properties"]

        if duplicate_node._category == 'INPUT':
            duplicate_node.SetThumbnailPreviewOpen(redraw=False)
        duplicate_node.Draw(self._pdc, False)
        self._pdc.SetIdBounds(nId, duplicate_node.GetRect())
        self._nodes[nId] = duplicate_node
        self.RefreshGraph()
        return duplicate_node
 
    def ResetToDefault(self):
        #for nodeId in self._nodes:
            #del self._nodes[nodeId]
            #self._nodes[nodeId].Delete(True)
        self._nodes = {}
        self._activenode = None
        self._selectednodes = []
        # Create the output node
        #self.AddNode('output', pos=wx.Point(600,300))
        self.GetPDC().RemoveAll()#Id(nodeId)
        self.RefreshGraph()

    def AddNode(self, _type, _id=wx.ID_ANY, pos=wx.Point(0, 0)):
        """ Adds a node of the given type to the nodegraph. """
        if _type != 'output':# or 'image':
            #pass
            pos = self.ConvertCoords(
                self.ScreenToClient(wx.GetMousePosition())
                )
        node = CreateNode(self, _type, _id, pos)
        nId = node.GetId()
        #print('ADDED-> ', nId)
        if node._category == 'INPUT':
            node.SetThumbnailPreviewOpen(redraw=False)
        node.Draw(self._pdc, False)
        self._pdc.SetIdBounds(nId, node.GetRect())
        self._nodes[nId] = node
        self.RefreshGraph()
        return node
 
    def AddNodeFromFile(self, _type, _id=wx.ID_ANY, pos=wx.Point(0, 0)):
        node = CreateNode(self, _type, _id, pos)
        nId = node.GetId()
        #print('ADDED NODE-> ', nId)
        if node._category == 'INPUT':
            node.SetThumbnailPreviewOpen(redraw=False)
        node.Draw(self._pdc, False)
        self._pdc.SetIdBounds(nId, node.GetRect())
        self._nodes[nId] = node

        self.RefreshGraph()
        return node

    def AddImageNodeFromDrop(self, filename):
        pos = self.ConvertCoords(self.ScreenToClient(wx.GetMousePosition()))
        node = CreateNode(self, 'corenode_image', wx.ID_ANY, pos)
        nId = node.GetId()
        node.SetThumbnailPreviewOpen(redraw=False)
        node.Draw(self._pdc, False)
        self._pdc.SetIdBounds(nId, node.GetRect())
        self._nodes[nId] = node
        node.EditProperties('Path', filename)
        self.RefreshGraph()

    def AddNodeFromNodeRegistryDrop(self, data):
        pos = self.ConvertCoords(self.ScreenToClient(wx.GetMousePosition()))
        node = CreateNode(self, data, wx.ID_ANY, pos)
        nId = node.GetId()
        node.Draw(self._pdc, False)
        self._pdc.SetIdBounds(nId, node.GetRect())
        self._nodes[nId] = node
        self.RefreshGraph()

    def DeleteNodes(self):
        for node in self._selectednodes:
            if node.IsCompositeNode() != True:
                node.Delete()
            else:
                # In the case that this is an output node, we 
                # want to deselect it, not delete it. :)
                node.SetSelected(False)
                node.Draw(self._pdc)
        self._selectednodes = []
        
        if self._activenode != None and \
           self._activenode.IsCompositeNode()!= True:
            self._activenode.Delete()
            self._activenode = None
        self.RefreshGraph()

    def OnAddNodeFrame(self, event):
        # Deselect node frame
        if self._selectednodeframe != None:
            self._selectednodeframe.SetSelected(False)
            self._selectednodeframe = None

        # Create and add a new frame
        ndfrm = NodeFrame()
        ndfrm.SetSelected(True)
        self._selectednodeframe = ndfrm
        self._nodeframes[ndfrm.GetId()] = ndfrm
        print('ADDED NODEFRM->', ndfrm.GetId())
        ndfrm.Draw(self.GetPDC())
        self.RefreshGraph()

    def OnDeleteNodeFrame(self, event):
        # Deselect node frame
        if self._selectednodeframe != None:
            self._selectednodeframe.SetSelected(False)

            del self._nodeframes[self._selectednodeframe.GetId()]
            self.GetPDC().RemoveId(self._selectednodeframe.GetId())
            self._selectednodeframe = None
        
        self.RefreshGraph()

    def UpdateAllNodes(self):
        for nodeId in self.GetNodes():
            self._nodes[nodeId].Draw(self.GetPDC(), False)
        self.RefreshGraph()

    def NodeFrameHitTest(self, pt):
        idxs = self._pdc.FindObjects(pt[0], pt[1], 5)
        hits = [
            idx 
            for idx in idxs
            if idx in self._nodeframes
        ]
        if hits != []:
            return self._nodeframes[hits[0]]
        else:
            # Make sure we deselect everything
            for node in self._selectednodes:
                node.SetSelected(False)
                node.Draw(self._pdc)
            self._selectednodes = []

            if self._activenode != None:
                self._activenode.SetActive(False)
                self._activenode.Draw(self._pdc)
                self._activenode = None

            if self._selectednodeframe != None:
                self._selectednodeframe.SetSelected(False)
                self._selectednodeframe.Draw(self._pdc)
                self._selectednodeframe = None
            return None

    def NodeHitTest(self, pt):
        idxs = self._pdc.FindObjects(pt[0], pt[1], 5)
        hits = [
            idx 
            for idx in idxs
            if idx in self._nodes
        ]
        if hits != []:
            return self._nodes[hits[0]]
        else:
            # Make sure we deselect everything
            for node in self._selectednodes:
                node.SetSelected(False)
                node.Draw(self._pdc)
            self._selectednodes = []

            if self._activenode != None:
                self._activenode.SetActive(False)
                self._activenode.Draw(self._pdc)
                self._activenode = None
            #self.RefreshGraph()
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
            for node in self._selectednodes:
                node.SetSelected(False)
                node.Draw(self._pdc)
            self._selectednodes = []
            return []


    def _DrawGridBackground(self, dc, rect):
        dc.SetBrush(wx.Brush(wx.Colour('#373737'), wx.CROSS_HATCH))
        dc.DrawRectangle(rect)

    def _DrawNodeWire(self, wire, pnt1=None, pnt2=None):
        if pnt1 != None:
            wire.SetPoint1(pnt1)
        if pnt2 != None:
            wire.SetPoint2(pnt2)
        wire.Draw(self._pdc)

