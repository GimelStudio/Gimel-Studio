Available Modules
=================

The Gimel Studio executable comes bundled with a Python 3 enviroment, complete with some standard-library modules and other open-source libraries for usage with the Gimel Studio Custom Node API.


Standard Library Modules
------------------------

Python standard-library modules that are guaranteed to be available for use from the API:

* ``os`` Full module
* ``sys`` Full module
* ``re`` Full module
* ``io`` Full module
* ``collections`` Full module


API Libraries
-------------

Other API modules that are guaranteed to be available for use from the API:

* ``Pillow`` Full module
* ``wxPython`` Partial module (Only ``wx`` and ``wx.adv``)
* ``Scipy`` Full module
* ``Numpy`` Full module
    

Example
-------

.. code-block:: python

    import os

    import wx # wx.adv...
    from PIL import Image # ImageOps, ImageDraw...

    from GimelStudio.api import NodeBase, RegisterNode # List, RenderImage...
    
    ...

