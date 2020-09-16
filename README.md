Gimel Studio
============

Gimel Studio is a **non-destructive, realtime image graphics editing software program** for Windows and Linux.
 
!["Gimel Studio"](/screenshots/gimel-studio-v0.4.2-pre-release-ui.JPG?raw=true "Gimel Studio")


# Introduction

Gimel Studio has a node-based workflow for realtime compositing, manipulating, generating and adding effects to images -complete with a registry of 20+ nodes and an API allowing users to script their own custom nodes in Python.

It provides basic image editing features such as rotate, resize and blur effects, as well as more advanced editing capabilities such as generating PBR maps for use in 3D from image textures.

*Still in BETA stage, but can be considered stable enough for light production work.*


# News

See the <a href="https://correctsyntax.com/blog/">Correct Syntax blog</a> for news and updates on releases.


# Development 

**Help develop Gimel Studio**

Pull requests and/or feature suggestions are welcome!

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidlines. Also see [ROADMAP.txt](ROADMAP.txt) for a general idea of the possible future goals of the development of Gimel Studio.


# Features

**Highlights**
  
  * Written in pure Python with minimal dependancies
  * Support for opening and saving your full nodegraph as a GIMEL-STUDIO-PROJECT
  * Features packing images into the project file (meaning project files can be shared between users on different computers and Operating Systems without hassle)
  * 20+ nodes with a wide range of functionality 
  * Node Graph featuring node deletion, duplication, selection, etc. 
  * Node-based workflow (similar to Blender 3D)
  * JPEG, JPG, PNG, BMP, WEBP (and more...) file type support
  * API for scripting custom nodes in Python
  * Dark & Light UI themes w/ wire curving
  * Zoomable Image Viewport for viewing renders in real-time

**Tidbits**

  * Auto-renders as the Node Graph is edited (this is a setting that you can change if you so desire)`
  * Toggle-able thumbnails on nodes showing the steps of the rendered image
  * Rearrangable and resizable panels for the main UI

**And More...**


# Releases

Head to the <a href="https://correctsyntax.com/projects/gimel-studio/">Gimel Studio homepage</a> to download the latest release or <a href="https://github.com/Correct-Syntax/Gimel-Studio/releases">click here</a> to see past releases on Github.


# Documentation

You can find the latest documentation on <a href="https://gimel-studio.readthedocs.io/en/latest/">Read the docs</a> or build it yourself following the steps in the section *Building the documentation from source* below.

Documentation for past Gimel Studio releases can be <a href="https://github.com/Correct-Syntax/Gimel-Studio/releases">here</a>.


# Installing from source

Please see the building from source documentation <a href="https://gimel-studio.readthedocs.io/en/latest/install.html#building-from-source">here</a>.


# Build the development version

The development version of Gimel Studio may be unstable and/or have new dependencies. If you fail to install the development version, please file a bug in Issues -tab.

1. Install Git in your system

2. Use Git to download Gimel Studio into a folder of your choosing by using the git clone command in a terminal or CMD:
  * Clone the repo with ``git clone https://github.com/Correct-Syntax/Gimel-Studio.git``

3. Follow the steps listed in the *Installing from source* section above.


# Building the documentation from source

The Gimel Studio docs use the Sphinx package.
  
  * Get <a href="https://pipenv.pypa.io/en/latest/">pipenv</a>
  * Install development dependancies with ``pipenv install --dev``
  * ``pipenv shell``
  * ``cd docs``
  * Now run ``make html`` to build the docs.

You will find the HTML docs in the ``build`` folder.


# License

Gimel Studio is licensed under the Apache License, Version 2.0. See the LICENSE and NOTICE files for full copyright and license information.
