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
## FILE: node_property_panel.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the Node Property panel
## ----------------------------------------------------------------------------

import wx

from GimelStudio.datafiles.icons import *


class NodePropertyPanel(wx.Panel):
    def __init__(self, parent, size=wx.DefaultSize):
        wx.Panel.__init__(self, parent, wx.ID_ANY, size=size)

        self._parent = parent
        self._selectedNode = None

        self._mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.SetSizer(self._mainSizer)
        self._mainSizer.Fit(self)
        
    @property
    def Parent(self):
        return self._parent

    @property
    def AUIManager(self):
        return self._parent._mgr

    def UpdatePanelContents(self, selected_node):
        self._mainSizer.Clear(delete_windows=True)
 
        if selected_node != None:

            panel_staticbox = wx.StaticBox(self, wx.ID_ANY, selected_node.GetLabel())

            # This gets the recommended amount of border space to use for items
            # within in the static box for the current platform.
            top_bd, other_bd = panel_staticbox.GetBordersForSizer()
            staticbox_sizer = wx.BoxSizer(wx.VERTICAL)
            #staticbox_sizer.AddSpacer(top_bd)

            # t1 = wx.StaticText(panel_staticbox, -1, "As of wxPython 2.9, wx.StaticBox can now be used as a parent like most other wx widgets. This is now the recommended way of using wx.StaticBox.")
            # staticbox_sizer.Add(t1, 1, wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT, other_bd+10)
            
            panel_staticbox.SetSizer(staticbox_sizer)

            panel_sizer = wx.BoxSizer(wx.VERTICAL)
            panel_sizer.Add(panel_staticbox, 1, wx.EXPAND|wx.ALL, 25)


            # Node Properties UI
            selected_node.PropertiesUI(selected_node, panel_staticbox, staticbox_sizer)

            # panel.SetSizer(sizer)
            # sizer.Fit(self)

            self._mainSizer.Add(panel_sizer, wx.EXPAND|wx.ALL)
        else:
            self._mainSizer.Clear(delete_windows=True)

        self.AUIManager.Update()
        self.Parent.Refresh()
        self.Parent.Update()
