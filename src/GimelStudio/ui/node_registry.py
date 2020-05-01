## ----------------------------------------------------------------------------
## Gimel Studio © 2020 Correct Syntax, Noah Rahm. All rights reserved.
##
## FILE: node_registry.py
## AUTHOR(S): Noah Rahm
## PURPOSE: -
## ----------------------------------------------------------------------------

import wx
import wx.adv

from GimelStudio.stylesheet import STYLE_NODES_COLOR_DICT
from GimelStudio.datafiles.icons import *


class NodeRegistryItem(object):
    def __init__(
        self, parent, rect, name, label, version, author,
        category, desc, is_depreciated, icon="image"
        ):
        self._parent = parent
        self._rect = rect
        self._name = name
        self._label = label
        self._version = version
        self._author = author
        self._category = category
        self._icon = "image"
        self._desc = desc
        self._isDepreciated = is_depreciated
        self._id = wx.NewIdRef().GetValue()
        self._isCoreNode = False
        self._isSelected = False
        self._isHover = False
        self._dragndropData = wx.TextDataObject(self._name)

    def GetParent(self):
        return self._parent

    def GetId(self):
        return self._id

    def GetRect(self):
        return self._rect

    def SetRect(self, rect):
        self._rect = rect

    def GetName(self):
        return self._name

    def GetLabel(self):
        return self._label

    def GetColor(self):
        if self._category in STYLE_NODES_COLOR_DICT.keys():
            return STYLE_NODES_COLOR_DICT[self._category]
        else:
            return STYLE_NODES_COLOR_DICT["DEFAULT"]

    def GetIcon(self):
        if self._icon == "image":
            return ICON_NODE_IMAGE_LIGHT.GetBitmap()

    def GetVersion(self):
        return self._version

    def GetAuthor(self):
        return self._author

    def GetDescription(self):
        return self._desc

    def GetIsDepreciated(self):
        return self._isDepreciated

    def GetIsCoreNode(self):
        return self._isCoreNode

    def SetIsCoreNode(self, is_corenode):
        self._isCoreNode = is_corenode

    def IsSelected(self):
        return self._isSelected

    def SetSelected(self, is_selected):
        self._isSelected = is_selected

    def SetHover(self, ishover):
        self._isHover = ishover

    def GetHover(self):
        return self._isHover

    def GetDragNDropInfo(self):
        return self._dragndropData

    def Draw(self, dc):
        dc.ClearId(self.GetId())
        dc.SetId(self.GetId())
        x, y, w, h = self.GetRect()

        sys_scrollbar_x = wx.SystemSettings.GetMetric(
            getattr(wx, 'SYS_VSCROLL_X')
            )

        if self.IsSelected() == True:
            dc.SetPen(wx.Pen(wx.Colour('#80b3ffff'), 4))

            # Draw Background
            dc.SetBrush(wx.Brush(wx.Colour('white'), wx.SOLID))
            dc.DrawRectangle(x, y, w-sys_scrollbar_x, h)

        elif self.IsSelected() == False:
            dc.SetPen(wx.Pen('black', 1))

            # Draw Background
            if self.GetHover() == True:
                dc.SetBrush(wx.Brush(wx.Colour('white'), wx.SOLID))
                dc.DrawRectangle(x, y, w-sys_scrollbar_x, h)
            else:
                dc.SetBrush(wx.Brush(wx.Colour('#ECECEC'), wx.SOLID))
                dc.DrawRectangle(x, y, w-sys_scrollbar_x, h)

        # Draw Colored Heading Background
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 0, 0), 1))
        dc.SetBrush(wx.Brush(wx.Colour(self.GetColor()), wx.SOLID))
        dc.DrawRectangle(x, y, w-sys_scrollbar_x, h-56)

        # Draw Node Label Text
        dc.SetTextForeground(wx.Colour('white'))
        #dc.SetFont(self.GetParent().GetParent().GetFont().MakeSmaller())
        dc.DrawText(self.GetLabel(), x+28, y+2)

        # Draw Icon
        dc.DrawBitmap(
            self.GetIcon(), x+6, y+2, True)

        # Draw Version and Author Text
        dc.SetTextForeground(wx.Colour('#ECECEC'))

        if self.GetIsCoreNode() != True:
            # TODO add icon for custom nodes
            #print("CUSTOM NODE")
            pass
        else:
            dc.DrawBitmap(
                ICON_GIMELSTUDIO_LOGO.GetBitmap(),
                x+w-sys_scrollbar_x-24,
                y+2,
                True
                )
        dc.DrawText('v{}'.format(self.GetVersion()), x+w-sys_scrollbar_x-70, y+2)

        # Draw Description Text
        dc.SetTextForeground(wx.Colour('black'))

        if self.GetIsDepreciated() == True:
            is_depreciated_msg = "\nTHIS NODE WILL BE REMOVED IN A FUTURE RELEASE."
            dc.DrawText(self.GetDescription() + is_depreciated_msg, x+6, y+28)
        else:
            dc.DrawText(self.GetDescription(), x+6, y+28)



class NodeRegistry(wx.ScrolledWindow):
    def __init__(self, parent, noderegistry, size=wx.DefaultSize):
        wx.ScrolledWindow.__init__(self, parent, size=size)

        self._noderegistry = noderegistry
        self._parent = parent
        self._selectednodeitem = None
        self._ndregistryitems = {}
        self.ITEMHEIGHT = 80
        self._maxheight = ((len(noderegistry) + 2) * self.ITEMHEIGHT) - self.ITEMHEIGHT
        self._maxwidth = 1000

        # Handle scrolling
        self.SetVirtualSize((self._maxwidth, self._maxheight))
        self.SetScrollRate(14, 14)

        # Create a PseudoDC to record our drawing
        self._pdc = wx.adv.PseudoDC()

        self.InitNodeItems()
        self.DrawNodeItems()

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: None)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnSize(self, event):
        self.DrawNodeItems()

    def OnMouseLeave(self, event):
        # Reset items when the mouse leaves the frame
        for i in self._ndregistryitems:
            if self._ndregistryitems[i].IsSelected() != True:
                self._ndregistryitems[i].SetHover(False)
                self._ndregistryitems[i].Draw(self._pdc)
        self.RefreshPanel()

    def OnPaint(self, event):
        # Create a buffered paint DC.  It will create the real wx.PaintDC and
        # then blit the bitmap to it when dc is deleted.
        dc = wx.BufferedPaintDC(self)
        dc = wx.GCDC(dc)

        # Use PrepareDC to set position correctly.
        self.PrepareDC(dc)

        # We need to clear the dc BEFORE calling PrepareDC.
        dc.SetBackground(wx.Brush(wx.Colour('#ECECEC')))
        dc.Clear()

        # Draw to the dc using the calculated clipping rect.
        self._pdc.DrawToDCClipped(
            dc, wx.Rect(0, 0, self._maxwidth, self._maxheight)
            )


    def OnLeftDown(self, event):
        pnt = event.GetPosition()
        winpnt = self.ConvertCoords(pnt)
        self._nodeitem = self.HitTest(winpnt)

        if self._nodeitem != None:
            # Handle node selection
            if self._selectednodeitem == None:
                self._selectednodeitem = self._nodeitem
                self._selectednodeitem.SetSelected(True)
                self._selectednodeitem.Draw(self._pdc)

            else:
                if self._nodeitem.GetId() != self._selectednodeitem.GetId():
                    self._selectednodeitem.SetSelected(False)
                    self._selectednodeitem.Draw(self._pdc)
                    self._selectednodeitem = self._nodeitem
                    self._selectednodeitem.SetSelected(True)
                    self._selectednodeitem.Draw(self._pdc)

            # Handle dnd node items to Node Graph
            dragSource = wx.DropSource(self)
            dragSource.SetData(self._selectednodeitem.GetDragNDropInfo())
            result = dragSource.DoDragDrop(True)

            self.RefreshPanel()


    def OnMotion(self, event):
        # Hover for items
        pnt = event.GetPosition()
        winpnt = self.ConvertCoords(pnt)
        for i in self._ndregistryitems:
            btn_region = wx.Region(self._ndregistryitems[i].GetRect())
            if btn_region.Contains(winpnt[0], winpnt[1]):
                self._ndregistryitems[i].SetHover(True)
            else:
                self._ndregistryitems[i].SetHover(False)
            self._ndregistryitems[i].Draw(self._pdc)
        self.RefreshPanel()

    def InitNodeItems(self):
        for nodedefId in self._noderegistry:
            nitem = self._noderegistry[nodedefId]()

            # Exclude the ouput composite node
            if self._noderegistry[nodedefId]()._name != "corenode_outputcomposite":
                noderegistryitem = NodeRegistryItem(
                    self,
                    wx.Rect(0, 0, self.Size[0], self.ITEMHEIGHT),
                    nitem._name,
                    nitem._label,
                    nitem._version,
                    nitem._author,
                    nitem._category,
                    nitem._description,
                    nitem._isdepreciated,
                    "image"#nitem._icon
                    )

                # Check to see if this is a core node
                if str(nitem._name).startswith("corenode_"):
                    noderegistryitem.SetIsCoreNode(True)
                else:
                    noderegistryitem.SetIsCoreNode(False)

                self._ndregistryitems[noderegistryitem.GetId()] = noderegistryitem

    def DrawNodeItems(self):
        y = 0
        for nritem in self._ndregistryitems:
            self._ndregistryitems[nritem].SetRect(
                wx.Rect(0, y, self.Size[0], self.ITEMHEIGHT)
                )
            self._ndregistryitems[nritem].Draw(self._pdc)
            self._pdc.SetIdBounds(
                self._ndregistryitems[nritem].GetId(),
                self._ndregistryitems[nritem].GetRect()
                )
            y += self.ITEMHEIGHT + 8

    def GetSelectedItem(self):
        if self._selectednodeitem == None:
            return None
        else:
            return self._selectednodeitem.GetName()


    def HitTest(self, pt):
        idxs = self._pdc.FindObjects(pt[0], pt[1], 25)
        hits = [
            idx
            for idx in idxs
            if idx in self._ndregistryitems
        ]

        if hits != []:
            return self._ndregistryitems[hits[0]]
        else:
            if self._selectednodeitem != None:
                self._selectednodeitem.SetSelected(False)
                self._selectednodeitem.Draw(self._pdc)

                self.RefreshPanel()
                self._selectednodeitem = None
            return None


    def ConvertCoords(self, pnt):
        xView, yView = self.GetViewStart()
        xDelta, yDelta = self.GetScrollPixelsPerUnit()
        return wx.Point(pnt[0] + (xView * xDelta), pnt[1] + (yView * yDelta))

    def OffsetRect(self, r):
        xView, yView = self.GetViewStart()
        xDelta, yDelta = self.GetScrollPixelsPerUnit()

    def RefreshPanel(self):
        """ Refreshes the panel so that everything is redrawn. """
        rect = wx.Rect(0, 0, self.Size[0], self.Size[1])
        self.OffsetRect(rect)
        self.RefreshRect(rect, False)
