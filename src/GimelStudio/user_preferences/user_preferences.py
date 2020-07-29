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
## FILE: user_preferences.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the program user preferences manager to manage user prefs
## ----------------------------------------------------------------------------

import os
import json

from GimelStudio.meta import __VERSION__
 

DEFAULT_USER_PREFERENCES = {
    "ui": {
        "active_theme": "dark_theme",
        "light_theme": {
            "app_bg": "#FFFFFF",
            "dock_pnl_bg": "#FFFFFF",
            "dock_pnl_caption_txt": "#000000",
            "node_graph_bg": "#F7F7F7",
            "node_graph_grid": "false",
            "node_bg_active": "#C3C3C3",
            "node_bg_selected": "#C3C3C3",
            "node_bg_normal": "#C3C3C3",
            "node_border_active": "#414141",
            "node_border_selected": "#414141",
            "node_border_normal": "#808080",
            "node_wire_active": "#414141",
            "node_wire_normal": "#808080",
            "node_plug_border": "#808080",
            "node_plug_labels": "#414141",
            "node_wire_curving": 0,
            },

        "dark_theme": {
            "app_bg": "#FFFFFF",
            "dock_pnl_bg": "#FFFFFF",
            "dock_pnl_caption_txt": "#000000",
            "node_graph_bg": "#505050",
            "node_graph_grid": "true",
            "node_bg_active": "#6F6F6F",
            "node_bg_selected": "#6F6F6F",
            "node_bg_normal": "#6F6F6F",
            "node_border_active": "#FFFFFF",
            "node_border_selected": "#FFFFFF",
            "node_border_normal": "#373737",
            "node_wire_active": "#ECECEC",
            "node_wire_normal": "#C1C1C1",
            "node_plug_border": "#373737",
            "node_plug_labels": "#FFFFFF",
            "node_wire_curving": 0,
            },
        },
    "renderer": {
        "auto_render": True,
    }
}

  
class UserPreferencesManager(object):
    def __init__(self, parent):
        self._parent = parent
        self._userprefs = DEFAULT_USER_PREFERENCES

    @property
    def UserPref(self):
        return self._userprefs

    @property
    def Theme(self):
        return self.GetTheme()

    def GetActiveTheme(self):
        return self._userprefs["ui"]["active_theme"]

    def GetTheme(self):
        return self._userprefs["ui"][self.GetActiveTheme()]

    def SetActiveTheme(self, theme_name):
        self._userprefs["ui"]["active_theme"] = theme_name

    def GetNodeWireCurving(self):
        return self._userprefs["ui"][self.GetActiveTheme()]["node_wire_curving"]

    def SetNodeWireCurving(self, wirecurving):
        self._userprefs["ui"][self.GetActiveTheme()]["node_wire_curving"] = wirecurving

    def GetRendererAutoRender(self):
        return self._userprefs["renderer"]["auto_render"]

    def SetRendererAutoRender(self, autorender):
        self._userprefs["renderer"]["auto_render"] = autorender

    def Load(self):
        try:
            os.makedirs(
                os.path.expanduser("~/.gimelstudio/".format(__VERSION__)),
                exist_ok=True
                )
            with open(
                os.path.expanduser(
                    "~/.gimelstudio/{}-config.json".format(__VERSION__)
                    ),
                "r"
                ) as file:
                self._userprefs = json.load(file)
        except IOError:
            pass # Just use default


    def Save(self):
        try:
            with open(
                os.path.expanduser(
                    "~/.gimelstudio/{}-config.json".format(__VERSION__)
                    ),
                "w"
                ) as file:
                json.dump(self._userprefs, file)
        except IOError:
            pass # Not a big deal

    def Overwrite(self):
        pass
