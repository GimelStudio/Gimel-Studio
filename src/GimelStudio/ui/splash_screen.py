## ----------------------------------------------------------------------------
## Gimel Studio © 2020 Correct Syntax, Noah Rahm. All rights reserved.
##
## FILE: splash_screen.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the program's startup splash screen
## ----------------------------------------------------------------------------

import wx
import wx.adv

from GimelStudio.datafiles.splash import SPLASH_GIMEL_STUDIO


class StartupSplashScreen(wx.adv.SplashScreen):
    def __init__(self):
        _bmp = SPLASH_GIMEL_STUDIO.GetBitmap()
        bmp = wx.Image.ConvertToBitmap(
            wx.Bitmap.ConvertToImage(_bmp).Scale(
                _bmp.GetWidth()/2,
                _bmp.GetHeight()/2,
                wx.IMAGE_QUALITY_HIGH
                )
            )
        wx.adv.SplashScreen.__init__(self, bmp,
                                     wx.adv.SPLASH_CENTRE_ON_SCREEN
                                     | wx.adv.SPLASH_NO_TIMEOUT,
                                     5000, None, -1)

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        

    def OnClose(self, event):
        # Make sure the default handler runs too
        # so this window gets destroyed.
        event.Skip()
        self.Hide()
