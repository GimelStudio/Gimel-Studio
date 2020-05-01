## ----------------------------------------------------------------------------
## Gimel Studio © 2020 Correct Syntax, Noah Rahm. All rights reserved.
##
## FILE: nodeframe.py
## AUTHOR(S): Noah Rahm
## PURPOSE: -
## ----------------------------------------------------------------------------

import wx
import wx.lib.agw.cubecolourdialog as CCD


# class GenericTextBox(object):
#     def __init__(self, parent, text="text here", pos=wx.Point(0, 0), _id=wx.ID_ANY):
#         self._parent = parent
#         self._text = text
#         self._pos = pos
#         self._isActive = True

#         if _id == wx.ID_ANY:
#             self._id = wx.NewId()
#         else:
#             self._id = _id
        
#         tdc = wx.WindowDC(wx.GetApp().GetTopWindow())
#         w, h = tdc.GetTextExtent(self.GetText())

#         self._rect = wx.Rect(
#             self._pos.x, 
#             self._pos.y, 
#             w,
#             h
#             )

#     def GetParent(self):
#         return self._parent

#     def GetId(self):
#         return self._id

#     def SetId(self, id_):
#         self._id = id_

#     def GetRect(self):
#         return self._rect

#     def SetRect(self, rect):
#         self._rect = rect

#     def SetPosition(self, x, y):
#         self._pos = wx.Point(x, y)

#     def GetPosition(self):
#         return self._pos

#     def SetText(self, text):
#         self._text = text

#     def GetText(self):
#         return self._text

#     def GetIsActive(self):
#         return self._isActive

#     def SetIsActive(self, active):
#         self._isActive = active

#     def Draw(self, dc):
#         dc.ClearId(self.GetId())
#         dc.SetId(self.GetId())

#         dc.SetTextForeground('white')
#         if self.GetIsActive() == True:
#             dc.SetPen(wx.Pen(wx.Colour('#FFFFFF'), 1.75))
#         else:
#             dc.SetPen(wx.Pen('transparent', 1))
#         dc.SetBrush(wx.Brush(wx.Colour('transparent'), wx.SOLID))
#         dc.DrawRectangle(self.GetRect())
 
#         x, y = self.GetPosition()
#         dc.DrawText(self.GetText(), x, y)



 
class NodeFrame(object):
    def __init__(self, pos=wx.Point(0, 0)):
        self._id = wx.NewId()
        self._rect = wx.Rect(pos.x, pos.y, 300, 220)
        self._text = '...'
        self._color = wx.Colour(608, 608, 608, 627)
        self._isSelected = False

    def SetLabelText(self, text):
        self._text = text

    def GetLabelText(self):
        return self._text

    def SetRect(self, rect):
        self._rect = rect

    def GetRect(self):
        return self._rect
    
    def GetId(self):
        return self._id

    def SetSelected(self, selected):
        self._isSelected = selected
    
    def GetIsSelected(self):
        return self._isSelected

    def GetColor(self):
        return self._color

    def SetColor(self, r, g, b):
        self._color = wx.Colour(r, g, b, 627)

    def EditColorDialog(self):
        dlg = wx.ColourDialog(None)

        # Ensure the full colour dialog is displayed,
        # not the abbreviated version.
        dlg.GetColourData().SetChooseFull(True)

        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            colordata = data.GetColour().Get()
            self.SetColor(colordata[0],
                          colordata[1],
                          colordata[2])
        dlg.Destroy()

    def EditTextDialog(self):
        dlg = wx.TextEntryDialog(
                None, 'Edit the text for the Node Frame Label:',
                'Node Frame Label', '')

        dlg.SetValue(self.GetLabelText())

        if dlg.ShowModal() == wx.ID_OK:
            self.SetLabelText(dlg.GetValue())
        dlg.Destroy()

    def Draw(self, dc, pos=wx.Point(0, 0)):         
        dc.ClearId(self.GetId())
        dc.SetId(self.GetId())
        
        x, y, w, h = self._rect.Get()

        dc.SetBrush(wx.Brush(self.GetColor(), wx.SOLID))

        if self.GetIsSelected() == True:
            dc.SetPen(wx.Pen('white', 2))
        else:
            dc.SetPen(wx.Pen('white', 1))
        dc.DrawRoundedRectangle(x, y, w, h, 6)
        dc.DrawLabel(self.GetLabelText(), wx.Rect(int(x+10), int(y+1), 2, 1))

        dc.SetIdBounds(self.GetId(), self.GetRect())
