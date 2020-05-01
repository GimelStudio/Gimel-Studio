## ----------------------------------------------------------------------------
## Gimel Studio © 2020 CorrectSyntax Software, Noah Rahm. All rights reserved.
##
## FILE: radio_buttons.py
## AUTHOR(S): Noah Rahm
## PURPOSE: -
## ----------------------------------------------------------------------------
import os
import wx

from GimelStudio.utils import ConvertImageToWx

##self.lvPics = AssetLibrary(id=wxID_PNLPFSPROJECTLVPICS,
##              name=u'lvPics', parent=self, pos=wx.Point(-1, -1),
##              size=wx.Size(-1, -1),
##              style=wx.HSCROLL)  # | wx.ALWAYS_SHOW_SB)
##        self.lvPics.Bind(wx.EVT_LIST_ITEM_SELECTED,
##              self.OnLvPicsSelectionChanged, id=wxID_PNLPFSPROJECTLVPICS)
##
def ChopText(dc, text, maxSize):
    """
    Chops the input `text` if its size does not fit in `maxSize`, by cutting the
    text and adding ellipsis at the end.

    :param `dc`: a `wx.DC` device context;
    :param `text`: the text to chop;
    :param `maxSize`: the maximum size in which the text should fit.
    """

    # first check if the text fits with no problems
    width, __ = dc.GetTextExtent(text)

    if width <= maxSize:
        return text, width

    for i in range(len(text), -1, -1):
        s = '%s ... %s' % (text[:i * 33 // 100], text[-i * 67 // 100:])

        width, __ = dc.GetTextExtent(s)

        if width <= maxSize:
            break
    return s, width








EVT_CHANGED_TYPE = wx.NewEventType()
EVT_CHANGED = wx.PyEventBinder(EVT_CHANGED_TYPE, 1)


class ChangedEvent(wx.PyCommandEvent):

    def __init__(self, wxId):
        wx.PyCommandEvent.__init__(self, EVT_CHANGED_TYPE, wxId)


class AssetLibrary(wx.ScrolledWindow):

    GAP = 10
    BORDER = 45
    THUMB_HEIGHT = 120
    LABEL_MARGIN = 8

    STRIP_HEIGHT = THUMB_HEIGHT + 2 * BORDER

    def __init__(self, parent, id=-1,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.HSCROLL | wx.VSCROLL):
        wx.ScrolledWindow.__init__(self, parent, id, pos, size, style)

