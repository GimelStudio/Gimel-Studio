Available Modules
=================

The Gimel Studio executable builds come bundled with a Python 3 environment, complete with some standard-library modules and other open-source libraries for usage with the Gimel Studio Custom Node API.

.. note::
    Other modules could be available depending on your build, but these are the modules that are *guaranteed to be available regardless of the build*.


Standard Library Modules
------------------------

Python standard-library modules that are guaranteed to be available for use from the API:

* ``os`` Full module
* ``sys`` Full module
* ``re`` Full module
* ``io`` Full module


API Libraries
-------------

Other API modules that are guaranteed to be available for use from the API:

* ``Pillow`` Full module
* ``wxPython`` Partial module (Only ``wx``, ``wx.lib`` and ``wx.adv``)
* ``Scipy`` Full module
* ``Numpy`` Full module
* ``OpenCV`` Partial module (FFmpeg support may not exist, etc.)


Example
-------

.. code-block:: python

    import os

    import cv2
    import wx # wx.adv...
    from PIL import Image # ImageOps, ImageDraw...

    from GimelStudio import api

    ...

