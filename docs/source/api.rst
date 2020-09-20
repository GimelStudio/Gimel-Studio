Gimel Studio API
================

The Gimel Studio API allows you to script your own custom nodes for Gimel Studio in Python.

.. warning::
    **New API Docs are yet to be written.** Most of the following API docs are depreciated in v0.5.0 and onward. Please see the `example_custom_node.py` file in the customnodes directory for an example of the new API.


Overview of the API 
###################

The Gimel Studio API is created with flexibility in mind and offers a lot of control for those who are willing to "get their hands dirty" and simplicity for those who just want to go ahead and create a node.

The API is based on 2 popular, open-source libraries: 

* Pillow, the friendly fork of PIL
* WxPython

with the option to use both `Numpy` and `Scipy` as well for your own custom-optimized manipulation, effects, etc.

The Gimel Studio API itself is quite small. Thus, the majority of the learning is learning to use these libraries in Gimel Studio to create a node. If you already have experience with these, learning the Gimel Studio API is even more simple.

.. note::

    All API classes, methods and functions should be imported from the ``GimelStudio.api`` module. 
    This is the only "safe" way to access the internal API.


Note on Python Versions
#######################

The Gimel Studio application comes bundled with Python 3, but specific versions may vary depending on the build and target OS:

| (Current builds)
| Linux 64-bit - Python 3.8
| Windows 64-bit - Python 3.8

If you built Gimel Studio from the source yourself, be sure that you used a Python version higher that 3.6. Gimel Studio is developed for Python 3.6+ and stability cannot be guaranteed with earlier versions. Please take this into account when developing custom nodes also.


First Steps: Input Node Tutorial
################################

This is a tutorial to create a simple, custom Input Node usng the Gimel Studio API. It gives first steps in creating custom nodes and shows some of the core API concepts. The example node we will be creating is a simplified version of the Image Core Node in Gimel Studio and is an easy way to get going creating a custom node (it can be used as a template).


Getting Setup to Script a Custom Node
-------------------------------------

Before starting to use the Gimel Studio API to script a custom node, you need to gain some knowledge of how to get setup.


Understand Directory Structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Within the directory of the Gimel Studio Program is a folder called **customnodes**. This directory is where you will place any custom node scripts you want to be found by Gimel Studio.

In this folder you will find an example Python script for an "Example Custom Node" which illustrates how to script and register a NodeDefinition class to create a custom node. The *example_custom_node.py* contents should look similar to the following code:

.. code-block:: python

    import os

    import wx
    from PIL import Image

    from GimelStudio.api import (Color, RenderImage, NodeBase,
                                Parameter, Property,
                                RegisterNode)

    
    class NodeDefinition(NodeBase):
        
        @property
        def NodeIDName(self):
            return "example_custom_node"

        @property
        def NodeLabel(self):
            return "Example Custom Node"

        @property
        def NodeCategory(self):
            return "INPUT"

        @property
        def NodeDescription(self):
            return "This is an example custom node showing how you can\n create a custom node with the Gimel Studio API" 

        @property
        def NodeVersion(self):
            return "1.1" 

        @property
        def NodeAuthor(self):
            return "[author's name]"

        @property
        def NodeProperties(self): 
            return [
                Property('Path',
                    prop_type='FILEPATH',
                    value=''
                    ),
            ]

        def NodePropertiesUI(self, node, parent, sizer):
            self.parent = parent
            
            current_value = self.NodeGetPropValue('Path')
    
            pathlabel = wx.StaticText(parent, label="Path:")
            sizer.Add(pathlabel, flag=wx.LEFT|wx.TOP, border=5)

            vbox = wx.BoxSizer(wx.VERTICAL)
            hbox = wx.BoxSizer(wx.HORIZONTAL)

            self.pathtxtctrl = wx.TextCtrl(parent)
            self.pathtxtctrl.ChangeValue(current_value)
            hbox.Add(self.pathtxtctrl, proportion=1)
            self.browsepathbtn = wx.Button(parent, label="Browse...")
            hbox.Add(self.browsepathbtn, flag=wx.LEFT, border=5)
            vbox.Add(hbox, flag=wx.EXPAND)

            sizer.Add(vbox, flag=wx.ALL|wx.EXPAND, border=5)

            parent.Bind(wx.EVT_BUTTON, self.OnFilePathButton, self.browsepathbtn)

        def OnFilePathButton(self, evt):
            # We allow opening only .jpg files here (for fun!)
            wildcard = "JPG file (*.jpg)|*.jpg|"
                    
            dlg = wx.FileDialog(
                self.parent, message="Choose an Image...",
                defaultDir=os.getcwd(),
                defaultFile="",
                wildcard=wildcard,
                style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW
                )

            # Show the dialog and retrieve the user response. If it is the OK response,
            # process the data.
            if dlg.ShowModal() == wx.ID_OK:
                # This returns a Python list of files that were selected.
                paths = dlg.GetPaths()

                # Update the property and txtctrl with the new file path
                self.NodePropertiesUpdate('Path', paths[0])
                self.pathtxtctrl.ChangeValue(paths[0])

        def NodeEvaluation(self, eval_info):
            # Get the file path from the property
            path = eval_info.EvaluateProperty('Path')

            image = RenderImage()
            if path != '':
                image.SetAsOpenedImage(path)
            image.SetAsImage(image.GetImage().convert('RGBA'))
            self.NodeSetThumb(image.GetImage())
            return image 


    RegisterNode(NodeDefinition)
    
This is a basic custom node which inputs an image from a filepath (similar to the Image node).

You should also see a *__init__.py* file with the following contents:

.. code-block:: python

    # Gimel Studio - (Custom Nodes)

    # Add the filename (without the .py extenstion) to the below list to make
    # your custom node(s) available for registering.

    __all__ = ['example_custom_node']


.. _create-the-file:

1. Create the File
^^^^^^^^^^^^^^^^^^
The first step to setup to create a custom node is to create the file. Create a new Python file (.py) in the **customnodes** directory and name it according to what the name of your custom node will be.

.. note::

    Please note that the *Name* of the Python file is important and should be named as "YOUR_NODE_NAME_HERE_node".
    

.. _edit-custom-node-list:

2. Edit the Custom Nodes List
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Next, open the *__init__.py* file in the **customnodes** directory. *Add the name of your custom node file (which you created in the "Create The File" section above) without the ".py" extension* to the ``__all__`` list. 

(This will allow the Gimel Studio node importer to find your custom node file and register and load it into the program.)

Then, open your custom node file in the code editor of your choice and you're all setup to start scripting your custom node with the Gimel Studio API!


Using the API to Script a Custom Node
-------------------------------------

Now that we're setup, let's start using the Gimel Studio API to create a custom node.

3. Starting with Imports
^^^^^^^^^^^^^^^^^^^^^^^^

To script a custom node, we start with some imports:

.. code-block:: python
    
    # from the standard library
    import os 
    
    # bundled with Gimel Studio
    import wx
    from PIL import Image
                             
Start by importing any of the available outside API modules. In this case, we need to import ``os`` from the standard library and ``wx`` (wxPython) and ``PIL`` (Pillow). 

.. seealso::

    See the :ref:`api-reference-docs`. for a list of the available outside API modules. 

.. note::

    ``PIL``, ``numpy`` and ``scipy`` provide the core API for manipulating the graphics in your custom node. In this example we keep it simple with just using ``PIL``.

Next, import the neccessary classes from the GimelStudio API. For this node, we need ``Color, RenderImage, NodeBase, Parameter, Property,`` and ``RegisterNode``. 

.. code-block:: python

    from GimelStudio.api import (Color, RenderImage, NodeBase,
                                Parameter, Property,
                                RegisterNode)

.. note::

    Classes from the Gimel Studio API provide a fairly high-level way to define how the node works, what properties it has and also gives us some "helper" methods to make it easier.


4. Making the NodeDefinition Class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Make a class that inherits from ``NodeBase``. By convention, this is called ``NodeDefinition``, but it can be any valid class name you want. 

Inside this class, we write the methods which override the default ``NodeBase`` methods which define the properties for our custom node.

.. code-block:: python

        class NodeDefinition(NodeBase):


5. Defining the Node's Meta Methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the ``NodeDefinition`` class we write a property method (``NodeIDName``) to define the name of the node (think of it as a unique ID for this node). This string *must be unique and not used by any other node in the node registry*. It is conventional to have this in all lower-case separated by underscores.

We write another property method (``NodeLabel``) to define the label of the node that will be seen by the user. It is conventional to have this in title-case.

In the ``NodeDefinition`` class, we write a property method (``NodeCategory``) to define the category the node will be placed in (for menus, node registry, etc.). The string must be in all upper-case. 

We will put ``"INPUT"`` for the catgory since we are creating an image input node.

.. seealso::

    See the *API Reference* for a list of valid strings for the ``NodeCategory`` method. 

Write a property method (``NodeDescription``) to define a short description of the node that will be seen by the user in the node registry. It is conventional to have this in sentence-case with less than 20 words.

.. code-block:: python

            @property
            def NodeIDName(self):
                return "simple_input_node"

            @property
            def NodeLabel(self):
                return "Simple Input"
                
            @property
            def NodeCategory(self):
                return "INPUT"

            @property
            def NodeDescription(self):
                return "This is a fun description for the simple imput node which inputs an image." 
                
                
                
Next, write a ``NodeVersion`` method which will show the user (in the node registry) what version of the node they are using. It is conventional to have this version string as [major].[minor].

Finally, write a ``NodeAuthor`` method which shows the user (in the node registry) who scripted/authored the node. (So, put your name there!) 

.. code-block:: python

            @property
            def NodeVersion(self):
                return "1.0"

            @property
            def NodeAuthor(self):
                return "Your Name!"

We have now defined the custom node's meta information. However, that isn't good enough because if you registered it as-is, it wouldn't actually *do* anything. 

.. figure:: _images/simple_input_node.png
    :align: center

    Our node so far -if you went ahead and registered it.


6. Creating the Node Properties
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now we start using the API to declare the data we want to handle. 

We write a ``NodeProperties`` method and return a list of ``Property`` objects. Properties, created via the ``Property`` class, hold the data so that we can set, update and get the data at any time within the API.

.. code-block:: python

        @property
        def NodeProperties(self): 
            return [
                Property('Path',
                    prop_type='FILEPATH',
                    value=''
                    ),
            ]

The ``Property`` object has three parameters:

1) the name (label and id) of the property
2) the data type this property will handle
3) the intial value of the property

In this case we call the property name param ``"Path"`` (this is also used as the id internally and in the API which we will use later). We want to have users choose an image and we need to get the filepath to load it, so we will use ``"FILEPATH"`` as the ``prop_type`` param. The intial value (param ``value``) we set to be blank as we expect the user to choose an image filepath themselves via the Node Properties Panel.


7. Creating the Node Property Panel UI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Next, we create the widgets for the Node Property Panel to allow users to change values for our node. The widgets are used directly from wxPython in a special method, ``NodePropertiesUI``. 

In our case, we are going to create a text control widget and a browse button with a file dialog to allow users to select the image our node will input.

Here is the code:

.. code-block:: python

        def NodePropertiesUI(self, node, parent, sizer):
            self.parent = parent
            
            # Get the current value of the property
            current_value = self.NodeGetPropValue('Path')
    
            # wxPython stuff...
            pathlabel = wx.StaticText(parent, label="Path:")
            sizer.Add(pathlabel, flag=wx.LEFT|wx.TOP, border=5)

            vbox = wx.BoxSizer(wx.VERTICAL)
            hbox = wx.BoxSizer(wx.HORIZONTAL)

            self.pathtxtctrl = wx.TextCtrl(parent)
            self.pathtxtctrl.ChangeValue(current_value)
            hbox.Add(self.pathtxtctrl, proportion=1)
            self.browsepathbtn = wx.Button(parent, label="Browse...")
            hbox.Add(self.browsepathbtn, flag=wx.LEFT, border=5)
            vbox.Add(hbox, flag=wx.EXPAND)

            sizer.Add(vbox, flag=wx.ALL|wx.EXPAND, border=5)

            parent.Bind(wx.EVT_BUTTON, self.OnFilePathButton, self.browsepathbtn)

        # This is specific to this node -it's not required for all custom nodes.
        def OnFilePathButton(self, evt):
            # We allow opening only .jpg files here (for fun!)
            wildcard = "JPG file (*.jpg)|*.jpg|"
                    
            # wxPython stuff here...
            dlg = wx.FileDialog(
                self.parent, message="Choose an Image...",
                defaultDir=os.getcwd(),
                defaultFile="",
                wildcard=wildcard,
                style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW
                )

            # Show the dialog and retrieve the user response. If it is the OK response,
            # process the data.
            if dlg.ShowModal() == wx.ID_OK:
                # This returns a Python list of files that were selected.
                paths = dlg.GetPaths()

                # Update the property and txtctrl with the new file path
                self.NodePropertiesUpdate('Path', paths[0])
                self.pathtxtctrl.ChangeValue(paths[0])


.. figure:: _images/simple_input_node_properties_ui.PNG
    :align: center

    Our completed Node Property panel UI

Of course, at this stage our node **still** doesn't actually *do* anything...so that is our next step.


7. Writing the Node Evaluation Method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            
Now, let's add the functionality of the node. We do so by writing a ``NodeEvaluation`` method which returns the render-image datatype.

.. code-block:: python

    def NodeEvaluation(self, eval_info):
        # Get the file path from the property
        path = eval_info.EvaluateProperty('Path')

        # Create the RenderImage
        image = RenderImage()

        # If the path is blank open the image, otherwise 
        # default to a transparent image.
        if path != '':
            image.SetAsOpenedImage(path)
        image.SetAsImage(image.GetImage().convert('RGBA'))

        # Set the node preview thumbnail
        self.NodeSetThumb(image.GetImage())

        # Return the render-image object
        return image 

Here, we get the file path value ``"Path"`` via the ``eval_info.EvaluateProperty`` method. We create a ``RenderImage`` object using the file path value as the parameter of the ``SetAsOpenedImage`` method -which opens the image for us. We also use ``SetAsImage`` to default to a transparent image when the path is blank (and make sure it is in RGBA mode by converting it with Pillow's ``convert`` method).

The ``RenderImage`` object now holds the opened image, which we get with ``.GetImage()``, set as the node preview thumb with ``self.NodeSetThumb`` and finally, return at the end of the method.


8. Registering the Node
^^^^^^^^^^^^^^^^^^^^^^^

The final step is to register our node in the Node Registry by calling the ``RegisterNode`` function with our custom node class as the only param.

.. note::

    If you have followed this tutorial from the beginning, the *__init__.py* file in the **customnodes** directory should have your node's file name (without the .py extension) listed. If not, please see :ref:`edit-custom-node-list`.

.. code-block:: python

    # Register the node
    RegisterNode(NodeDefinition)


Finished Result
^^^^^^^^^^^^^^^

You can now launch the Gimel Studio Application and you should see the custom node in the *Add Node* menu and/or the Node Registry. Add the node and connect it to the Output node. Click on the simple custom input node and click the browse button in the Node Property panel. It should prompt with a dialog allowing you to choose an image to input.

.. figure:: _images/simple_input_node_finished_result.PNG
    :align: center

    The finished custom input node.

There we have it: a simple, custom input node. Feel free to edit as you like.

Here is the full code for the simple input node:

.. code-block:: python

    import os

    import wx
    from PIL import Image

    from GimelStudio.api import (Color, RenderImage, NodeBase,
                                Parameter, Property,
                                RegisterNode)

    
    class NodeDefinition(NodeBase):
        
        @property
        def NodeIDName(self):
            return "simple_input_node"

        @property
        def NodeLabel(self):
            return "Simple Input"

        @property
        def NodeCategory(self):
            return "INPUT"

        @property
        def NodeDescription(self):
            return "This is a fun description for the simple imput node which inputs an image." 

        @property
        def NodeVersion(self):
            return "1.0" 

        @property
        def NodeAuthor(self):
            return "Your name!"

        @property
        def NodeProperties(self): 
            return [
                Property('Path',
                    prop_type='FILEPATH',
                    value=''
                    ),
            ]

    def NodePropertiesUI(self, node, parent, sizer):
        self.parent = parent

        # Get the current value of the property
        current_value = self.NodeGetPropValue('Path')

        # wxPython stuff...
        pathlabel = wx.StaticText(parent, label="Path:")
        sizer.Add(pathlabel, flag=wx.LEFT|wx.TOP, border=5)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.pathtxtctrl = wx.TextCtrl(parent)
        self.pathtxtctrl.ChangeValue(current_value)
        hbox.Add(self.pathtxtctrl, proportion=1)
        self.browsepathbtn = wx.Button(parent, label="Browse...")
        hbox.Add(self.browsepathbtn, flag=wx.LEFT, border=5)
        vbox.Add(hbox, flag=wx.EXPAND)

        sizer.Add(vbox, flag=wx.ALL|wx.EXPAND, border=5)

        parent.Bind(wx.EVT_BUTTON, self.OnFilePathButton, self.browsepathbtn)

    # This is specific to this node -it's not required for all custom nodes.
    def OnFilePathButton(self, evt):
        # We allow opening only .jpg files here (for fun!)
        wildcard = "JPG file (*.jpg)|*.jpg|"

        # wxPython stuff here...
        dlg = wx.FileDialog(
            self.parent, message="Choose an Image...",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW
            )

        # Show the dialog and retrieve the user response. If it is the OK response,
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            paths = dlg.GetPaths()

            # Update the property and txtctrl with the new file path
            self.NodePropertiesUpdate('Path', paths[0])
            self.pathtxtctrl.ChangeValue(paths[0])

        def NodeEvaluation(self, eval_info):
            # Get the file path from the property
            path = eval_info.EvaluateProperty('Path')

            # Create the RenderImage
            image = RenderImage()

            # If the path is blank open the image, otherwise 
            # default to a transparent image.
            if path != '':
                image.SetAsOpenedImage(path)
            image.SetAsImage(image.GetImage().convert('RGBA'))

            # Set the node preview thumbnail
            self.NodeSetThumb(image.GetImage())

            # Return the render-image object
            return image 

    # Register the node
    RegisterNode(NodeDefinition)



Building Blocks: Filter Node Tutorial
#####################################

If you've followed the above tutorial, you should have the basics of creating a custom node. 

However, you will soon realize that something is missing from the input node: input sockets. Obviously, this is intentional since we were creating a node that inputs an image. We only needed a Property for that. 

Understanding Parameters
------------------------

When creating a node (such as a filter node) that edits the image in some way, we need to have an input socket so that the Image node (or another Input node) can be connected.

In the Gimel Studio API, we use a ``Parameter`` class to define the data we want to hold, just like the ``Property`` we created in the simple input node tutorial above.


Creating the Filter Node
------------------------

This is a tutorial to create a more advanced, custom Filter Node using the Gimel Studio API. It shows how to use ``Parameter`` and ``Property`` objects in creating custom nodes with input sockets and reviews some of the core API concepts.


1. Setup
^^^^^^^^

Again, we setup by creating a new Python file (.py) in the **customnodes** directory and naming it according to what the name of your custom node will be.

Next, we add the name of our custom node file (without the ".py" extension) to the ``__all__`` list in the *__init__.py* file in the **customnodes** directory. 

.. seealso::

    See :ref:`create-the-file` and :ref:`edit-custom-node-list` from the Input Node Tutorial above for a more detailed explanation for setup.


2. Node Imports, Meta, etc.
^^^^^^^^^^^^^^^^^^^^^^^^^^^

In your custom node file (opened in the code editor of your choice), start by writing the imports, meta information, etc. for the node like below:

.. code-block:: python

    import wx
    from PIL import Image, ImageFilter

    from GimelStudio.api import (Color, RenderImage, List, NodeBase, 
                                Parameter, Property, RegisterNode)

    
    class NodeDefinition(NodeBase):
        
        @property
        def NodeIDName(self):
            return "box_blur_node"

        @property
        def NodeLabel(self):
            return "Box Blur"

        @property
        def NodeCategory(self):
            return "FILTER"

        @property
        def NodeDescription(self):
            return "Blurs the given image using the specified blur radius with the Box algorithm." 

        @property
        def NodeVersion(self):
            return "1.0" 

        @property
        def NodeAuthor(self):
            return "Your name!" 





.. note::

    TODO: Finish tutorial


Creating More Advanced Nodes
############################

The best place to start for learning to create more advanced nodes with the Gimel Studio API is the **corenodes** directory in the source of Gimel Studio.

`Gimel Studio Github repo <https://github.com/Correct-Syntax/Gimel-Studio>`_

