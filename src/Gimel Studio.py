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
## FILE: Gimel Studio.py (entry-point)
## AUTHOR(S): Noah Rahm
## PURPOSE: The entry-point for the Gimel Studio application
## ----------------------------------------------------------------------------

import argparse
import wx

from GimelStudio.node_importer import *
from GimelStudio.meta import  __TITLE__, __DEBUG__
from GimelStudio.application import MainApplication
#from GimelStudio.ui import StartupSplashScreen


if __name__ == '__main__':
    # Parse the arguments to see if a file is given, otherwise
    # fallback on the default Gimel Studio project file.
    parser = argparse.ArgumentParser(
        description=__TITLE__
        )
    parser.add_argument(
        'file',
        nargs='?',
        default="DEFAULT_FILE",
        help="Open a Gimel Studio Project file in Gimel Studio"
        )
    args = parser.parse_args()

    # Create the app and startup
    app = wx.App(redirect=False)
    #print(app.outputWindowClass)
    frame = MainApplication(
        arguments=args
        )
    
    if __DEBUG__ != True:
        #splash = StartupSplashScreen()
        #splash.Show()
        pass
    frame.Show()
    app.SetTopWindow(frame)
    app.MainLoop()
