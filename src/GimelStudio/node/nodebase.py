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
        self.parent = None
        self.sizer = None

    def _Init(self, node):
        """ Internal init method. Do not override! 
        This will be set automatically on runtime.
        """
        self._node_obj = node

    @property
    def Node(self):
        """ Returns the ``Node`` object for use in 
        this API class.

        .. note::
            Be careful when accessing internal values via this property. Changing values on runtime may result in unstablity and unusabilty of the program.

        :returns: ``Node`` object
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
        """ UNUSED!!!!
        Whether this node is being depreciated or removed from 
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
        
        .. warning::
            THIS MUST BE UNIQUE FROM OTHER NODES IN THE NODE REGISTRY!
            Avoid starting the Id name with "gimelstudio" to prevent possible
            clashes between Core nodes and your custom node.

        :returns: a string
        """
        return "" 

    @property
    def NodeLabel(self):
        """ The shown (human-readable) text of the label for the node. This can be 
        different from the node Id name.

        :returns: a string
        """
        return "N/A"

    @property
    def NodeCategory(self):
        """ The category of the node. This can be one of the 
        following category values (in all uppercase):

        Category | Hex Value | Color Name

        | "INPUT": "#975B5B", # Burgendy
        | "DRAW": "#AF4467", # Pink
        | "CONVERT": "#564B7C", # Purple
        | "VALUE": "#CC783D", # Orange
        | "FILTER": "#558333", # Green
        | "BLEND": "#498DB8", # Light blue
        | "COLOR": "#C2AF3A", # Yellow
        | "DISTORT": "#6B8B8B", # Blue-Grey
        | "OUTPUT": "#B33641", # Red
        | "DEFAULT": "#975B5B" # Burgendy

        :returns: a string
        """
        return "DEFAULT"

    @property 
    def NodeOutputType(self):
        """ The type of data the node outputs. This can be one of the 
        following data types:

        Data type | Description

        | "RENDERIMAGE": will output a ``RenderImage`` object instance

        :returns: a string
        """
        return "RENDERIMAGE"

    @property
    def NodeProperties(self):
        """ List of node properties for the node. These will translate 
        into properties in the Node Properties Panel. You must also setup
        the widgets in ``NodePropertiesUI`` in order for end-users to
        change the values.

        :returns: a list of ``Property`` objects (for internal use)
        """
        return [] 

    @property
    def NodeParameters(self):
        """ List of node parameters for the node. These will translate 
        into plugs on the node itself.

        :returns: a list of ``Parameter`` objects (for internal use)
        """
        return []
 
    def NodePropertiesUI(self, node, parent, sizer):
        """ Defines the UI for the Node Property Panel when this node
        is selected. Widgets should be provided for all Properties the
        end-user will be able to change.
        
        wxPython widgets are to be used normally as children of the ``parent`` 
        variable and added to the ``sizer`` variable:

        .. code-block:: python

            import wx
            example_lbl = wx.StaticText(parent, label="Example:")
            sizer.Add(example_lbl, flag=wx.ALL, border=5)

        :param node: ``Node`` object of the currently selected node. Also accessible from ``self.Node``.
        :param parent: parent wxPython panel of the Node Property Panel
        :param sizer: main wxPython sizer of the Node Property Panel
        """
        pass

    def NodeEvaluation(self, eval_info):
        """ This is the method that is called during rendering 
        of the image. This should contain the actual code which does
        something to the data type (e.g: blurs the image, RENDERIMAGE data type)
        and should return it as that same data type.

        :param eval_info: object exposing methods to get evaluated ``Parameter`` and ``Property`` values to use for evaluating this node.
        :returns: the same data type as specified by ``NodeOutputType``
        """
        pass

    # Convienience methods
    def NodePropertiesUpdate(self, prop_name, value):
        """ Updates the node property to be the specified value. This
        also refreshes the Node Graph and renders the current image. 

        :param str prop_name: name of the node Property to update
        :param value: value to change the Property value to
        """
        self.Node.EditProperties(prop_name, value)
        self.Node.GetParent().RefreshGraph()
        self.Node.GetParent().GetParent().Render() 

    def NodeSetThumb(self, image, force_redraw=False):
        """ Set the image thumbnail of the node. No editing needs to
        be done to the image before calling this method as the 
        thumbnail is resized internally as needed.

        :param image: node thumbnail as ``PIL Image`` object
        :param force_redraw: boolean value of whether to force a redraw of the node right away rather than waiting until a render show the updated node thumb.
        """
        self.Node.UpdateThumbImage(image)

        if force_redraw == True:
            self.Node.Draw(self.Node.GetParent().GetPDC(), use_cache=False)
            self.Node.GetParent().RefreshGraph()
        

    def NodeGetPropValue(self, name):
        """ Get the current value of this node's property.

        :param name: Name of the property of which to get the value for
        :returns: the value of the node property, if it exists
        """
        try:
            for i in range (0, len(self.Node.GetEvaluationData()["properties"])):
                if self.Node.GetEvaluationData()["properties"][i]["name"] == name:
                    return self.Node.GetEvaluationData()["properties"][i]["value"]
        except KeyError:
            print("WARNING: The property {} could not be found.".format(name))
        finally:
            pass
