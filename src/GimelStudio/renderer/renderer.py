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
import json

from .output_node import OutputNode


class Renderer(object):
    """ The renderer which builds the node tree, resolves 
    each node's evaldata and outputs the final image and rendertime.
    """
    def __init__(self, parent):
        self._parent = parent
        self._renderedimg = None
        self._rendertime = 0.00

    def GetRenderedImage(self):
        return self._renderedimg
    
    def SetRenderedImage(self, renderedimage):
        self._renderedimg = renderedimage
        
    def GetRenderTime(self):
        return self._rendertime

    def SetRenderTime(self, rendertime):
        self._rendertime = rendertime

    def GetParent(self):
        return self._parent

    def Render(self, nodes):
        """ Main render method for rendering a nodegraph."""
        # Start timing rendertime
        start_time = time.time()

        # Build node tree and render the image
        output = self._BuildNodeTree(nodes)
        image = output.RenderImage()

        if image != None: 
            # Set renderedimg
            self.SetRenderedImage(image.GetImage())
 
            # Set rendertime
            self.SetRenderTime(time.time() - start_time)
        else:
            pass

    def _BuildNodeTree(self, nodes):
        """ Builds the node tree and resolves the node parameters
        and properties and returns the output. In addition, it counts
        the number of nodes in use that are not disabled.
        """
        nodetree = {}
        for nodeId in nodes:
            if nodes[nodeId].IsCompositeNode() != True:
                nodetree[str(nodes[nodeId].GetId())] = nodes[nodeId] 
                nodes[nodeId].ReadData()
            else:
                outputnode = nodes[nodeId]

        self._ResolveNodes(nodetree)

        output = self._CreateOutput(outputnode._evalData, nodetree)
        return output   

    def _ResolveParameters(self, node, nodes):
        """
        Given a single node, this method resolves any references to other nodes
        within the parameter list.
        """
        for _, param in node._parameters.items():
            if param.binding != None:
                param.binding = nodes[param.binding]

    def _ResolveNodes(self, nodes):
        """
        Given a list of nodes, this method resolves all the parameters that make
        reference to other nodes.
        """
        for item in nodes.items():
            self._ResolveParameters(item[1], nodes)
 
    def _CreateOutput(self, data, nodes):
        """
        Creates the output node from the supplied data.
        """
        if 'bind' in data:
            output = OutputNode()
            output.ReadData(data, nodes)
     
        return output
