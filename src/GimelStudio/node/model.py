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
## FILE: model.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the model for the node
## ----------------------------------------------------------------------------

import math 

import wx
from wx.lib.embeddedimage import PyEmbeddedImage
from PIL import Image

from GimelStudio.datafiles import *
from .socket import Socket


# Nodes
STYLE_NODES_COLOR_DICT = {
    "INPUT": "#975B5B", # Burgendy
    "DRAW": "#AF4467", # Pink
    "CONVERT": "#564B7C", # Purple
    "VALUE": "#CC783D", # Orange
    "FILTER": "#558333", # Green
    "BLEND": "#498DB8", # Light blue
    "COLOR": "#C2AF3A", # Yellow
    "DISTORT": "#6B8B8B", # Blue-Grey
    "OUTPUT": "#B33641", # Red
    "DEFAULT": "#975B5B" # Burgendy
}

 
class NodeModel(object):
    """ Holds the data for the node. The intention is that this class
    will be THE one that you can know has the latest, updated data.
     """
    def __init__(self, _id):
        self._id = _id
        self._parent = None
        self._type = "" # idname
        self._backgroundColor = (109, 111, 111, 255)
        self._borderColor = (55, 55, 55, 255)
        self._headerColor = (0, 0, 0, 255)
        self._socketColor = (0, 0, 0, 255)
        self._textColor = (255, 255, 255, 255)
        self._isOutput = False
        self._label = ""
        self._category = "DEFAULT"
        self._muted = False
        self._selected = False
        self._active = False
        self._size = wx.Size(160, 116)
        self._position = wx.Point(0, 0)
        self._sockets = []
        self._lastCoords = 0

        # Default thumbnail is a transparent 256x256 image
        self._thumbImage = Image.new('RGBA', (256, 256), (0, 0, 0, 1))  
        self._thumbCache = None
        
        self._properties = {}
        self._parameters = {}

        self._author = ""
        self._version = (0, 0, 1)
        self._supportedAppVersion = (0, 0, 0)
        self._description = ""

    def AddProperty(self, prop):
        self._properties[prop.IdName] = prop
        return self._properties

    def AddParameter(self, param):
        self._parameters[param.IdName] = param
        return self._parameters
 
    def EditProperty(self, idname, value, render=True):
        prop = self._properties[idname]
        prop.SetValue(value, render)
        return prop

    def SetRect(self, rect):
        self.SetPosition(wx.Point(rect[0], rect[1]))
        self.SetSize(wx.Size(rect[2], rect[3]))

    def GetRect(self):
        return wx.Rect(
            self.GetPosition()[0],
            self.GetPosition()[1],
            self.GetSize()[0],
            self.GetSize()[1],
            )

    def GetId(self):
        return self._id

    def SetId(self, unique_id):
        self._id = unique_id

    def GetParent(self):
        return self._parent

    def SetParent(self, parent):
        self._parent = parent

    def GetType(self):
        return self._type

    def SetType(self, node_type):
        self._type = node_type

    def GetLabel(self):
        return self._label

    def SetLabel(self, label):
        self._label = label

    def GetCategory(self):
        return self._category

    def SetCategory(self, category):
        self._category = category
 
    def GetNodeHeaderColor(self):
        if self._category in STYLE_NODES_COLOR_DICT.keys():
            return STYLE_NODES_COLOR_DICT[self._category]
        else:
            return STYLE_NODES_COLOR_DICT["DEFAULT"]

    def GetNodeColor(self):
        return self._backgroundColor

    def SetNodeColor(self, color):
        self._backgroundColor = color

    def GetSocketColor(self):
        return self._socketColor

    def SetSocketColor(self, color):
        self._socketColor = color

    def GetBorderColor(self):
        if self.IsSelected() is True or self.IsActive() is True:
            self.SetBorderColor((255, 255, 255, 255))
        else:
            self.SetBorderColor((55, 55, 55, 255))
        return self._borderColor

    def SetBorderColor(self, color):
        self._borderColor = color

    def GetTextColor(self):
        return self._textColor

    def SetTextColor(self, color):
        self._textColor = color

    def IsSelected(self):
        return self._selected

    def SetSelected(self, selected):
        self._selected = selected

    def IsActive(self):
        return self._active

    def SetActive(self, active):
        self._active = active

    def IsMuted(self):
        return self._muted

    def SetMuted(self, state=False):
        self._muted = state

    def GetSize(self):
        return self._size

    def SetSize(self, size):
        self._size = size
 
    def GetPosition(self):
        return self._position

    def SetPosition(self, pos):
        self._position = pos

    def IsOutputNode(self):
        return self._isOutput

    def GetSockets(self):
        return self._sockets

    def GetParameters(self):
        return self._parameters

    def GetProperties(self):
        return self._properties

    def GetLastSocketCoords(self):
        return self._lastCoords

    def GetThumbImage(self):
        return self._thumbImage

    def SetThumbImage(self, thumb):
        self._thumbImage = thumb

    def GetThumbCache(self):
        return self._thumbCache

    def SetThumbCache(self, thumb):
        self._thumbCache = thumb

    def UpdateThumbnail(self, image):
        """ Update the thumbnail. This saves the thumb image and creates
        a thumbnail in the cache.
        
        :param image: PIL Image
        """
        self.SetThumbImage(image)
        thumb = self.CreateThumbnail(image)
        self.SetThumbCache(thumb)
        self.CalcNewSize(thumb.size[1])

    def CreateThumbnail(self, image):
        """ Create a thumbnail sized to the correct dimensions for display
        as the node thumbnail.
        
        :param image: PIL Image
        :returns: PIL Image sized to the correct dimensions
        """
        thumb = image.copy()
        thumb.thumbnail((round((self.GetSize()[0]-10)/1.1), thumb.size[1]))
        return thumb

    def CalcNewSize(self, thumb_height, set_size=True, border=20):
        """ Calculate the new size of the node based on the current 
        thumbnail and border, then sets it if `set_size` param is true.
        
        :param thumb_height: height of the current thumb image
        :param set_size: whether to set the node to the calculated dimensions
        :param border: border (in pixels) to be placed above and below thumb image
        :returns: the size of the node as wx.Size
        """
        width = 160 # Hard-coded value
        height = self._lastCoords+thumb_height+(border*2)
        size = wx.Size(width, height)
        if set_size == True:
            self.SetSize(size)
        return size

    def HitTest(self, x, y):
        """ Handles node socket hit-tests.

        :param x: x coord
        :param y: y coord
        """
 
        # Handle socket hittest
        for socket in self.GetSockets():
            if socket.HitTest(wx.Point(x, y) - self.GetPosition()):
                return socket

    def UpdateSockets(self):
        """ Sets the correct sockets based on the node. """

        sockets = []
         
        ins = []
        for param in self.GetParameters():
            ins.append((param, "RENDERIMAGE"))

        outs = [] 
        if self.IsOutputNode() != True:
            outs = [('Output', "RENDERIMAGE")]

        x, y, w, h = self.GetRect()
        for i, p in enumerate(ins + outs):
            socket_type = 0 # Socket type IN
            x = 2 # Plug margin
            if (p[0], p[1]) in outs:
                x = w - x + 1
                socket_type = 1 # Socket type OUT

            # We keep track of where the last socket is placed so that
            # we can place the thumbnail far enough below the sockets.
            self._lastCoords = 40 + 20 * i

            socket = Socket(p[0], p[1], (x, 40 + 19 * i), 6.5, socket_type, self)
            sockets.append(socket)

        self._sockets = sockets

    @property
    def NodeGraph(self):
        return self._parent

    @property
    def ModelViewData(self):
        data =  {
            'id': self.GetId(),
            'type': self.GetType(),
            'label': self.GetLabel(),
            'header_color': self.GetNodeHeaderColor(),
            'color': self.GetNodeColor(),
            'socket_color': self.GetSocketColor(),
            'border_color': self.GetBorderColor(),
            'text_color': self.GetTextColor(),
            'selected': self.IsSelected(),
            'active': self.IsActive(),
            'muted': self.IsMuted(),
            'size': self.GetSize(),
            'position': self.GetPosition(),
            'is_output': self.IsOutputNode(),
            'sockets': self.GetSockets(),
            'last_socket_coords': self.GetLastSocketCoords(),
            'thumbnail': self.GetThumbCache()
        }
        return data
