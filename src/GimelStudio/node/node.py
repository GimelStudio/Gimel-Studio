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

from GimelStudio.utils import (ConvertImageToWx, TruncateText)
from GimelStudio.stylesheet import *
from GimelStudio.datafiles.icons import *


class Node(object):
    def __init__(self, parent, nodedef, pos, _id=wx.ID_ANY):
        self._parent = parent
        self._nodedef = nodedef

        self._defaultSize = wx.Point(160, 116) # TODO

        self._IDName = nodedef.NodeIDName
        self._label = nodedef.NodeLabel
        self._category = nodedef.NodeCategory
        self._outputType  = nodedef.NodeOutputType
        self._supportsImagePacking = nodedef.NodeSupportsImagePacking
        self._packedImageData = {}
        self._properties = self._GetInitProperties()
        self._parameters = self._GetInitParameters()
        self._propertiesUI = nodedef.NodePropertiesUI
        self._evaluation = nodedef.NodeEvaluation

        self._id = self._GetInitID(_id)
        self._rect = self._GetInitRect(pos, wx.Point(160, 116)) #TODO
        self._nodeColor = self._GetInitNodeColor()
        self._toggleIcon = self._GetInitToggleIcon()
        self._thumbImage = self._GetInitThumbImage()
        self._drawThumb = False
        self._thumbCache = None
        self._isSelected = False
        self._isActive = False
        self._isDisabled = False

        self._evaluationData = self._GetInitEvalData()
        self._plugs = self._GetInitPlugs()

        nodedef._Init(self)


    def _GetInitEvalData(self):
        """ Returns the default evaldata format based on whether
        the node is an output composite node or not.

        Format examples:
        ---------------------------------------
        {"bind": "100"}
        {"name": "bind", "value": "100"}
        {"name": "path", "value": "example.jpg"}

        :returns: dict
        """
        properties = self._CreateDefaultProperties()

        if self.IsCompositeOutput() == True:
            eval_data =  {
                "bind": ""
                }
        else:
            eval_data = {
                "parameters": [],
                "properties": properties
                }

        return eval_data
 
    def _GetInitProperties(self):
        properties = {
            p.name: Property(p) for p in self._nodedef.NodeProperties
            }
        return properties

    def _GetInitParameters(self):
        parameters = {
            p.name: Parameter(p) for p in self._nodedef.NodeParameters
            }
        return parameters

    def _GetInitNodeColor(self):
        if self.GetCategory() in STYLE_NODES_COLOR_DICT.keys():
            return STYLE_NODES_COLOR_DICT[self.GetCategory()]
        else:
            return STYLE_NODES_COLOR_DICT["DEFAULT"]

    def _GetInitToggleIcon(self):
        if self.GetOutputType() == "RENDERIMAGE":
            return ICON_NODE_IMAGE_LIGHT.GetBitmap()
        else:
            return ICON_NODE_IMAGE_LIGHT.GetBitmap()

    @staticmethod
    def _GetInitThumbImage():
        # Default thumbnail is a transparent 256x256 image
        return Image.new('RGBA', (256, 256), (0, 0, 0, 1))

    @staticmethod
    def _GetInitID(_id):
        if _id == wx.ID_ANY:
            return wx.NewIdRef().GetValue()
        else:
            return _id

    @staticmethod
    def _GetInitRect(pos, size):
        return wx.Rect(
            pos.x,
            pos.y,
            size[0],
            size[1]
            )

    # TODO: FIXME
    def _GetInitPlugs(self):
        """ Returns the correct plugs based on the node definition. 

        :returns: a list of Plug objects
        """
        plugs = []
        
        ins = []
        for param in self._nodedef.NodeParameters:
            ins.append((param.name, param.param_type))

        outs = []
        if self.IsCompositeOutput() != True:
            outs = [('Output', self.GetOutputType())]

        x, y, w, h = self.GetRect().Get()
        for i, p in enumerate(ins + outs):
            plugtype = 0 # Plug type IN
            x = 2 # Plug margin
            if (p[0], p[1]) in outs:
                x = w - x + 1
                plugtype = 1 # Plug type OUT

            # We keep track of where the last plug is placed so that
            # we can place the thumbnail far enough below the plugs.
            self._thumbStartCoords = 40 + 20 * i

            plug = Plug(p[0], p[1], (x, 40 + 20 * i - 3), 6.5, plugtype, self)
            plugs.append(plug)

        return plugs

    def _CreateDefaultProperties(self):
        properties = []
        for prop in self.GetProperties():
            if self.GetPropertyType(prop) == "LIST":
                data = {
                    "name": self._properties[prop].Name,
                    "value": self._properties[prop].current_value.GetDefault()
                    }
            else:
                data = {
                    "name": self._properties[prop].Name,
                    "value": self._properties[prop].current_value
                    }
            properties.append(data)
        return properties

    def GetParent(self):
        return self._parent

    def GetNodeDef(self):
        return self._nodedef

    def GetDefaultSize(self):
        return self._defaultSize

    def UpdateNodeHeight(self, thumb_height):
        self.SetRect(
            wx.Rect(
                self.GetRect()[0],
                self.GetRect()[1],
                self.GetDefaultSize()[0],
                20+self._thumbStartCoords+thumb_height+20
                )
            )

    def GetIDName(self):
        return self._IDName

    def GetLabel(self):
        return self._label

    def SetLabel(self):
        return self._label

    def GetCategory(self):
        return self._category

    def GetOutputType(self):
        """ Return the data type this node outputs.

        :returns: string
        """
        return self._outputType

    def GetSupportsImagePacking(self):
        return self._supportsImagePacking

    def UpdatePackedImageData(self, image):
        self._packedImageData = image

    def GetPackedImageData(self):
        return self._packedImageData

    def GetProperties(self):
        return self._properties

    # TODO
    def GetPropertyType(self, prop):
        return self.GetProperties()[prop].definition.prop_type


    def EditProperty(self, name, value):
        """ Changes the value of a property for this node.

        :param name: the name of the property (as a string)
        :param value: value to set as the property value
        """
        if self.IsCompositeOutput() == False:
            # Loop over until we find the correct property
            for i in range (0, len(self.GetEvaluationData()["properties"])):
                if name == self.GetEvaluationData()["properties"][i]["name"]:
                    self.GetEvaluationData()["properties"][i]["value"] = value

            #print('PROPERTY DATA NODES:', self.GetEvaluationData())

    def GetParameters(self):
        return self._parameters

    @property
    def PropertiesUI(self):
        """ Returns the properties UI method associated with
        this node (from nodedef) for the Node Properties Panel.

        :returns: Python method
        """
        return self._propertiesUI

    @property
    def EvaluateNode(self):
        """ Returns the evaluation method associated with this 
        node (from nodedef) so that it can be rendered. 

        :returns: Python method
        """
        return self._evaluation

    def GetNodeEvaluation(self):
        """ Same as EvaluateNode property. 

        :returns: Python method
        """
        return self._evaluation

    def GetId(self):
        return self._id

    def SetId(self, _id):
        self._id = _id

    def GetRect(self):
        return self._rect
    
    def SetRect(self, rect):
        self._rect = rect

    def GetNodeColor(self):
        """ Returns the node color. 

        :returns: string
        """
        if self.IsDisabled() == True:
            return "grey"
        else:
            return self._nodeColor

    def GetToggleIcon(self):
        return self._toggleIcon

    def GetThumbImage(self):
        """ Returns the thumbnail image rendered for the current node. If this is
        the composite node, it returns the final rendered image.

        :returns: ``PIL.Image`` object
        """
        if self.IsCompositeOutput() != True:
            return self._thumbImage
        else:
            # If there is no rendered image yet, return 
            # the default transparent image
            rendered_img = self.GetRenderedImage()
            if rendered_img != None: 
                return rendered_img
            else:
                return self._GetInitThumbImage()

    def SetThumbImage(self, thumb):
        """ Same as UpdateThumbImage. 

        :param thumb: PIL Image object to set as the thumbnail
        """
        self._thumbImage = thumb

    def UpdateThumbImage(self, thumb):
        """ Update the thumbnail image. 

        :param thumb: PIL Image object to set as the thumbnail
        """
        self._thumbImage = thumb

    def GetDrawThumb(self):
        """ Get whether the thumbnail should be drawn 
        on the node.

        :returns: boolean
        """
        return self._drawThumb

    def SetDrawThumb(self, draw_thumb=True):
        """ Set whether the thumbnail should be drawn 
        on the node.

        :draw_thumb: boolean value
        :returns: nothing
        """
        self._drawThumb = draw_thumb

    def GetThumbCache(self):
        return self._thumbCache

    def SetThumbCache(self, thumb):
        self._thumbCache = thumb

    def IsSelected(self):
        return self._isSelected

    def SetSelected(self, is_selected=True):
        self._isSelected = is_selected

    def IsActive(self):
        return self._isActive

    def SetActive(self, is_active=True):
        self._isActive = is_active

    def IsDisabled(self):
        return self._isDisabled

    def SetDisabled(self, is_disabled=True):
        self._isDisabled = is_disabled

    def IsCoreNode(self):
        """ Whether this node is a core node. 

        :returns: boolean
        """
        # Better way to do this???
        if self.GetIDName().startswith("gimelstudiocorenode_"):
            is_corenode = True
        else:
            is_corenode = False
        return is_corenode

    def IsCompositeOutput(self):
        """ Whether this node is the core node Output Composite. 

        :returns: boolean
        """
        if self.GetIDName() == "gimelstudiocorenode_outputcomposite": # Hard coded!!
            is_composite_output = True
        else: 
            is_composite_output = False
        return is_composite_output

    def GetEvaluationData(self):
        return self._evaluationData

    def SetEvaluationData(self, data):
        self._evaluationData = data

    def GetPlugs(self):
        """ Return all the node plugs of this node.

        :returns: a list of Plug objects
        """
        return self._plugs

    def FindPlug(self, plug_name):
        """ Return the node plug with the given plug_name.

        :param plug_name: the plug name as a string
        :returns: Plug object
        """
        for plug in self.GetPlugs():
            #print(plug.GetLabel(), '\n')
            if plug.GetLabel() == plug_name:
                return plug

    def SetData(self, data):
        """ Sets the evaluation data dict for this node to the 
        proper data based on whether it is the composite node or not.

        :param data: dictionary of data to set
         """
        if self.IsCompositeOutput() == False:
            data = {
                "parameters": [],
                "properties": data["properties"]
                }
            self.SetEvaluationData(data)
    

    def ReadData(self):
        """ Reads all the parameter and property data for the 
        node from the evaluation data dict.
        """
        # TODO: Raise error instead of printing it
        if "parameters" in self.GetEvaluationData():
            for param in self.GetEvaluationData()["parameters"]:
                if param["name"] in self.GetParameters():
                    #print('B->',self._parameters[param['name']].binding)
                    self.GetParameters()[param["name"]].ReadData(param)
                    #print('A->', self._parameters[param['name']].binding)
                else:
                    print("WARNING: Parameter '{}' does not exist in node type {}".format(param["name"], self.GetIDName()))

        if "properties" in self.GetEvaluationData():
            for prop in self.GetEvaluationData()["properties"]:
                if prop["name"] in self.GetProperties():
                    self.GetProperties()[prop["name"]].ReadData(prop)
                else:
                    print("WARNING: Property '{}' does not exist in node type {}".format(prop["name"], self.GetIDName()))


    def GetMetaData(self):
        """ Returns the node's meta data as a Python dictionary.
        :returns: dict
        """
        node_meta = {
            "AUTHOR": self._nodedef.NodeAuthor,
            "VERSION": self._nodedef.NodeVersion,
            "DESCRIPTION": self._nodedef.NodeDescription,
            "IS_DEPRECIATED": self._nodedef.NodeIsDepreciated,
        }
        return node_meta

    def GetDrawData(self):
        """ Returns the data for drawing the node as a Python dictionary.
        :returns: dict
        """
        draw_data = {
            "COLOR": self.GetNodeColor(),
            "ICON": self.GetToggleIcon(),
        }
        return draw_data 

    def HitTest(self, x, y, thumb_btn_active=False):
        """ Toggles the node thumbnail if the icon was clicked and handles
        node plug hittests.
        """

        # Handle toggling the node's thumbnail
        if thumb_btn_active != False:
            pnt = wx.Point(x, y) - wx.Point(self.GetRect()[0]+136, self.GetRect()[1]+2/2)
            dist = math.sqrt(math.pow(pnt.x, 2) + math.pow(pnt.y, 2))

            if math.fabs(dist) < 18: # Icon hit radius
                if self.GetDrawThumb() == True:
                    self.SetThumbnailPreviewClosed(redraw=False)
                elif self.GetDrawThumb() == False:
                    self.SetThumbnailPreviewOpen(redraw=False)

                self.Draw(self.GetParent().GetPDC())
                self.GetParent().RefreshGraph()
            else:
                pass

        # Handle plug hittest
        for plug in self.GetPlugs():
            if plug.HitTest(wx.Point(x, y) - self.GetRect().GetPosition()):
                return plug


    def SetThumbnailPreviewOpen(self, redraw=True):
        """ Sets the node thumbnail preview to be toggled
        to show the thumb. 
        """
        self.SetDrawThumb(True)
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
        to hide the thumb. 
        """
        self.SetDrawThumb(False)
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


    def Delete(self, skip_del=False):
        """ Delete this node from the node graph. """
        for plug in self.GetPlugs():
            for wire in plug.GetWires():
                # Clean up any wires that are
                # connected to this node.
                dst = wire.dstPlug
                src = wire.srcPlug
                dst.Disconnect(src, render=False)
                self.GetParent().GetPDC().RemoveId(wire.GetId())

        if skip_del == False:
            del self.GetParent()._nodes[self.GetId()]
        self.GetParent().GetPDC().RemoveId(self.GetId()) 


    def EditProperties(self, propertyname, propertyvalue):
        if self.IsCompositeOutput() == True:
            pass
        else:
            for i in range(0, len(self.GetEvaluationData()["properties"])):
                # Change the value of the property
                if propertyname == self.GetEvaluationData()["properties"][i]['name']:
                    self.GetEvaluationData()["properties"][i]['value'] = propertyvalue

            #print('PROPERTY DATA NODES:', self.GetEvaluationData())
 

    def MakeConnection(self, plug1, plug2, render=True):
        if self.IsCompositeOutput() == True:
            self._evaluationData = {
                "bind": str(plug1.GetNode().GetId())
                }
            #print('CONNECTION DATA OUTPUT:', self._evalData)
        else:
            for param in self._parameters:
                if param == plug2.GetLabel():
                    #print('PARAM', param)
                    data = {
                        "name": self._parameters[param].Name,
                        "bind": str(plug1.GetNode().GetId())
                        }
                    self._evaluationData["parameters"].append(data)

            #print('CONNECTION DATA NODES:', self._evalData)

        # See if we should be updating (rendering) automatically
        if render == True:
            self.RenderNodeGraph()


    def MakeDisconnect(self, plug1, plug2, render=True):
        if self.IsCompositeOutput() == True:
            self._evaluationData= {
                "bind": ""
            }
        else:
            for i in range(0, len(self._evaluationData["parameters"])):
                if self._evaluationData["parameters"][i]["bind"] == str(plug1.GetNode().GetId()):
                    #print('deleting ->', self._evalData["parameters"][i])
                    del self._evaluationData["parameters"][i]
                    self._parameters[plug2.GetLabel()].binding = None


    def RenderNodeGraph(self):
        """ Render the Node Graph. """
        self._parent._parent.Render()


    def UpdateThumbCache(self):
        thumb = self.GetThumbImage().copy()
        thumb.thumbnail((round((self.GetRect()[2]-10)/1.1), thumb.size[1]))
        self.SetThumbCache(thumb)
        return thumb

    def GetRenderedImage(self):
        """ Get the completed rendered composite image. """
        return self.GetParent().GetParent().GetRenderedImage()

    @property
    def Theme(self):
        """ Gets the active UI theme. 

        :returns: theme dict
        """
        return self._parent.Theme

 
    def Draw(self, dc, use_cache=True):
        """ Draws the node on a wx.DC.
        :param dc: wx.DC on which to draw the node
        :param use_cache: Whether to use the cached thumbnail for this draw
        """
        dc.ClearId(self.GetId())
        dc.SetId(self.GetId())

        # Calculate the node height and thumb
        if self.GetDrawThumb() == True:

            # We should only NOT use the cache 
            # when the nodegraph is rendered again
            if use_cache != False:
                if self.GetThumbCache() != None:
                    thumb = self.GetThumbCache()
                    #print('INFO: USING CACHE')
                else:
                    # Create the thumbnail if this is the
                    # first time the node has been toggled
                    thumb = self.UpdateThumbCache()
            else:
                # Make a copy of the image so that we do not edit
                # the original with the 'thumbnail' function.
                thumb = self.UpdateThumbCache()
                
            # Update the node height
            self.UpdateNodeHeight(thumb.size[1])
            x, y, w, h = self.GetRect()
        else:
            x, y, w, h = self.GetRect()

        fnt = self.GetParent().GetParent().GetFont()
        #fnt = fnt.MakeBold()
        dc.SetFont(fnt)

        # Active/Unactive node
        if self.IsActive() == True:
            dc.SetPen(wx.Pen(wx.Colour(self.Theme["node_border_active"]), 2))
            dc.SetBrush(wx.Brush(wx.Colour(self.Theme["node_bg_active"]), wx.SOLID))
        elif self.IsActive() == False:
            # Select/Deselect node
            if self.IsSelected() == True:
                dc.SetPen(wx.Pen(wx.Colour(self.Theme["node_border_selected"]), 2))
                dc.SetBrush(wx.Brush(wx.Colour(self.Theme["node_bg_selected"]), wx.SOLID))
            elif self.IsSelected() == False:
                dc.SetPen(wx.Pen(self.Theme["node_border_normal"], 2))
                dc.SetBrush(wx.Brush(wx.Colour(self.Theme["node_bg_normal"]), wx.SOLID))

        # Draw main body of the node
        dc.DrawRoundedRectangle(x, y, w, h, 2)

        dc.SetPen(wx.TRANSPARENT_PEN)
        if self.IsActive() == True or self.IsSelected() == True:
            color = wx.Colour(self.GetNodeColor())
        else:
            color = wx.Colour(self.GetNodeColor()).ChangeLightness(105)

        dc.SetBrush(wx.Brush(color, wx.SOLID))
        dc.DrawRoundedRectangle(x+1, y+1, w-2, 24, 1)

        # Draw plugs
        dc.SetTextForeground(wx.Colour(self.Theme["node_plug_labels"]))
        for plug in self._plugs:
            plug.Draw(dc)

        # Icon
        dc.DrawBitmap(self.GetToggleIcon(), x+136, y+3, True)

        # Draw node text
        dc.SetTextForeground(wx.Colour('#FFFFFF'))
        dc.DrawText(TruncateText(self.GetLabel()), x+6, y+3)

        # Draw thumbnail
        if self.GetDrawThumb() == True:
            
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
            dc.SetPen(wx.Pen(wx.Colour(self.Theme["node_border_normal"])))
            dc.SetBrush(wx.Brush(wx.Colour(0, 0, 0, 0), wx.TRANSPARENT))
            dc.DrawRectangle(
                x+((w-thumbnail_width)/2),
                y+_y+20+self._thumbStartCoords,
                thumbnail_width,
                thumbnail_height,
                )

        dc.SetIdBounds(self.GetId(), self.GetRect())


