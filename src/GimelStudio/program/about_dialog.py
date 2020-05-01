## ----------------------------------------------------------------------------
## Gimel Studio © 2020 Correct Syntax, Noah Rahm. All rights reserved.
##
## FILE: about_dialog.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Defines the Gimel Studio about dialog
## ----------------------------------------------------------------------------

import wx
from wx.lib.wordwrap import wordwrap

from GimelStudio.meta import (__NAME__, __AUTHOR__, __VERSION__,
                              __BUILD__, __RELEASE__, __TITLE__)


class AboutGimelStudioDialog(object):
    def __init__(self, parent):
        self._parent = parent
        self._name = __NAME__
        self._title = __TITLE__
        self._author = __AUTHOR__
        self._version = __VERSION__
        self._build = __BUILD__
        self._release = __RELEASE__
    
    def ShowDialog(self):
        info = wx.adv.AboutDialogInfo()
        info.SetName(self._name)
        info.SetVersion("v{0}.{1}".format(self._version, self._release))
        info.SetCopyright("© 2020 {}. All rights reserved.".format(self._author))
        info.SetDescription(
            wordwrap(
                margin=10,
                text="""
Non-destructive (node-based), realtime graphics editing program for Windows and Linux.

Praise to YAHWEH for allowing the time and resources to make this software program a reality. Please consider giving your feedback through the program menu (Help > Feedback Survey) so that I can work to improve Gimel Studio. :)
                """,
                width=550, 
                dc=wx.ClientDC(self._parent)
                ))
        info.SetWebSite("https://correctsyntax.com/projects/gimel-studio/", "Visit the Gimel Studio Homepage")

        wx.adv.AboutBox(info)
        
