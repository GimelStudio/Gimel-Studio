Gimel Studio API
================

The Gimel Studio API allows you to script your own custom nodes for Gimel Studio in Python.

.. note::
    **New API Docs are yet to be written.** Please see the `example_custom_node.py` file in the customnodes directory for an example of the new API.

    Also see the *corenodes* directory in the source of Gimel Studio to see how the corenodes included in Gimel Studio are written.


Overview of the API
###################

The Gimel Studio API is created with flexibility in mind and offers a lot of control for those who are willing to "get their hands dirty" and simplicity for those who just want to go ahead and create a node.

The API is based on popular open-source libraries:

* Pillow, the friendly fork of PIL
* WxPython (though most nodes can be written *without any knowledge of wxPython* as writing wxPython code is not required except when creating a new Property.)

with the option to use `Numpy`, `Scipy` and `OpenCV` as well for your own custom-optimized manipulation, effects, etc.

The Gimel Studio API itself is quite small. Thus, the majority of the learning is learning to use these libraries in Gimel Studio to create a node. If you already have experience with these, learning the Gimel Studio API is even more simple!

.. note::

    All API classes, methods and functions should be imported from the ``GimelStudio.api`` module. **This is the only "safe" way to access the internal API.**


Note on Python Versions
#######################

The Gimel Studio application comes bundled with Python 3, but specific versions may vary depending on the build and target OS:

| (Current builds)
| Linux 64-bit - Python 3.8
| Windows 64-bit - Python 3.8

If you built Gimel Studio from the source yourself, be sure that you used a Python version higher that 3.6. Gimel Studio is developed for Python 3.6+ and stability cannot be guaranteed with earlier versions. Please take this into account when developing custom nodes also.


Examples of Creating Nodes
##########################

The best place to start for learning to create nodes with the Gimel Studio API is the **corenodes** directory in the source of Gimel Studio.

`Gimel Studio Github repo <https://github.com/Correct-Syntax/Gimel-Studio>`_
