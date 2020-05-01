## ----------------------------------------------------------------------------
## Gimel Studio © 2020 Correct Syntax, Noah Rahm. All rights reserved.
##
## FILE: nodebase.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the core base class for all nodes with a higher-level API
## ----------------------------------------------------------------------------

from PIL import Image


class NodeBase(object):
    """ Base class with defaults for all nodes to inherit from. """
    def __init__(self):
        # Meta
        self._author = self.NodeAuthor
        self._version = self.NodeVersion
        self._description = self.NodeDescription
        self._isdepreciated = self.NodeIsDepreciated
 
        # Attributes
        self._name = self.NodeName
        self._label = self.NodeLabel
        self._category = self.NodeCategory
        self._size = self.NodeSize
        self._output = self.NodeOutput

        self._properties = self.NodeProperties
        self._parameters = self.NodeParameters

        self._evaluate = self.NodeEvaluation
        self._properties_ui = self.NodePropertiesUI

        # Variables for convienience 
        self.node = None
        self.ui = None
        self.parent = None
        self.sizer = None

    # Internal methods: DO NOT OVERRIDE!
    def _Init(self, node):
        self.node = node

    def _GetNodeMetadata(self):
        return [
            self._author, # 0
            self._version,# 1
            self._description # 2
            ]

    def _GetNodeAttributes(self):
        return [
            self._name, # 0
            self._label, # 1
            self._category, # 2
            self._size, # 3
            self._output # 4
            ]

    def _GetNodeProperties(self):
        return self._node_properties

    def _GetNodeParameters(self):
        return self._node_parameters

    def _GetNodePropertiesUI(self):
        return self._properties_ui

    def _GetNodeEvaluation(self):
        return self._node_evaluation

    # Default attributes and meta
    @property
    def NodeAuthor(self):
        return ""

    @property
    def NodeVersion(self):
        return "1.0.0"

    @property
    def NodeDescription(self):
        return ""

    @property
    def NodeIsDepreciated(self):
        return False

    @property
    def NodeName(self):
        return ""

    @property
    def NodeLabel(self):
        return "[Label]"

    @property
    def NodeCategory(self):
        # Value is set to the default category
        # and color if this is left blank.
        return ""

    @property
    def NodeSize(self):
        # default size
        return [200, 130] # Classic size: [160, 110]
    @property 
    def NodeOutput(self):
        # default output type
        return 'image'

    @property
    def NodeProperties(self):
        return [] 

    @property
    def NodeParameters(self):
        return []

    def NodePropertiesUI(self, node, ui, parent, sizer):
        pass

    def NodeEvaluation(self, eval_info):
        pass

    # Convienience methods
    def NodePropertiesUpdate(self, propertyname, value):
        """ Updates the node property to be the specified value. """
        self.node.EditProperties(propertyname, value)
        self.node.GetParent().RefreshGraph()
        self.node.GetParent().GetParent().Render() 

    def NodePropertiesHelperInit(self, node, ui, parent, sizer):
        """ Sets values as params of the current node object. """
        self.ui = ui #self.wx = wx
        self.parent = parent
        self.sizer = sizer

    def NodeSetThumbnail(self, image):
        self.node.UpdateThumbnail(image)

    def NodeGetPropertyValue(self, propertyname):
        for i in range (0, len(self.node._evalData["properties"])):
            if self.node._evalData["properties"][i]['name'] == propertyname:
                return self.node._evalData["properties"][i]['value']
