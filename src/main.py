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
## FILE: main.py (entry-point)
## AUTHOR(S): Noah Rahm
## PURPOSE: The entry-point for the Gimel Studio application
## ----------------------------------------------------------------------------

import argparse
import wx

from GimelStudio.meta import  APP_TITLE, APP_DEBUG
from GimelStudio.application import MainApplication

# Fix blurry text on Windows 10
# from https://stackoverflow.com/questions/50884283/how-to-fix-blurry-text-in-wxpython-controls-on-windows
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except:
    pass


if __name__ == '__main__':

    args = None


    # Create the app and startup
    app = wx.App(redirect=False)
    frame = MainApplication(
        arguments=args
        )

    frame.Show()
    app.SetTopWindow(frame)
    app.MainLoop()
