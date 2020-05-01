## ----------------------------------------------------------------------------
## Gimel Studio © 2020 Correct Syntax, Noah Rahm. All rights reserved.
##
## FILE: renderer.py
## AUTHOR(S): Noah Rahm
## PURPOSE: -
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
        self._renderedNodeCount = 0
        self._rendertime = 0.00

    def GetRenderedImage(self):
        return self._renderedimg
    
    def SetRenderedImage(self, renderedimage):
        self._renderedimg = renderedimage

    def GetRenderedNodeCount(self):
        return self._renderedNodeCount

    def SetRenderedNodeCount(self, node_count):
        self._renderedNodeCount = node_count
        
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
        #self.GetParent().statusbar.SetStatusText("Building Node Tree...")

        # Build node tree and render the image
        output = self._BuildNodeTree(nodes)
        #self.GetParent().statusbar.SetStatusText("Rendering Image...")
        image = output.RenderImage()

        if image != None: 
            # Set renderedimg
            self.SetRenderedImage(image.GetImage())
 
            # Set rendertime
            self.SetRenderTime(time.time() - start_time)
            #self.GetParent().statusbar.SetStatusText(
                #"Render Finished In {} Seconds".format(round(self.GetRenderTime(), 3))
                #)
        else:
            pass
            #self.GetParent().statusbar.SetStatusText("")


    def _BuildNodeTree(self, nodes):
        """ Builds the node tree and resolves the node parameters
        and properties and returns the output. In addition, it counts
        the number of nodes in use that are not disabled.
        """
        nc = 0
        nodetree = {}
        for nodeId in nodes:
            if nodes[nodeId].IsCompositeNode() != True:
                nodetree[str(nodes[nodeId].GetId())] = nodes[nodeId] 
                nodes[nodeId].ReadData()
                if nodes[nodeId].IsDisabled() != True:
                    nc += 1
            else:
                outputnode = nodes[nodeId]


        self.SetRenderedNodeCount(nc)
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
