## ----------------------------------------------------------------------------
## Gimel Studio © 2020 Correct Syntax, Noah Rahm. All rights reserved.
##
## FILE: Gimel Studio.py (entry-point)
## AUTHOR(S): Noah Rahm
## PURPOSE: The entry-point for the Gimel Studio application
## ----------------------------------------------------------------------------

import argparse
import wx

from GimelStudio.meta import  __TITLE__, __DEBUG__
from GimelStudio.application import MainApplication
from GimelStudio.ui import StartupSplashScreen


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
    frame = MainApplication(
        arguments=args
        )
    if __DEBUG__ != True:
        splash = StartupSplashScreen()
        splash.Show()
    frame.Show()
    app.SetTopWindow(frame)
    app.MainLoop()
