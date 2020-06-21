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

from .node_registry_base import _NodeRegistryBase, NodeRegistryBase
from GimelStudio.stylesheet import STYLE_NODES_COLOR_DICT
from GimelStudio.datafiles.icons import *

# DICT = {}
# Nodes get registered on startup 
# DICT is passed into NodeRegistry

class NodeRegistry(wx.Panel, NodeRegistryBase):
    def __init__(self, parent, size=wx.DefaultSize):
        wx.Panel.__init__(self, parent, size=size)

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
        self._pdc = wx.adv.PseudoDC()

        #self.InitNodeItems()
        #self.DrawNodeItems()

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: None)


    def _InitNodes(self):
        self._registeredNodes = self._registryBase.GetRegisteredNodes()


    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        dc = wx.GCDC(dc)

        # We need to clear the dc BEFORE calling PrepareDC.
        dc.SetBackground(wx.Brush(wx.Colour('#ECECEC')))
        dc.Clear()

        # Draw to the dc using the calculated clipping rect.
        self._pdc.DrawToDCClipped(
            dc, wx.Rect(0, 0, self.Size[0], self.Size[1])
            )


    def GetParent(self):
        return self._parent

    def GetRegistryBase(self):
        return self._registryBase






    def RefreshPanel(self):
        """ Refreshes the panel so that everything is redrawn. """
        rect = wx.Rect(0, 0, self.Size[0], self.Size[1])
        self.RefreshRect(rect, False)

