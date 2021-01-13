####################
Building From Source
####################

This part of the documentation shows how to build Gimel Studio from source.


Download Release Builds
=======================

Binary package builds for Windows and Linux can be downloaded from the  `Gimel Studio homepage`_.

MacOs binaries are not yet available. See the building from source documentation to build it from the source code yourself.

.. _Gimel Studio homepage: https://correctsyntax.com/projects/gimel-studio/

.. note::
    It is likely that the *binary packages* for Linux (available for download on the website) only supports Ubuntu 20.04.1 LTS/Linux Mint 20 and onwards.

    **Building from source should work on any system that supports Python 3.6+**


Building from Source
====================

Gimel Studio is currently written in 100% pure Python, so there shouldn't be any need to compile anything except for the dependencies (in some cases).

**Step 1. Get the source**
  * Download the tar.gz source archive file from `the Github Releases`_
  * Extract the archive.
  * Navigate to the root directory (the folder called `Gimel-Studio`) in your shell/bash/command prompt ``cd Gimel-Studio``.

.. note::
    The following steps assume you have **Python 3.6 or higher** (added to your PATH), **pip** installed on your system and you are in the **root directory** of Gimel Studio.


Windows
-------

**Step 2. Setup and install dependancies**
  * Get pipenv with ``pip install pipenv``
  * Install the dependencies with ``pipenv install --dev``

  This will install the core dependancies for Gimel Studio.

**Step 3. Build the executable**
  * Launch the pipenv shell with ``pipenv shell``
  * Run ``python "src/main.py"`` to test if you have installed everything correctly. If this launches Gimel Studio, then you are ready to build the executable.
  * Next, run ``make.bat`` to build the executable. You should find the executable in the *dist* folder.


Linux (Debian-based systems)
----------------------------

**Step 2. Setup and install dependancies**
  * Get pipenv with ``pip3 install pipenv``
  * Install the dependencies with ``pipenv install --dev``

  This will install the core dependancies for Gimel Studio.

.. note::
    If the above does not work for you, you can try the following alternative dependency installation:

    1. Run each of these commands:
    ``pip3 install opencv-python``
    ``pip3 install numpy``
    ``pip3 install scipy``
    ``pip3 install pillow``

    2. Download the wheel file for wxpython which matches your Python version and Linux OS version from https://extras.wxpython.org/wxPython4/extras/linux/

    3. Install the wxpython package with ``pip3 install <pathtothewheelfilehere>``


**Step 3. Build the executable**
  * Launch the pipenv shell with ``pipenv shell`` (only if you did not use the alternative dependency installation)
  * Run ``python3 "src/main.py"`` to test if you have installed everything correctly. If this launches Gimel Studio, then you are ready to build the executable.
  * Next, run ``./make`` or ``sudo ./make`` to build the executable. You should find the executable in the *dist* folder.


MacOs
-----

.. warning::

  **This part of the documentation is still WIP. These instructions may or may not work correctly! :)**

  *TODO: Confirm that these are the correct steps for building on MacOs.*


**Step 2. Setup and install dependancies**
  * Get pipenv with ``pip3 install pipenv``
  * Install the dependencies with ``pipenv install --dev``

  This will install the core dependancies for Gimel Studio.


**Step 3. Build the executable**
  * Launch the pipenv shell with ``pipenv shell``
  * Run ``python3 "src/main.py"`` to test if you have installed everything correctly. If this launches Gimel Studio, then you are ready to build the executable.
  * Next, run ``./make`` or ``sudo ./make`` to build the executable. You should find the executable in the *dist* folder.


.. _the Github Releases: https://github.com/Correct-Syntax/Gimel-Studio/releases
