Gimel Studio API
================

The Gimel Studio API allows you to script your own custom nodes for Gimel Studio in Python.


Getting Setup To Script A Custom Node
-------------------------------------

Before starting to use the Gimel Studio API to script a custom node, you need to gain some knowledge of how to get setup.


Overview Of The API 
^^^^^^^^^^^^^^^^^^^

Gimel Studio API


Understand The Directory Structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Within the directory of the Gimel Studio Program is a folder called **customnodes**. This directory is where you will place any custom node scripts you want to be found by Gimel Studio.

In this folder you will find an example Python script for an "Example Custom Node" which illustrates how to script and register a NodeDefinition class to create a custom node. The *example_custom_node.py* contents should look similar to the following code:

.. code-block::

    import os
    from PIL import Image

    from GimelStudio.api import (Color, RenderImage, NodeBase,
                             ParameterDefinition, PropertyDefinition,
                             RegisterNode)


    class NodeDefinition(NodeBase):

        @property
        def NodeName(self):
            return "example custom node"

        @property
        def NodeLabel(self):
            return "Example Custom Node"

        @property
        def NodeCategory(self):
            return "INPUT"

        @property
        def NodeDescription(self):
            return "[description]" 

        @property
        def NodeVersion(self):
            return "1.0.0" 

        @property
        def NodeAuthor(self):
            return "[author's name]"

        @property
        def NodeProperties(self): 
            return [
                PropertyDefinition('path',
                                   prop_type='filepath',
                                   value=''
                                   ),
            ]

        def NodePropertiesUI(self, node, ui, parent, sizer):
            self.NodePropertiesHelperInit(node, ui, parent, sizer)
            current_value = self.NodeGetPropertyValue('path')

            pathlabel = ui.StaticText(parent, label="Path:")
            sizer.Add(pathlabel, pos=(2, 0), flag=ui.LEFT|ui.TOP, border=10)

            self.pathtxtctrl = ui.TextCtrl(parent)
            sizer.Add(self.pathtxtctrl, pos=(2, 1), span=(1, 3), flag=ui.TOP|ui.EXPAND, border=5)
            self.pathtxtctrl.ChangeValue(current_value)

            self.browsepathbtn = ui.Button(parent, label="Browse...")
            sizer.Add(self.browsepathbtn, pos=(2, 4), flag=ui.TOP|ui.RIGHT, border=5)

            parent.Bind(ui.EVT_BUTTON, self.OnFilePathButton, self.browsepathbtn)

        def OnFilePathButton(self, evt):
            wildcard = "JPG file (*.jpg)|*.jpg|" \
                       "PNG file (*.png)|*.png|" \
                       "All files (*.*)|*.*"

            dlg = self.ui.FileDialog(
                self.parent, message="Choose an Image",
                defaultDir=os.getcwd(),
                defaultFile="",
                wildcard=wildcard,
                style=self.ui.FD_OPEN | self.ui.FD_CHANGE_DIR | self.ui.FD_FILE_MUST_EXIST | self.ui.FD_PREVIEW
                )

            # Show the dialog and retrieve the user response. If it is the OK response,
            # process the data.
            if dlg.ShowModal() == self.ui.ID_OK:
                # This returns a Python list of files that were selected.
                paths = dlg.GetPaths()
                self.NodePropertiesUpdate('path', paths[0])
                self.pathtxtctrl.ChangeValue(paths[0])

        def NodeEvaluation(self, eval_info):
            path = eval_info.EvaluateProperty('path')
            image = RenderImage()
            if path != '':
                image.SetAsOpenedImage(path)
            image.SetAsImage(image.GetImage().convert('RGBA'))
            self.NodeSetThumbnail(image.GetImage())
            return image 



    RegisterNode(NodeDefinition)
    
This is a basic custom node which inputs an image from a filepath (similar to the Image node). We will walk through this example in the section "Using The API To Script A Custom Node" below.

You should also see a *__init__.py* file with the following contents:

.. code-block::

    # Gimel Studio - (Custom Nodes)

    # Add the filename (without the .py extenstion) to the below list to make
    # your custom node(s) available for registering.

    __all__ = ['example_custom_node']



Create The File
^^^^^^^^^^^^^^^
The first step to setup to create a custom node is to create the file. Create a new Python file (.py) in the **customnodes** directory and name it according to what the name of your custom node will be.

.. note::

    Please note that the *Name* of the Python file is important and should be named as "YOUR_NODE_NAME_HERE_node".
    
    
Edit The Custom Nodes List
^^^^^^^^^^^^^^^^^^^^^^^^^^
Next, open the *__init__.py* file in the **customnodes** directory. *Add the name of your custom node file (which you created in the "Create The File" section above) without the ".py" extension* to the ``__all__`` list. 

(This will allow the Gimel Studio node importer to find your custom node file and register and load it into the program.)

Then, open your custom node file in the code editor of your choice and you're all setup to start scripting your custom node with the Gimel Studio API!


Using The API To Script A Custom Node
-------------------------------------

Now that we're setup, let's start using the Gimel Studio API to create a custom node.

Starting With Imports
^^^^^^^^^^^^^^^^^^^^^

To script a custom node, we start with some imports:

.. code-block::

    import os
    from PIL import Image
                             
Start by importing any of the available outside API modules. In this case, we need to import ``os`` and ``PIL``. 

.. seealso::
    See the *API Reference* for a list of the available outside API modules. 

.. note::

    ``PIL, numpy`` and ``scipy`` provide the core API for manipulating the graphics in your custom node.

Next, import the neccessary classes from the GimelStudio API. For this node, we need ``Color, RenderImage, NodeBase, ParameterDefinition, PropertyDefinition`` and ``RegisterNode``. 

.. code-block::

    from GimelStudio import (Color, RenderImage, NodeBase,
                             ParameterDefinition, PropertyDefinition,
                             RegisterNode)

.. note::
    Classes from the Gimel Studio API provide a fairly high-level way to define how the node works, what properties it has and also gives us some "helper" methods to make it easier.


Making The NodeDefinition Class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Make a class that inherits from ``NodeBase``. By convention, this is called ``NodeDefinition``. Inside this class, we write methods which override the default ``NodeBase`` methods to define our custom node.

.. code-block::

        class NodeDefinition(NodeBase):


Defining The Node's Meta Methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the ``NodeDefinition`` class we write a property method (``NodeName``) to define the name of the node (think of it as a unique ID for this node). This string *must be unique and not used by any other node in the node registry*. It is conventional to have this in all lower-case.

We write another property method (``NodeLabel``) to define the label of the node that will be seen by the user. It is conventional to have this in title-case.

Yet again, in the ``NodeDefinition`` class, we write a property method (``NodeCategory``) to define the category the node will be placed in (for menus, node registry, etc.). The string must be in all upper-case.

.. seealso::
    See the *API Reference* for a list of valid strings for the ``NodeCategory`` method. 

Write a property method (``NodeDescription``) to define a short description of the node that will be seen by the user in the node registry. It is conventional to have this in sentence-case with less than 20 words.

.. code-block::

            @property
            def NodeName(self):
                return "example custom node"

            @property
            def NodeLabel(self):
                return "Example Custom Node"
                
            @property
            def NodeCategory(self):
                return "INPUT"

            @property
            def NodeDescription(self):
                return "[description]" 
                
                
                
Next, write a ``NodeVersion`` method which will show the user (in the node registry) what version of the node they are using. It is conventional to have this version string as [major].[minor].[release].

Finally, write a ``NodeAuthor`` method which shows the user (in the node registry) who scripted/authored the node. (So, put your name there!) 

.. code-block::

            @property
            def NodeVersion(self):
                return "1.0.0"

            @property
            def NodeAuthor(self):
                return "[author's name]"

We have now defined the custom node's meta information. However, that isn't good enough because if you registered it as-is, it wouldn't actually do anything. 


Creating Node Properties
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::

        @property
        def NodeProperties(self): 
            return [
                PropertyDefinition('path',
                                   prop_type='filepath',
                                   value=''
                                   ),
            ]



Creating Node Parameters
^^^^^^^^^^^^^^^^^^^^^^^^

TODO: CHANGE NODE EXAMPLE TO USE PARAMS




