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
## FILE: add_node_menu.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the Add Node menu popup
## ----------------------------------------------------------------------------

import copy

import wx
import wx.adv

from GimelStudio.datafiles.icons import *


class NodesVListBox(wx.VListBox):
    def __init__(self, *args, **kw):
        self._parent = args[0]
        wx.VListBox.__init__(self, *args, **kw)

        self.SetBackgroundColour(wx.Colour("#6D6F6E"))

        self.Bind(wx.EVT_MOTION, self.OnStartDrag)

    def _GetItemColor(self, item):
        return self.GetNodeObject(item).Model.GetNodeHeaderColor()

    def _GetItemText(self, item):
        return self.GetNodeObject(item).GetLabel()

    def _GetItemVersion(self, item):
        return self.GetNodeObject(item).GetVersionString()

    def GetNodeObject(self, node_type):
        return self.NodeRegistry[self.NodeRegistryMap[node_type]]

    @property
    def NodeRegistryMap(self):
        return self._parent._nodeRegistryMapping

    @property
    def NodeRegistry(self):
        return self._parent._nodeRegistry

    def OnStartDrag(self, event):
        """ Start of drag n drop event handler. """
        if event.Dragging():
            selection = self.NodeRegistryMap[self.GetSelection()]
            data = wx.TextDataObject()
            data.SetText(selection)

            dropSource = wx.DropSource(self)
            dropSource.SetData(data)
            result = dropSource.DoDragDrop()

            # Reset the focus back to the search input so that
            # after a user dnd a node, they can search again straight-away.
            if result:
                self._parent.search_bar.SetFocus()
                self.SetSelection(-1)

    # This method must be overridden.  When called it should draw the
    # n'th item on the dc within the rect.  How it is drawn, and what
    # is drawn is entirely up to you.
    def OnDrawItem(self, dc, rect, n):
        """ Draws the item itself. """
        # Monkey-patch some padding for the left side
        rect[0] += 6

        # Draw item with node label
        if self.GetSelection() == n:
            color = wx.Colour("#fff")
            bmp = ICON_GIMELSTUDIO_LOGO.GetBitmap()#.GetImage().AdjustChannels(0, 0, 0, 1).ConvertToBitmap()
        else:
            color = wx.Colour("#fff")
            bmp = ICON_GIMELSTUDIO_LOGO.GetBitmap()
        dc.SetFont(self.GetFont())
        dc.SetTextForeground(color)
        dc.SetBrush(wx.Brush(color, wx.SOLID))
        dc.DrawLabel(text=self._GetItemText(n), bitmap=bmp, rect=rect,
                     alignment=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)

        # Monkey-patch some padding for the right side
        rect[2] -= 18

        # Draw version label
        dc.DrawLabel(text=self._GetItemVersion(n), rect=rect,
                     alignment=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)


    def OnMeasureItem(self, n):
        """ Returns the height required to draw the n'th item. """
        height = 0
        for line in self._GetItemText(n).split('\n'):
            w, h = self.GetTextExtent(line)
            height += h
        return height + 20


    def OnDrawBackground(self, dc, rect, n):
        """ Draws the item background. """
        if self.GetSelection() == n:
            color  = wx.Colour(self._GetItemColor(n))
        else:
            # Create striped effect
            if n % 2 == 0:
                color = wx.Colour("#6D6F6E")
            else:
                color = wx.Colour("#838383")

        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.Brush(color, wx.SOLID))
        dc.DrawRectangle(rect)


    def SearchNodeRegistry(self, node_label, search_string):
        """ Returns whether or not the search string is in
        the label text or not.
        """
        label = node_label.lower()
        if search_string in label:
            return True
        else:
            return False

    def UpdateForSearch(self, search_string):
        """ Updates the listbox based on the search string. """
        # Reset mapping var
        self._parent._nodeRegistryMapping = {}

        i = 0
        for item in self.NodeRegistry:
            if item != "corenode_outputcomposite":
                lbl = self.NodeRegistry[item].GetLabel()
                if self.SearchNodeRegistry(lbl, search_string.lower()):
                    self.NodeRegistryMap[i] = item
                    i += 1

        # Deal with selection and update size
        size = len(self.NodeRegistryMap)
        if size == 1:
            self.SetSelection(0)
        else:
            self.SetSelection(-1)
        self.SetItemCount(size)

        # Refresh the window
        self.Refresh()



class AddNodeMenu(wx.PopupTransientWindow):
    def __init__(self, parent, node_registry, size, style=wx.BORDER_NONE):
        wx.PopupTransientWindow.__init__(self, parent, style)

        self._parent = parent
        self._size = size
        self._nodeRegistry = node_registry
        self._nodeRegistryMapping = {}

        self.SetBackgroundColour(wx.Colour("#6D6F6E"))

        self._InitRegistryMapping()
        self._InitAddNodeMenuUI()

    def _InitRegistryMapping(self):
        i = 0
        for item in self._nodeRegistry:
            if item != "corenode_outputcomposite":
                self._nodeRegistryMapping[i] = item
                i += 1

    def _InitAddNodeMenuUI(self):
        # Sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Label
        main_sizer.AddSpacer(5)
        header_lbl = wx.StaticText(self, wx.ID_ANY, "Add Node from Registry")
        header_lbl.SetForegroundColour(wx.Colour("#fff"))
        #header_lbl.SetFont(self.GetFont().MakeBold())
        main_sizer.Add(header_lbl,  flag=wx.EXPAND|wx.ALL, border=5)
        main_sizer.AddSpacer(5)

        # Search bar
        self.search_bar = wx.SearchCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.search_bar.SetFocus()
        # FIXME
        if 'gtk3' in wx.PlatformInfo:
            # Something is wrong with the bestsize of the SearchCtrl, so for now
            # let's set it based on the size of a TextCtrl.
            txt = wx.TextCtrl(self)
            bs = txt.GetBestSize()
            txt.DestroyLater()
            self.search_bar.SetMinSize((200, bs.height+4))
        main_sizer.Add(self.search_bar, flag=wx.EXPAND|wx.ALL, border=5)
        main_sizer.AddSpacer(5)

        # Nodes list box
        self.nodes_listbox = NodesVListBox(
            self,
            size=self._size,
            style=wx.BORDER_SIMPLE
            )
        self.nodes_listbox.SetItemCount(
            len(self._nodeRegistryMapping)
            )
        #nodes_listbox.SetFocus()
        main_sizer.Add(self.nodes_listbox, flag=wx.EXPAND|wx.ALL, border=5)

        self.SetSizer(main_sizer)

        # Bindings
        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnDoSearch, self.search_bar)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnDoSearch, self.search_bar)
        self.Bind(wx.EVT_TEXT, self.OnDoSearch, self.search_bar)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnDClickSelectItem, self.nodes_listbox)
        self.Bind(wx.EVT_LISTBOX, self.OnClickSelectItem, self.nodes_listbox)

    @property
    def NodeGraph(self):
        """ Get the Node Graph. """
        return self._parent

    def OnDoSearch(self, event):
        """ Event handler for when something is typed into the search bar, etc. """
        self.nodes_listbox.UpdateForSearch(event.GetString())

    def OnDClickSelectItem(self, event):
        """ Event handler for a double-click listbox selection.
        This also Adds the selected node to Node Graph.
        """
        sel = self._nodeRegistryMapping[event.GetInt()]
        coords = self.NodeGraph.ConvertCoords(
            wx.Point(self.NodeGraph.Size[0]/2, self.NodeGraph.Size[1]/2)
            )

        self.NodeGraph.AddNode(sel, pos=coords)
        self.NodeGraph.RefreshGraph()

    def OnClickSelectItem(self, event):
        """ Event handler for a single click listbox selection.
        This merely updates the statusbar text.
        """
        sel = self._nodeRegistryMapping[event.GetInt()]
        desc = self._nodeRegistry[sel].GetDescription()
        lbl = self._nodeRegistry[sel].GetLabel()
        self.NodeGraph.GetParent().SetStatusText("{}: {}".format(lbl, desc))
