!["Gimel Studio"](/screenshots/gimel-studio-ui-05.png?raw=true "Gimel Studio")

Gimel Studio
============

## 🚀 New development is now focused on the 0.6.x series in the [new repository](https://github.com/GimelStudio/GimelStudio). 

The next generation of Gimel Studio is the v0.6.x series. Join us in planning and development!

## ⚠️ This repository is the previous version which will no longer be maintained.


Gimel Studio is a cross-platform, node-based, non-destructive image editor.

The aim of this project is to provide a non-destructive (and fun!) python-based image editor with a workflow for compositing, masking, manipulating, generating and editing images via both CPU and GPU processing. As a core principle, Gimel Studio has a simple, yet powerful API allowing users to script their own custom nodes (and thus effects, manipulations, etc) in Python.

The version in this repository provides only basic image editing features such as flip, color balance, brightness, contrast and blur effects, as well as more advanced editing capabilities such as generating PBR maps for use in 3D from image textures.

**See the [new repository](https://github.com/GimelStudio/GimelStudio) to see more features and keep track of new development.**


# Features

**Highlights**

  * Thumbnail preview on each node showing the steps of the rendered image
  * Fast node-based, non-destructive workflow (similar to Blender 3D)
  * 20+ nodes with a wide range of functionality
  * Node Graph featuring node deletion, duplication, selection, etc.
  * JPEG, JPG, PNG, BMP, WEBP (and more...) file type support
  * API for scripting custom nodes in Python
  * Integration with [Blender](https://blender.org) via the [Blender Gimel Studio addon](https://github.com/Correct-Syntax/Blender-Gimel-Studio-Addon)
  * Dark theme w/ wire curving
  * Rearrangable and resizable panels for the main UI
  * Zoomable Image Viewport for viewing rendered image result
  * Auto-renders as the Node Graph is edited (this is a setting that you can change if you so desire)

**And More...**


# Installing from source

Please see the building from source documentation <a href="https://gimel-studio.readthedocs.io/en/latest/getting_started/building_from_source.html">here</a>. Please open a [Github Issue](https://github.com/Correct-Syntax/Gimel-Studio/issues/new/choose) if you have problems building from source.


# Building the documentation from source

The Gimel Studio docs use the Sphinx package.

  * ``pip install -r docs/requirements.txt``
  * ``cd docs``
  * Now run ``make html`` to build the docs.

You will find the HTML docs in the ``build`` folder.


# License

Gimel Studio is licensed under the Apache License, Version 2.0. See the LICENSE and NOTICE files for full copyright and license information.
