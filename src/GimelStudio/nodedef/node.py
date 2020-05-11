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
## FILE: node.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the node object with its parameters & properties data
##
## This file includes code that was modified from wxnodegraph 
## (https://github.com/Derfies/wxnodegraph) which is licensed under the MIT 
## License, Copyright 2016
## ----------------------------------------------------------------------------

import math
import wx
from PIL import Image

from .plug import Plug
from .property import Property
from .parameter import Parameter
from GimelStudio.utils import (ConvertImageToWx, DrawCheckerBoard,
                               TruncateText)
from GimelStudio.stylesheet import STYLE_NODES_COLOR_DICT
from GimelStudio.datafiles.icons import *


class Node(object):
    """ The node class is used to represent a single step within the rendered
    output composite. Nodes may be linked together in the node graph to
    allow for complex image compositing.
    """
    def __init__(self, parent, definition, pos, _id=wx.ID_ANY):
        self._parent = parent
        self._userprefmanager = parent.GetParent().GetUserPrefManager()
        self._definition = definition
        self._name = definition._name
        self._category = definition._category
        self._label = definition._label
        self._color = self._InitColor()
        self._icon = self._InitIcon()
        self._defaultSize = definition._size
        self._output = definition._output

        # Default thumbnail is a transparent 256x256 image
        self._thumbnail = Image.new(
            'RGBA', (256, 256), (0, 0, 0, 1)
            )
        self._drawThumbnail = False
        self._thumbCache = None

        self._isSelected = False
        self._isActive = False
        self._isDisabled = False
        self._labelFrame = None
        self._pos = pos

        if _id == wx.ID_ANY:
            self._id = wx.NewIdRef().GetValue()
        else:
            self._id = _id

        self._rect = wx.Rect(
            self._pos.x,
            self._pos.y,
            self._defaultSize[0],
            self._defaultSize[1]
            )

        self._parameters = {
            p.name: Parameter(p) for p in definition._parameters
            }
        self._properties = {
            p.name: Property(p) for p in definition._properties
            }

        self._evalData = self._InitEvalData()
        self._plugs = self._InitPlugs()
        self._definition._Init(self)


    def _InitPlugs(self):
        """ Returns the correct plugs based on the node definition. """
        plugs = []

        ins = []
        for param in self._definition._parameters:
            ins.append((param.name, param.param_type))

        outs = []
        if self.IsCompositeNode() != True:
            outs = [('Output', self._output)]

        x, y, w, h = self.GetRect().Get()
        for i, p in enumerate(ins + outs):
            plugtype = 0 # Plug type IN
            x = 3 # Plug margin
            if (p[0], p[1]) in outs:
                x = w - x + 1
                plugtype = 1# Plug type OUT

            # We keep track of where the last plug is placed so that
            # we can place the thumbnail far enough below the plugs.
            self._thumbStartCoords = 40 + 20 * i

            plug = Plug(p[0], p[1], (x, 40 + 20 * i), 6.5, plugtype, self)
            plugs.append(plug)

        return plugs


    def _InitEvalData(self):
        """ Returns the correct evaldata format based on whether
        the node is an output node or not.

        Format examples:
        {"bind": "100"}
        {"name": "bind", "value": "100"}
        {"name": "path", "value": "example.jpg"}
        """
        # Set the default properties
        properties = self._CreateDefaultProperties()

        if self.IsCompositeNode() == True:
            return {
                "bind": ""
                }
        else:
            return {
                "parameters": [],
                "properties": properties
                }

    def _CreateDefaultProperties(self):
        properties = []
        for prop in self._properties:
            prop_type = self._properties[prop].definition.prop_type
            if prop_type == 'list':
                data = {
                    "name": self._properties[prop].name,
                    "value": self._properties[prop].current_value.GetValue()
                    }
            else:
                data = {
                    "name": self._properties[prop].name,
                    "value": self._properties[prop].current_value
                    }
            properties.append(data)
        return properties


    def _InitIcon(self):
        if self._definition._output == "image":
            return ICON_NODE_IMAGE_LIGHT.GetBitmap()
        else:
            return ICON_NODE_IMAGE_LIGHT.GetBitmap()


    def _InitColor(self):
        if self._category in STYLE_NODES_COLOR_DICT.keys():
            return STYLE_NODES_COLOR_DICT[self._category]
        else:
            return STYLE_NODES_COLOR_DICT["DEFAULT"]

    def GetUserPrefManager(self):
        return self._userprefmanager

    def GetDrawThumbnail(self):
        return self._drawThumbnail

    def SetDrawThumbnail(self, drawthumbnail):
        self._drawThumbnail = drawthumbnail

    def HasThumbnail(self):
        if self._thumbnail != None:
            return True
        else:
            return False

    def GetThumbnail(self):
        return self._thumbnail

    def UpdateThumbnail(self, thumbnail):
        self._thumbnail = thumbnail

    def UpdateNodeHeight(self, thumb_height):
        self.SetRect(
            wx.Rect(
                self.GetRect()[0],
                self.GetRect()[1],
                self.GetDefaultSize()[0],
                20+self._thumbStartCoords+thumb_height+20
                )
            )

    def SetThumbCache(self, thumb):
        self._thumbCache = thumb

    def GetThumbCache(self):
        return self._thumbCache

    def GetParent(self):
        return self._parent

    def GetId(self):
        return self._id

    def SetId(self, id_):
        self._id = id_

    def GetName(self):#GetType
        return self._name

    def GetLabel(self):
        return self._label

    def SetLabel(self, label):
        self._label = label

    def GetCategory(self):
        return self._category

    def GetRect(self):
        return self._rect

    def SetRect(self, rect):
        self._rect = rect

    def IsSelected(self):
        return self._isSelected

    def SetSelected(self, is_selected):
        self._isSelected = is_selected

    def IsActive(self):
        return self._isActive

    def SetActive(self, is_active):
        self._isActive = is_active

    def GetColor(self):
        return self._color

    def SetColor(self, color):
        self._color = color

    def GetIcon(self):
        return self._icon

    def GetDefaultSize(self):
        return self._defaultSize

    def GetOutput(self):
        return self._output

    def IsDisabled(self):
        return self._isDisabled

    def SetDisabled(self, is_disabled):
        self._isDisabled = is_disabled

    def GetPlugs(self):
        return self._plugs

    def FindPlug(self, plug_name):
        for plug in self.GetPlugs():
            #print(plug.GetLabel(), '\n')
            if plug.GetLabel() == plug_name:
                return plug

    def IsCompositeNode(self): # IsOutputNode
        """ Returns whether the node is the output composite. """
        if self.GetName() != 'corenode_outputcomposite':
            return False
        else:
            return True

    def SetThumbnailPreviewOpen(self, redraw=True):
        """ Sets the node thumbnail preview to be toggled
        to show the thumb. """
        self.SetDrawThumbnail(True)
        self.SetRect(
            wx.Rect(
                self.GetRect()[0],
                self.GetRect()[1],
                self.GetRect()[2],#160,
                self.GetRect()[3]
                )
            )
        if redraw == True:
            self.Draw(self.GetParent().GetPDC())

    def SetThumbnailPreviewClosed(self, redraw=True):
        """ Sets the node thumbnail preview to be toggled
        to hide the thumb. """
        self.SetDrawThumbnail(False)
        self.SetRect(
            wx.Rect(
                self.GetRect()[0],
                self.GetRect()[1],
                self.GetDefaultSize()[0],
                self.GetDefaultSize()[1]
                )
            )
        if redraw == True:
            self.Draw(self.GetParent().GetPDC())

    def HitTest(self, x, y, thumb_btn_active=False):
        if self.IsCompositeNode() != True:
            # Handle toggling the node's thumbnail
            if thumb_btn_active != False:
                pnt = wx.Point(x, y) - wx.Point(self.GetRect()[0]+6/2, self.GetRect()[1]+2/2)
                dist = math.sqrt(math.pow(pnt.x, 2) + math.pow(pnt.y, 2))

                # Icon hit radius
                if math.fabs(dist) < 16:
                    if self.GetDrawThumbnail() == True:
                        self.SetThumbnailPreviewClosed(redraw=False)
                    elif self.GetDrawThumbnail() == False:
                        self.SetThumbnailPreviewOpen(redraw=False)

                    self.Draw(self.GetParent().GetPDC())
                    self.GetParent().RefreshGraph()
                else:
                    pass

        # Handle plug hittest
        for plug in self.GetPlugs():
            if plug.HitTest(wx.Point(x, y) - self.GetRect().GetPosition()):
                return plug

    @property
    def Evaluate(self):
        """ The evaluation function associated with this node. """
        return self._definition._evaluate

    @property
    def PropertiesUI(self):
        """ The properties UI function associated with
        this node for the properties panel.
        """
        return self._definition._properties_ui


    def SetData(self, data):
        if self.IsCompositeNode() == True:
            pass
        else:
            self._evalData = {
                "parameters": [],
                "properties": data["properties"]
                }

    def ReadData(self):
        """ Reads all properties for the node that have been
        defined within the supplied JSON data.
        """
        if 'parameters' in self._evalData:
            for p in self._evalData['parameters']:
                if p['name'] in self._parameters:
                    #print('B->',self._parameters[p['name']].binding)
                    self._parameters[p['name']].ReadData(p)
                    #print('A->', self._parameters[p['name']].binding)
                else:
                    print("WARNING: Parameter '{}' does not exist in node type {}".format(p['name'], self._definition._name))

        if 'properties' in self._evalData:
            for p in self._evalData['properties']:
                if p['name'] in self._properties:
                    self._properties[p['name']].ReadData(p)
                else:
                    print("WARNING: Property '{}' does not exist in node type {}".format(p['name'], self._definition._name))


    def EditProperties(self, propertyname, propertyvalue):
        if self.IsCompositeNode() == True:
            pass
        else:
            for i in range (0, len(self._evalData["properties"])):
                # Change the value of the property
                if propertyname == self._evalData["properties"][i]['name']:
                    self._evalData["properties"][i]['value'] = propertyvalue

            print('PROPERTY DATA NODES:', self._evalData)


    def MakeConnection(self, plug1, plug2, render=True):
        if self.IsCompositeNode() == True:
            self._evalData= {
                "bind": str(plug1.GetNode().GetId())
                }
            #print('CONNECTION DATA OUTPUT:', self._evalData)
        else:
            for param in self._parameters:
                if param == plug2.GetLabel():
                    #print('PARAM', param)
                    data = {
                        "name": self._parameters[param].name,
                        "bind": str(plug1.GetNode().GetId())
                        }
                    self._evalData["parameters"].append(data)

            #print('CONNECTION DATA NODES:', self._evalData)

        # See if we should be updating (rendering) automatically
        if render == True:
            #pass
            self.RenderNodeGraph()



    def MakeDisconnect(self, plug1, plug2, render=True):
        if self.IsCompositeNode() == True:
            self._evalData= {
                "bind": ""
            }
        else:
            val = 0
            for param in self._evalData["parameters"]:

                #print(self._evalData["parameters"], param, 'i')

                if self._evalData["parameters"][val]["bind"] == str(plug1.GetNode().GetId()):
                    #print('deleting ->', self._evalData["parameters"][val])
                    del self._evalData["parameters"][val]
                    self._parameters[plug2.GetLabel()].binding = None

                else:
                    pass
                    #self._evalData["parameters"] = []
                    # print('IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII')
                val += 1

##            for i in range (0, len(self._evalData["parameters"])):
##
##                print(self._evalData["parameters"], i, 'i')
##
##                if self._evalData["parameters"][i]["bind"] == str(plug1.GetNode().GetId()):
##                    print('deleting ->', self._evalData["parameters"][i])
##                    del self._evalData["parameters"][i]
##                    self._parameters[plug2.GetLabel()].binding = None
##
##                else:
##                    #self._evalData["parameters"] = []
##                    print('IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII')
##
##
##
##
##
##
        #print('CONNECTION DATA NODES:', self._evalData)

        # See if we should be updating (rendering) automatically
        if render == True:
            #pass
            self.RenderNodeGraph()


    def Delete(self, skip_del=False):
        for plug in self.GetPlugs():
            for wire in plug.GetWires():
                # Clean up any wires that are
                # connected to this node.
                dst = wire.dstPlug
                src = wire.srcPlug
                dst.Disconnect(src, render=False)
                self.GetParent().GetPDC().RemoveId(wire.GetId())
        # Delete the labelframe, if it has one
        #self.DeleteLabelFrame()
        if skip_del == False:
            del self.GetParent()._nodes[self.GetId()]
        self.GetParent().GetPDC().RemoveId(self.GetId())

    def RenderNodeGraph(self):
        if self._userprefmanager.GetRendererAutoRender() == True:
            self.GetParent().GetParent().Render()
 
    def Draw(self, dc, use_cache=True):
        """ Draws the full node on the wx.DC.
        :param dc: wx.DC to draw the node on
        :param use_cache: Whether to use the cached thumbnail for this draw
        """
        dc.ClearId(self.GetId())
        dc.SetId(self.GetId())

        # Calculate the node height
        if self.IsCompositeNode() != True and self.GetDrawThumbnail() == True:

            # We should only NOT use the cache 
            # when the nodegraph is rendered again
            if use_cache != False:
                if self.GetThumbCache() != None:
                    thumb = self.GetThumbCache()
                    #print('INFO: USING CACHE')
                else:
                    # Create the thumbnail if this is the
                    # first time the node has been toggled
                    # TODO: This is repeating code
                    thumb = self.GetThumbnail().copy()
                    thumb.thumbnail((round((self.GetRect()[2]-10)/1.1), thumb.size[1]))
                    self.SetThumbCache(thumb) 
            else:
                # Make a copy of the image so that we do not edit
                # the original with the 'thumbnail' function.
                thumb = self.GetThumbnail().copy()
                thumb.thumbnail((round((self.GetRect()[2]-10)/1.1), thumb.size[1]))
                self.SetThumbCache(thumb)
                
            # Update the node height
            self.UpdateNodeHeight(thumb.size[1])
            x, y, w, h = self.GetRect()
        else:
            x, y, w, h = self.GetRect()

        # Active/Unactive node
        if self.IsActive() == True:
            dc.SetPen(wx.Pen(wx.Colour('#FFFFFF'), 1.75))
        elif self.IsActive() == False:
            # Select/Deselect node
            if self.IsSelected() == True:
                dc.SetPen(wx.Pen(wx.Colour('#FFFFFF'), 1.75))
            elif self.IsSelected() == False:
                dc.SetPen(wx.Pen('#373737', 1.75))

        # Draw main body of the node
        dc.SetBrush(wx.Brush(wx.Colour('#6F6F6F'), wx.SOLID))
        dc.DrawRoundedRectangle(x, y, w, h, 3)

        # Draw label background
        dc.SetPen(wx.TRANSPARENT_PEN)

        # Enable/Disable node
        if self.IsDisabled() == True:
            dc.SetBrush(wx.Brush(wx.Colour('grey'), wx.SOLID ))
        elif self.IsDisabled() == False:
            dc.SetBrush(wx.Brush(wx.Colour(self.GetColor()), wx.SOLID))
        dc.DrawRoundedRectangle(x+1, y+1, w-2, h-84, 3)

        # Draw node body background
        dc.SetBrush(wx.Brush(wx.Colour('#6F6F6F'), wx.SOLID))
        dc.DrawRectangle(x+1, y+20, w-2, h-30)

        # Icon
        dc.DrawBitmap(self.GetIcon(), x+6, y, True)

        # Draw node text
        dc.SetTextForeground(wx.Colour('white'))
        dc.SetFont(self.GetParent().GetParent().GetFont().MakeSmaller())
        dc.DrawText(TruncateText(self.GetLabel()), x+28, y+1)

        # Draw plugs
        for plug in self._plugs:
            plug.Draw(dc)

        # Draw thumbnail if the node is not the output node
        if self.IsCompositeNode() != True and self.GetDrawThumbnail() == True:
            # Max size
            thumbnail_width = round((w-10)/1.1)
            thumbnail_height = thumb.size[1]

            _x = thumbnail_width/2.0-thumb.size[0]/2.0
            _y = thumbnail_height/2.0-thumb.size[1]/2.0

            # Draw thumbnail image
            dc.DrawBitmap(
                wx.Bitmap(ConvertImageToWx(thumb)),
                x+_x+((w-thumbnail_width)/2),
                y+_y+20+self._thumbStartCoords,
                True
                )

            # Draw thumbnail border
            dc.SetPen(wx.Pen(wx.Colour('#373737')))
            dc.SetBrush(wx.Brush(wx.Colour(0, 0, 0, 0), wx.TRANSPARENT))
            dc.DrawRectangle(
                x+((w-thumbnail_width)/2),
                y+_y+20+self._thumbStartCoords,
                thumbnail_width,
                thumbnail_height
                )

        dc.SetIdBounds(self.GetId(), self.GetRect())
