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
## FILE: export.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the image export options tab of the Image Viewport
## ----------------------------------------------------------------------------

import wx
import wx.adv

from PIL import Image

from GimelStudio.utils import ConvertImageToWx, DrawCheckerBoard
from GimelStudio.datafiles.icons import *



class ExportOptionsPnl(wx.Panel):
    def __init__(self, parent, size=wx.DefaultSize):
        wx.Panel.__init__(self, parent, size=size)

            self.panel_staticbox = wx.StaticBox(
                self, id=wx.ID_ANY, 
                label=selected_node.GetLabel(), 
                size=wx.Size(self.Size[0], self.Size[1])
                )
 
            # This gets the recommended amount of border space to use for items
            # within in the static box for the current platform.
            top_bd, other_bd = self.panel_staticbox.GetBordersForSizer()

            staticbox_sizer = wx.BoxSizer(wx.VERTICAL)
            staticbox_sizer.AddSpacer(top_bd)

            self.panel_staticbox.SetSizer(staticbox_sizer)

            panel_sizer = wx.BoxSizer(wx.VERTICAL)
            panel_sizer.Add(self.panel_staticbox, 1, wx.EXPAND|wx.ALL, other_bd+10)

            # Node Properties UI
            selected_node.PropertiesUI(selected_node, self.panel_staticbox, staticbox_sizer)

            self._mainSizer.Add(panel_sizer, wx.EXPAND|wx.ALL)







class ImageExportPnl(wx.Panel):
    def __init__(self, parent, size=wx.DefaultSize):
        wx.Panel.__init__(self, parent, size=size)

        self._parent = parent







