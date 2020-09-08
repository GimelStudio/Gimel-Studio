Gimel Studio Usage
==================

This part of the documentation shows basic installation and usage of Gimel Studio.


Download Release Builds
-----------------------

Executable builds for Windows and Linux can be downloaded from the  `Gimel Studio homepage`_.

.. _Gimel Studio homepage: https://correctsyntax.com/projects/gimel-studio/


Building from Source
--------------------
 
Please see the README in the `Github repository`_ for information on bulding from source.

.. _Github repository: https://github.com/Correct-Syntax/Gimel-Studio


System Support
--------------

Gimel Studio has been tested to run the following systems:

Windows
^^^^^^^

* Windows 10 (64-bit)
* Apparently, it also runs on Windows 7 and 8 (64-bit) as well.

 
Linux
^^^^^

* Linux Mint 20 (64-bit)

.. warning::
    It is likely that the *built executable* (available for download on the website) only supports Ubuntu 20.04.1 LTS/Linux Mint 20 and onwards. 
    
    *Building from source* should work on any system that supports Python 3.6+

.. note::
    Feel free to submit a Github pull request with a system you've tested Gimel Studio on in the above list.


Launching the Application
-------------------------

Windows
^^^^^^^

1. Copy the downloaded zip file into the desired folder on your system and unzip it. 
2. Find the 'Gimel Studio' executable file.

Double-click on the executable file to launch Gimel Studio.


Linux
^^^^^

1. Copy the downloaded compressed file into the desired folder on your system and uncompress in the same directory. 
2. Find the 'Gimel Studio' executable file and right-click it to bring up the context menu. 
3. Click *Properties* and navigate to the *Permissions* tab. 
4. Under *Execute*, check the *Allow executing file* as program checkbox. 

You should now be able to double-click on the executable file to launch Gimel Studio.


Gimel Studio Panels
-------------------

Gimel Studio's UI is made up of rearrangable (dockable) and resizeable panels.


Image Viewport
^^^^^^^^^^^^^^

This panel is where the final result, the rendered "composite" image, will be shown. The image preview will be auto-updated each time a change is made to the Node tree in the Node Graph, if you have the *Auto Render* setting checkbox ticked in User Preferences (File > User Preferences).


Node Graph
^^^^^^^^^^

The Node Graph panel is where you add and connect nodes, etc. to create a node tree. Nodes are connected in the desired order to produce a rendered "composite" image with the effects and manipulations applied.


Node Properties
^^^^^^^^^^^^^^^

The Node Properties panel is where the properties of the node selected in the Node Graph are displayed, if any.


Node Registry
^^^^^^^^^^^^^

NOTE: This was removed (for the moment) in v0.3.0 and v0.4.0.

The Node Registry Panel lists the registered Gimel Studio nodes available for usage in the Node Graph (both the core nodes and any registered custom nodes will be shown) 

All of the available nodes are listed in the Node Registry, including any custom nodes. Select an item in the list in the Node Registry to make it active. CTRL+LMB the Node Graph to add the active item node to the Node Graph at the location of the mouse pointer.


