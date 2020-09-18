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
## FILE: renderer.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the core renderer 
##
## This file includes code that was modified from imagegen 
## (https://github.com/nfactorial/imagegen) which is licensed 
## under the Apache License Version 2.0 
## Copyright 2016 nfactorial
## ----------------------------------------------------------------------------

import time

from .output_node import OutputNode


class Renderer(object):
    """ The core renderer which evaluates the data of the node tree and 
    outputs the final render image and render time.
    """
    def __init__(self, parent):
        self._parent = parent
        self._render = None
        self._time = 0.00

    def GetParent(self):
        return self._parent

    def GetRender(self):
        return self._render
    
    def SetRender(self, render):
        self._render = render
        
    def GetTime(self):
        return self._time

    def SetTime(self, time):
        self._time = round(time, 3)

    def Render(self, nodes):
        """ Render method for evaluating the Node Graph 
        to render an image.

        :param nodes: dictionary of nodes of the Node Graph
        """
        # Start timing the render
        start_time = time.time()

        # Render the image
        output_node = self.GetOutputNode(nodes)
        rendered_image = self.RenderNodeGraph(output_node, nodes)

        # Get rendered image, otherwise use 
        # the default transparent image.
        if rendered_image != None: 
            image = rendered_image.GetImage()
        else:
            image = output_node.Parameters["Image"].value.GetImage()

        output_node.NodeSetThumb(image)
        self.SetRender(image)

        # Set rendertime
        self.SetTime(time.time() - start_time)

    def RenderNodeGraph(self, output_node, nodes):
        """ Render the image, starting from the output node.

        :param output_node: the output node object
        :param nodes: dictionary of nodes of the Node Graph
        :returns: RenderImage object
        """
        output_data = OutputNode()
        output_data.SetNode(output_node)
        return output_data.RenderImage()

    def GetOutputNode(self, nodes):
        """ Get the output composite node.
        
        :param nodes: dictionary of nodes of the Node Graph
        :returns: node object of output node
        """
        for nodeId in nodes:
            if nodes[nodeId].IsOutputNode() == True:
                output_node = nodes[nodeId]
        return output_node
