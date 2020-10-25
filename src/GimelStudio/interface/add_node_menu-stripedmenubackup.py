## ----------------------------------------------------------------------------
## Gimel Studio Copyright 2019-2020 by Noah Rahm and contributors
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
## FILE: add_node_menu.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the Add Node menu popup
## ----------------------------------------------------------------------------

import copy

import wx
import wx.adv

from GimelStudio.datafiles.icons import *


class NodeRegistryItem(object):
    def __init__(
        self, parent, rect, name, label, version, author,
        category, desc
        ):
        self._parent = parent
        self._rect = rect
        self._name = name
        self._label = label
        self._version = version
        self._author = author
        self._category = category
        self._desc = desc
        self._id = wx.NewIdRef().GetValue()
        self._isCoreNode = False
        self._isSelected = False
        self._isHover = False
        self._dragndropData = wx.TextDataObject(self._name)

    def GetParent(self):
        return self._parent

    def GetId(self):
        return self._id

    def GetRect(self):
        return self._rect

    def SetRect(self, rect):
        self._rect = rect

    def GetName(self):
        return self._name

    def GetLabel(self):
        return self._label

    def GetColor(self):
        # if self._category in STYLE_NODES_COLOR_DICT.keys():
        #     return STYLE_NODES_COLOR_DICT[self._category]
        # else:
        #     return STYLE_NODES_COLOR_DICT["DEFAULT"]
        return "#ccc"

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

    def Draw(self, dc):
        dc.ClearId(self.GetId())
        dc.SetId(self.GetId())
        x, y, w, h = self.GetRect()

        sys_scrollbar_x = wx.SystemSettings.GetMetric(
            getattr(wx, 'SYS_VSCROLL_X')
            )

        if self.IsSelected() == True:
            dc.SetPen(wx.Pen(wx.Colour('#80b3ffff'), 4))

            # Draw Background
            dc.SetBrush(wx.Brush(wx.Colour('white'), wx.SOLID))
            dc.DrawRectangle(x, y, w-sys_scrollbar_x, h)

        elif self.IsSelected() == False:
            dc.SetPen(wx.Pen('black', 1))

            # Draw Background
            if self.GetHover() == True:
                dc.SetBrush(wx.Brush(wx.Colour('white'), wx.SOLID))
                dc.DrawRectangle(x, y, w-sys_scrollbar_x, h)
            else:
                dc.SetBrush(wx.Brush(wx.Colour('#ECECEC'), wx.SOLID))
                dc.DrawRectangle(x, y, w-sys_scrollbar_x, h)

        # Draw Colored Heading Background
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 0, 0), 1))
        dc.SetBrush(wx.Brush(wx.Colour(self.GetColor()), wx.SOLID))
        dc.DrawRectangle(x, y, w-sys_scrollbar_x, h-56)

        # Draw Node Label Text
        dc.SetTextForeground(wx.Colour('white'))
        #dc.SetFont(self.GetParent().GetParent().GetFont().MakeSmaller())
        dc.DrawText(self.GetLabel(), x+28, y+2)

        # Draw Icon
        # dc.DrawBitmap(
        #     self.GetIcon(), x+6, y+2, True)

        # Draw Version and Author Text
        dc.SetTextForeground(wx.Colour('#ECECEC'))

        # if self.GetIsCoreNode() != True:
        #     # TODO add icon for custom nodes
        #     #print("CUSTOM NODE")
        #     pass
        # else:
        #     dc.DrawBitmap(
        #         ICON_GIMELSTUDIO_LOGO.GetBitmap(),
        #         x+w-sys_scrollbar_x-24,
        #         y+2,
        #         True
        #         )
        dc.DrawText('v{}'.format(
            self.GetVersion()), 
            x+w-sys_scrollbar_x-70, 
            y+2
            )

        # Draw Description Text
        dc.SetTextForeground(wx.Colour('black'))

        if self.GetIsDepreciated() == True:
            is_depreciated_msg = "\nTHIS NODE WILL BE REMOVED IN A FUTURE RELEASE."
            dc.DrawText(self.GetDescription() + is_depreciated_msg, x+6, y+28)
        else:
            dc.DrawText(self.GetDescription(), x+6, y+28)












class MyVListBox(wx.VListBox):
    def __init__(self, *args, **kw):
        self.parent = args[0]
        wx.VListBox.__init__(self, *args, **kw)

        self.SetBackgroundColour(wx.Colour("#6D6F6E"))

    @property
    def NodeRegistryMap(self):
        return self.parent.nodeRegistryMapping

    @property
    def NodeRegistry(self):
        return self.parent.nodeRegistry

    # This method must be overridden.  When called it should draw the
    # n'th item on the dc within the rect.  How it is drawn, and what
    # is drawn is entirely up to you.
    def OnDrawItem(self, dc, rect, n):
        # Monkey-patch some padding for the left side
        rect[0] += 6

        if self.GetSelection() == n:
            c = wx.Colour("#000")
            bmp = ICON_GIMELSTUDIO_LOGO.GetImage().AdjustChannels(0, 0, 0, 1).ConvertToBitmap()
        else:
            c = wx.Colour("#fff")
            bmp = ICON_GIMELSTUDIO_LOGO.GetBitmap()
        dc.SetFont(self.GetFont())
        dc.SetTextForeground(c)
        dc.SetBrush(wx.Brush(c, wx.SOLID))
        dc.DrawLabel(text=self._getItemText(n), bitmap=bmp, rect=rect,
                     alignment=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)

    # This method must be overridden.  It should return the height
    # required to draw the n'th item.
    def OnMeasureItem(self, n):
        height = 0 
        for line in self._getItemText(n).split('\n'):
            w, h = self.GetTextExtent(line)
            height += h
        return height + 10


    def OnDrawBackground(self, dc, rect, n):
        #   Draw the background and maybe a border if desired.
        if self.GetSelection() == n:
            c = wx.Colour("#fff")
        else:
            if n % 2 == 0:
                c = wx.Colour("#6D6F6E")
            else:
                c = wx.Colour("#838383")
                
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.Brush(c, wx.SOLID))
        dc.DrawRectangle(rect)




    def _getItemText(self, item):

        return self.NodeRegistry[self.NodeRegistryMap[item]].GetLabel()


    def UpdateForSearch(self, search_string):
        search_string = search_string.lower()

        self.parent.nodeRegistryMapping = {} 
        i = 0
        for item in self.NodeRegistry:
            if item != "corenode_outputcomposite":
                #print(self.NodeRegistry[item].GetLabel(), "<<<<<<<node")
                if self.NodeRegistry[item].GetLabel().lower().startswith(search_string):
                    self.NodeRegistryMap[i] = item
                    i += 1

        size = len(self.NodeRegistryMap)
        self.SetItemCount(size)

        if size > 0:
            self.SetSelection(-1)

        #print(self.NodeRegistryMap, "map")

        self.Refresh()
        #self.Update()










class AddNodeMenu(wx.PopupTransientWindow): 
    def __init__(self, parent, node_registry, size, style=wx.BORDER_NONE):
        wx.PopupTransientWindow.__init__(self, parent, style)

        self.nodeRegistry = node_registry
        self._parent = parent


        self.nodeRegistryMapping = {}

        i = 0
        for item in self.nodeRegistry:
            if item != "corenode_outputcomposite":
                self.nodeRegistryMapping[i] = item
                i += 1

        #print(self.nodeRegistryMapping)

        vlbSizer = wx.BoxSizer(wx.VERTICAL)

        header_lbl = wx.StaticText(self, wx.ID_ANY, "Add Node")

        vlbSizer.Add(header_lbl,  flag=wx.EXPAND|wx.ALL, border=5) 

        # Search bar
        self.search_bar = wx.SearchCtrl(self, style=wx.TE_PROCESS_ENTER)
        if 'gtk3' in wx.PlatformInfo:
            # Something is wrong with the bestsize of the SearchCtrl, so for now
            # let's set it based on the size of a TextCtrl.
            txt = wx.TextCtrl(self)
            bs = txt.GetBestSize()
            txt.DestroyLater()
            self.search_bar.SetMinSize((200, bs.height+4))
        self.search_bar.SetFocus()

        vlbSizer.Add(self.search_bar, flag=wx.EXPAND|wx.ALL, border=5)

        # Nodes list box
        self.nodes_listbox = MyVListBox(self, size=size, style=wx.BORDER_NONE)
        self.nodes_listbox.SetItemCount(len(self.nodeRegistryMapping))
        #self.nodes_listbox.SetSelection(0)
        #nodes_listbox.SetFocus()

        

        vlbSizer.Add(self.nodes_listbox, flag=wx.EXPAND|wx.ALL, border=5)


        self.SetSizer(vlbSizer)




        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnDoSearch, self.search_bar)
        #self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnCancel, self.search)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnDoSearch, self.search_bar)
        self.Bind(wx.EVT_TEXT, self.OnDoSearch, self.search_bar)

        self.Bind(wx.EVT_LISTBOX, self.OnSelectItem, self.nodes_listbox)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnSelectItem, self.nodes_listbox)
        



    def OnDoSearch(self, event): 
        print(event.GetString())
        self.nodes_listbox.UpdateForSearch(event.GetString())

    def OnSelectItem(self, event):
        print(self.nodeRegistryMapping[event.GetInt()], "<-SEL")

        sel = self.nodeRegistryMapping[event.GetInt()]
        print(sel) 

        coords = self._parent.ConvertCoords(wx.Point(
            self._parent.Size[0]/2, 
            self._parent.Size[1]/2, 
            ))

        node = self._parent.AddNode(sel, pos=coords)

        self._parent.RefreshGraph()

 


    # def OnLeftDown(self, event):
    #     pnt = event.GetPosition()
    #     winpnt = self.ConvertCoords(pnt)
    #     self._nodeitem = self.HitTest(winpnt)

    #     if self._nodeitem != None:
    #         # Handle node selection
    #         if self._selectednodeitem == None:
    #             self._selectednodeitem = self._nodeitem
    #             self._selectednodeitem.SetSelected(True)
    #             self._selectednodeitem.Draw(self._pdc)

    #         else:
    #             if self._nodeitem.GetId() != self._selectednodeitem.GetId():
    #                 self._selectednodeitem.SetSelected(False)
    #                 self._selectednodeitem.Draw(self._pdc)
    #                 self._selectednodeitem = self._nodeitem
    #                 self._selectednodeitem.SetSelected(True)
    #                 self._selectednodeitem.Draw(self._pdc)

    #         # Handle dnd node items to Node Graph
    #         dragSource = wx.DropSource(self)
    #         dragSource.SetData(self._selectednodeitem.GetDragNDropInfo())
    #         result = dragSource.DoDragDrop(True)

    #         self.RefreshPanel()


    # def OnMotion(self, event):
    #     # Hover for items
    #     pnt = event.GetPosition()
    #     winpnt = self.ConvertCoords(pnt)
    #     for i in self._ndregistryitems:
    #         btn_region = wx.Region(self._ndregistryitems[i].GetRect())
    #         if btn_region.Contains(winpnt[0], winpnt[1]):
    #             self._ndregistryitems[i].SetHover(True)
    #         else:
    #             self._ndregistryitems[i].SetHover(False)
    #         self._ndregistryitems[i].Draw(self._pdc)
    #     self.RefreshPanel()

    # def InitNodeItems(self):
    #     print(">>>>", self._noderegistry)
    #     for nodedefId in self._noderegistry:
    #         nitem = self._noderegistry[nodedefId]("corenode_mix")
    #         print("NN", nitem)
    #         print(self._noderegistry[nodedefId])
    #         # Exclude the ouput composite node
    #         #if self._noderegistry[nodedefId].IsOutputNode() != True:
    #         noderegistryitem = NodeRegistryItem(
    #             self,
    #             wx.Rect(0, 0, self.Size[0], self.ITEMHEIGHT),
    #             nitem.GetType(), 
    #             nitem.GetLabel(),
    #             "0.5.0",
    #             "test",
    #             "INPUT",
    #             "this is a desc",
    #             )

    #         # Check to see if this is a core node
    #         if str(nitem._name).startswith("corenode_"):
    #             noderegistryitem.SetIsCoreNode(True)
    #         else:
    #             noderegistryitem.SetIsCoreNode(False)

    #         self._ndregistryitems[noderegistryitem.GetId()] = noderegistryitem

    # def DrawNodeItems(self):
    #     y = 0
    #     for nritem in self._ndregistryitems:
    #         self._ndregistryitems[nritem].SetRect(
    #             wx.Rect(0, y, self.Size[0], self.ITEMHEIGHT)
    #             )
    #         self._ndregistryitems[nritem].Draw(self._pdc)
    #         self._pdc.SetIdBounds(
    #             self._ndregistryitems[nritem].GetId(),
    #             self._ndregistryitems[nritem].GetRect()
    #             )
    #         y += self.ITEMHEIGHT + 8

    # def GetSelectedItem(self):
    #     if self._selectednodeitem == None:
    #         return None
    #     else:
    #         return self._selectednodeitem.GetName()


    # def HitTest(self, pt):
    #     idxs = self._pdc.FindObjects(pt[0], pt[1], 25)
    #     hits = [
    #         idx
    #         for idx in idxs
    #         if idx in self._ndregistryitems
    #     ]

    #     if hits != []:
    #         return self._ndregistryitems[hits[0]]
    #     else:
    #         if self._selectednodeitem != None:
    #             self._selectednodeitem.SetSelected(False)
    #             self._selectednodeitem.Draw(self._pdc)

    #             self.RefreshPanel()
    #             self._selectednodeitem = None
    #         return None


    # def ConvertCoords(self, pnt):
    #     xView, yView = self.GetViewStart()
    #     xDelta, yDelta = self.GetScrollPixelsPerUnit()
    #     return wx.Point(pnt[0] + (xView * xDelta), pnt[1] + (yView * yDelta))

    # def OffsetRect(self, r):
    #     xView, yView = self.GetViewStart()
    #     xDelta, yDelta = self.GetScrollPixelsPerUnit()

    # def RefreshPanel(self):
    #     """ Refreshes the panel so that everything is redrawn. """
    #     rect = wx.Rect(0, 0, self.Size[0], self.Size[1])
    #     self.OffsetRect(rect)
    #     self.RefreshRect(rect, False)