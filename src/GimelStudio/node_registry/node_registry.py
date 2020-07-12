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
## FILE: node_registry.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the Node Registry panel
## ----------------------------------------------------------------------------

import wx
import wx.adv

import wx.lib.buttons  as  buttons

from .node_registry_base import _NodeRegistryBase, NodeRegistryBase
from GimelStudio.stylesheet import STYLE_NODES_COLOR_DICT
from GimelStudio.datafiles.icons import *

# DICT = {}
# Nodes get registered on startup 
# DICT is passed into NodeRegistry


ITEM_HEIGHT = 120



class NodeRegistryItem(wx.Control):
    """A Node Registry item
    """
    def __init__(self, parent, node, _id, pos=(0, 0), size=wx.Size(125, 120)):
        """Creates a new colour box instance and initializes the colour
        content."""
        wx.Control.__init__(self, parent, wx.ID_ANY, pos=pos, size=size, style=wx.NO_BORDER)
 
        self._parent = parent
        self._rect = size
        self._icon = "image"
        self._name = node._IDName
        self._label = node.NodeLabel
        self._version = node.NodeVersion
        self._author = node.NodeAuthor
        self._category = node.NodeCategory
        self._desc = node.NodeDescription
        #self._isDepreciated = is_depreciated
        self._id = _id#.GetValue()
        self._isCoreNode = False
        self._isSelected = False
        self._isHover = False
        self._dragndropData = wx.TextDataObject(node._IDName)


        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: None)


    def OnPaint(self, event):
        dc = wx.PaintDC(self)

        # Use PrepareDC to set position correctly.
        #self.PrepareDC(dc)

        # We need to clear the dc BEFORE calling PrepareDC.
        dc.SetBackground(wx.Brush(wx.Colour('grey')))
        dc.Clear()

        (width, height) = self.GetClientSize()
        x1 = y1 = 0
        x2 = width-1
        y2 = height-1

        self.DrawItem(dc)



    def GetName(self):
        return self._name

    def GetLabel(self):
        return self._label

    def GetColor(self):
        #print(self._category, "<<---")
        if self._category in STYLE_NODES_COLOR_DICT.keys():
            return STYLE_NODES_COLOR_DICT[self._category]
        else:
            return STYLE_NODES_COLOR_DICT["DEFAULT"]

    def GetIcon(self):
        if self._icon == "image":
            return ICON_NODE_IMAGE_LIGHT.GetBitmap()

    def GetVersion(self):
        return self._version

    def GetAuthor(self):
        return self._author

    def GetDescription(self):
        return self._desc

    def GetIsDepreciated(self):
        return self._isDepreciated

    def GetIsCoreNode(self):
        return self._isCoreNode

    def SetIsCoreNode(self, is_corenode):
        self._isCoreNode = is_corenode

    def IsSelected(self):
        return self._isSelected

    def SetSelected(self, is_selected):
        self._isSelected = is_selected

    def SetHover(self, ishover):
        self._isHover = ishover

    def GetHover(self):
        return self._isHover

    def GetDragNDropInfo(self):
        return self._dragndropData

    def GetId(self):
        return self._id


    def DrawItem(self, dc):

        x, y, w, h = self.GetRect()

        #print(self.GetId(), x, y, w, h, "fknfkfnfknkn")

        #dc.SetIdBounds(self.GetId(), self.GetRect())

        sys_scrollbar_x = wx.SystemSettings.GetMetric(
            getattr(wx, 'SYS_VSCROLL_X')
            )

        # if self.IsSelected() == True:
        #     dc.SetPen(wx.Pen(wx.Colour('#80b3ffff'), 4))

        #     # Draw Background
        #     dc.SetBrush(wx.Brush(wx.Colour('white'), wx.SOLID))
        #     dc.DrawRectangle(x, y, w-sys_scrollbar_x, h)

        # elif self.IsSelected() == False:
        #     dc.SetPen(wx.Pen('black', 1))

        #     # Draw Background
        #     if self.GetHover() == True:
        #         dc.SetBrush(wx.Brush(wx.Colour('white'), wx.SOLID))
        #         dc.DrawRectangle(x, y, w-sys_scrollbar_x, h)
        #     else:
        #         dc.SetBrush(wx.Brush(wx.Colour('#ECECEC'), wx.SOLID))
        #         dc.DrawRectangle(x, y, w-sys_scrollbar_x, h)

        # Draw Colored Heading Background
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 0, 0), 1))
        dc.SetBrush(wx.Brush(wx.Colour(self.GetColor()), wx.SOLID))
        dc.DrawRectangle(x, y, w-sys_scrollbar_x, h-56)

        # Draw Node Label Text
        dc.SetTextForeground(wx.Colour('white'))
        #dc.SetFont(self.GetParent().GetParent().GetFont().MakeSmaller())
        dc.DrawText(self.GetLabel(), 28, 2)


       # Draw Icon
        dc.DrawBitmap(
            self.GetIcon(), 6, 2, True)

        # Draw Version and Author Text
        dc.SetTextForeground(wx.Colour('#ECECEC'))

        if self.GetIsCoreNode() != True:
            # TODO add icon for custom nodes
            print("CUSTOM NODE")
            pass
        else:
            dc.DrawBitmap(
                ICON_GIMELSTUDIO_LOGO.GetBitmap(),
                24,
                2,
                True
                )
        dc.DrawText('v{}'.format(
            self.GetVersion()), 
            w-sys_scrollbar_x-70, 
            2
            )
        self.Refresh()


 
# class NodeRegistry(wx.Panel, NodeRegistryBase):
#     def __init__(self, parent, size=wx.DefaultSize):
#         wx.Panel.__init__(self, parent)

class NodeRegistry(NodeRegistryBase):
    def __init__(self, parent, size=wx.DefaultSize):

        self._parent = parent
        self._registeredNodes = {}
        #self.ndict = {}
        self._registryBase = _NodeRegistryBase

        # self._selectednodeitem = None
        # self._ndregistryitems = {}
        # self.ITEMHEIGHT = 80
        # self._maxheight = (
        #     (len(noderegistry) + 2) * self.ITEMHEIGHT
        #     ) - self.ITEMHEIGHT

        # Create a PseudoDC to record our drawing
        #dc = wx.adv.PseudoDC()

        #self.InitNodeItems()
        #self.DrawNodeItems()

        self._InitNodes()

        #self.Bind(wx.EVT_SIZE, self.OnSize)


        # self.colour_boxs = [ ]
        # colour_grid = wx.BoxSizer(wx.VERTICAL)

        # i = 0
        # for nodeName in self.GetAvailableNodes():

        #         #print(self.GetAvailableNodes()[nodeName]())

        #         nr_item = buttons.GenButton(self, -1, self.GetAvailableNodes()[nodeName]().NodeLabel)

                
        #         # nr_item = NodeRegistryItem(self, 
        #         # self._registeredNodes[nodeName](), 
        #         # _id=wx.NewIdRef(),
        #         # #pos=wx.Point(0, i),
        #         # size=wx.Size(self.Size[1], ITEM_HEIGHT)
        #         # )
        #         # #box.Draw()
        #         # #box.Bind(wx.EVT_LEFT_DOWN, lambda x, b=box: self.onBasicClick(x, b))

        #         # # Check to see if this is a core node
        #         # if str(nodeName).startswith("corenode_"):
        #         #     nr_item.SetIsCoreNode(True)
        #         # else:
        #         #     nr_item.SetIsCoreNode(False)

        #         self.colour_boxs.append(nr_item)
        #         colour_grid.Add(nr_item, 0, wx.EXPAND)

        #         i =+ ITEM_HEIGHT + 8


        # csizer = wx.BoxSizer(wx.VERTICAL)

        # csizer.Add(colour_grid, 0, wx.EXPAND)

        # self.SetSizer(csizer)

        


    def OnSize(self, event):
        i = 0
        for n in self.colour_boxs:
            n.SetSize(self.Size[0], ITEM_HEIGHT)
            n.SetPosition(wx.Point(0, i))
            #print(n.GetRect(), n.GetName(), "s")

            #n.Draw()
            i =+ ITEM_HEIGHT
        self.Refresh()


    def _InitNodes(self):
        self._registeredNodes = self._registryBase.GetRegisteredNodes()

    def GetRegisteredNodes(self):
        """ Returns all the registered nodes, including the composite node. """
        return self._registeredNodes

    def GetAvailableNodes(self):
        """ Returns all the registered nodes, except for the composite node. """
        nodes = {}
        for node_name in self.GetRegisteredNodes():
            if node_name != 'gimelstudiocorenode_outputcomposite':
                nodes[node_name] = self._registeredNodes[node_name]
        return nodes


    def onBasicClick(self, event, box):
        """Highlights the selected colour box and updates the solid colour
        display and colour slider to reflect the choice."""
        if hasattr(self, '_old_custom_highlight'):
            self._old_custom_highlight.SetHighlight(False)
        if hasattr(self, '_old_colour_highlight'):
            self._old_colour_highlight.SetHighlight(False)
        box.SetHighlight(True)
        self._old_colour_highlight = box


        # Handle dnd node items to Node Graph
        dragSource = wx.DropSource(self)
        dragSource.SetData(box.GetDragNDropInfo())
        result = dragSource.DoDragDrop(True)

 
        #self.UpdateColour(box.GetColour())


    # def OnPaint(self, event):
    #     dc = wx.BufferedPaintDC(self)
    #     dc = wx.GCDC(dc)

    #     # We need to clear the dc BEFORE calling PrepareDC.
    #     dc.SetBackground(wx.Brush(wx.Colour('#ECECEC')))
    #     dc.Clear()

    #     # Draw to the dc using the calculated clipping rect.
    #     dc.DrawToDCClipped(
    #         dc, wx.Rect(0, 0, self.Size[0], self.Size[1])
    #         )


    def GetParent(self):
        return self._parent

    def GetRegistryBase(self):
        return self._registryBase