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
        "wire_curving": 0,
        "wire_shadow": True,
        "node_shadow": False,
        },
    "renderer": {
        "auto_render": True
        }
    }


class UserPreferencesManager(object):
    def __init__(self, parent):
        self._parent = parent
        self._userprefs = DEFAULT_USER_PREFERENCES

    def GetUIWireCurving(self):
        return self._userprefs["ui"]["wire_curving"]

    def SetUIWireCurving(self, wirecurving):
        self._userprefs["ui"]["wire_curving"] = wirecurving

    def GetUIWireShadow(self):
        return self._userprefs["ui"]["wire_shadow"]

    def SetUIWireShadow(self, wireshadow):
        self._userprefs["ui"]["wire_shadow"] = wireshadow

    def GetUINodeShadow(self):
        return self._userprefs["ui"]["node_shadow"]

    def SetUINodeShadow(self, nodeshadow):
        self._userprefs["ui"]["node_shadow"] = nodeshadow

    def GetRendererAutoRender(self):
        return self._userprefs["renderer"]["auto_render"]

    def SetRendererAutoRender(self, autorender):
        self._userprefs["renderer"]["auto_render"] = autorender

    def Load(self):
        try:
            os.makedirs(
                os.path.expanduser("~/.gimelstudio{}/".format(__VERSION__)),
                exist_ok=True
                )
            with open(
                os.path.expanduser(
                    "~/.gimelstudio{}/user-pref.json".format(__VERSION__)
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
                    "~/.gimelstudio{}/user-pref.json".format(__VERSION__)
                    ),
                "w"
                ) as file:
                json.dump(self._userprefs, file)
        except IOError:
            pass # Not a big deal

    def Overwrite(self):
        pass
