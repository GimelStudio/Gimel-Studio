Installing Gimel Studio
=======================

This part of the documentation shows how to build Gimel Studio from source.


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


.. note::
    Feel free to submit a Github pull request with a system you've tested Gimel Studio on in the above list.


Download Release Builds
-----------------------

Executable builds for Windows and Linux can be downloaded from the  `Gimel Studio homepage`_.

.. _Gimel Studio homepage: https://correctsyntax.com/projects/gimel-studio/

.. warning::
    It is likely that the *built executable* (available for download on the website) only supports Ubuntu 20.04.1 LTS/Linux Mint 20 and onwards.

    *Building from source* should work on any system that supports Python 3.6+


Building from Source
--------------------

Gimel Studio is currently written in pure Python, so there shouldn't be any need to compile anything except for the dependancies (in some cases).

**Step 1. Get the source**
  * Download the tar.gz source archive file from `the Github Releases`_
  * Extract the archive.
  * Navigate to the root directory (the folder called `Gimel-Studio`) in your shell/bash/command prompt.

.. note::
    The following steps assume you have **Python 3.6 or higher** and **pip** installed on your system and you are in the **root directory** of Gimel Studio.

Windows
^^^^^^^

**Step 2. Setup and install dependancies**
  * Get pipenv with ``pip install pipenv``
  * Install the dependencies with ``pipenv install --dev``

  This will install the core dependancies for Gimel Studio.

**Step 3. Build the executable**
  * Run ``python "src/Gimel Studio.py"`` to test if you have installed everything correctly. If this launches Gimel Studio, then you are ready to build the executable.
  * Next, run ``make.bat`` to build the executable. You should find the executable in the *dist* folder.


Linux (Debian-based systems)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Step 2. Setup and install dependancies**
  * Get pipenv with ``pip3 install pipenv``
  * Install the dependencies with ``pipenv install --dev``

  This will install the core dependancies for Gimel Studio.

.. note::
    If the above does not work for you, you can try the following alternative dependancy installation:

    1. Run each of these commands:
    ``pip3 install opencv-python``
    ``pip3 install numpy``
    ``pip3 install scipy``
    ``pip3 install pillow``

    2. Download the wheel file for wxpython which matches your Python version and Linux OS version from https://extras.wxpython.org/wxPython4/extras/linux/

    3. Install the wxpython package with ``pip3 install <pathtothewheelfilehere>``


**Step 3. Build the executable**
  * Run ``python3 "src/Gimel Studio.py"`` to test if you have installed everything correctly. If this launches Gimel Studio, then you are ready to build the executable.
  * Next, run ``./make`` or ``sudo ./make`` to build the executable. You should find the executable in the *dist* folder.


.. _the Github Releases: https://github.com/Correct-Syntax/Gimel-Studio/releases


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

