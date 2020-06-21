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
## FILE: nodebase.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the core base class for all nodes with a high-level API
## ----------------------------------------------------------------------------


 
class NodeBase(object):
    """ Base class for all nodes which defines the node's core attributes."""
    def __init__(self):
        # Node Meta
        self._author = self.NodeAuthor
        self._version = self.NodeVersion
        self._description = self.NodeDescription
        self._isDepreciated = self.NodeIsDepreciated
 
        # Node Attributes
        self._IDName = self.NodeIDName
        self._label = self.NodeLabel
        self._category = self.NodeCategory
        self._outputType  = self.NodeOutputType
        self._properties = self.NodeProperties
        self._parameters = self.NodeParameters
        self._propertiesUI = self.NodePropertiesUI
        self._evaluation = self.NodeEvaluation

        # Other values to be set later
        self._isCorenode = None
        self._isCompositeOutput = None 

        # Variables for convienience 
        self.ui = None
        self.parent = None
        self.sizer = None

    def _Init(self, node):
        """ Internal method: PLEASE DO NOT OVERRIDE! 
        This will be set automatically on runtime.
        """
        self._node_obj = node

    @property
    def NodeOBJ(self):
        """ Returns the Node object for use in this class.
        :returns: Node object
        """
        return self._node_obj

    @property
    def NodeAuthor(self):
        """ Name of the author of this node
        :returns: a string
        """
        return ""

    @property
    def NodeVersion(self):
        """ Version string of the node formatted as [major].[minor] 
        :returns: a string
        """
        return "0.1"

    @property
    def NodeDescription(self):
        """ Description of what the node does for the end user to see 
        in the Node Registry, etc.
        :returns: a string
        """
        return "N/A"

    @property
    def NodeIsDepreciated(self):
        """ Whether this node is being depreciated or removed from 
        the Node Registry soon.
        :returns: a boolean value of True or False
        """
        return False

    @property
    def NodeIDName(self):
        """ Pseudo name ID of this node. This is not the same as 
        the node label -think of this like the ID of the node kind 
        you are creating. 
        
        Leaving this blank will result in an error.
        
        WARNING: THIS MUST BE UNIQUE FROM OTHER NODES IN THE 
        NODE REGISTRY!

        :returns: a string
        """
        return "" 

    @property
    def NodeLabel(self):
        """ The shown text of the label for the node. This can be 
        different from the node name.
        :returns: a string
        """
        return "N/A"

    @property
    def NodeCategory(self):
        """ The category of the node. This can be one of the 
        following category values (in all uppercase):

        Category | Hex Value | Color Name
        ---------------------------------
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

        :returns: a string
        """
        return "DEFAULT"

    @property 
    def NodeOutputType(self):
        """ The type of data the node outputs. This can be one of the 
        following data types:

        Data type | Description
        ------------------------------------------------
        "RENDERIMAGE": will output a RenderImage instance

        :returns: a string
        """
        return "RENDERIMAGE"

    @property
    def NodeProperties(self):
        """ List of node properties for the node. These will translate 
        into properties in the Node Properties Panel.
        :returns: a list of PropertyDefinition objects
        """
        return [] 

    @property
    def NodeParameters(self):
        """ List of node parameters for the node. These will translate 
        into plugs on the node itself.
        :returns: a list of ParameterDefinition objects
        """
        return []

    def NodePropertiesUI(self, node, parent, sizer):
        pass

    def NodeEvaluation(self, eval_info):
        """ This is the method that is called during rendering 
        of the image. This should contain the actual code which does
        something to the data type (e.g: blurs the image, RENDERIMAGE data-type)
        and should return it as that same data type.
        :returns: the same data type as specified by NodeOutputType
        """
        pass

    # Convienience methods
    def NodePropertiesUpdate(self, propertyname, value):
        """ Updates the node property to be the specified value. """
        self.NodeOBJ.EditProperties(propertyname, value)
        self.NodeOBJ.GetParent().RefreshGraph()
        self.NodeOBJ.GetParent().GetParent().Render() 


    # FIXME
    def NodePropertiesHelperInit(self, node, ui, parent, sizer):
        """ Sets values as params of the current node object. """
        self.ui = ui #self.wx = wx
        self.parent = parent
        self.sizer = sizer

    def NodeSetThumb(self, image):
        self.NodeOBJ.UpdateThumb(image)

    def NodeGetPropertyValue(self, name):
        """ Get the current value of this node's property.
        """
        for i in range (0, len(self.NodeOBJ.GetEvaluationData()["properties"])):
            if self.NodeOBJ.GetEvaluationData()["properties"][i]["name"] == name:
                return self.NodeOBJ.GetEvaluationData()["properties"][i]["value"]
            else:
                print("WARNING: The property {} could not be found.".format(name))

