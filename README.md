!["Gimel Studio"](/screenshots/gimel-studio-ui-04.jpg?raw=true "Gimel Studio")

Gimel Studio
============

[![Documentation Status](https://readthedocs.org/projects/gimel-studio/badge/?version=latest)](https://gimel-studio.readthedocs.io/en/latest/?badge=latest)
[![GitHub license](https://img.shields.io/github/license/Correct-Syntax/Gimel-Studio?color=light-green)](https://github.com/Correct-Syntax/Gimel-Studio/blob/master/LICENSE)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Correct-Syntax/Gimel-Studio.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Correct-Syntax/Gimel-Studio/context:python)
![Build Gimel Studio](https://github.com/Correct-Syntax/Gimel-Studio/workflows/Build%20Gimel%20Studio/badge.svg)
[![Gitter](https://badges.gitter.im/Gimel-Studio/community.svg)](https://gitter.im/Gimel-Studio/community?utm_source=badge&utm_medium=badge)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/Correct-Syntax/Gimel-Studio/latest?style=flat)


[Website](https://correctsyntax.com/projects/gimel-studio/) | [Downloads](https://correctsyntax.com/projects/gimel-studio/#download) | [Official Manual](https://gimel-studio.readthedocs.io/en/latest/) | [Discord](https://discord.gg/RqwbDrVDpK) | [Community Discussion](https://github.com/Correct-Syntax/Gimel-Studio/discussions)


Gimel Studio is a cross-platform, node-based, non-destructive image editor.

The aim of this project is to provide a non-destructive (and fun!) python-based image editor with a workflow for compositing, masking, manipulating, generating and editing images via both CPU and GPU processing. As a core principle, Gimel Studio has a simple, yet powerful API allowing users to script their own custom nodes (and thus effects, manipulations, etc) in Python and GLSL.

Currently, Gimel Studio provides only basic image editing features such as flip, color balance, brightness, contrast and blur effects, as well as more advanced editing capabilities such as generating PBR maps for use in 3D from image textures.


# Future Plans of this Project

Interested in this project? Have ideas you'd like to share?

We're currently planning the next step of Gimel Studio to make it a truly *usable* and *serious* image editor. This is an exciting step for development which allows us to consider introducing concepts like a layer *and* nodes workflow and vector support. 👍

The next generation of Gimel Studio is happening at https://github.com/GimelStudio/GimelStudio. **No matter your skill-level, you are welcome to join in planning and development!**

See [here](https://github.com/Correct-Syntax/Gimel-Studio/issues/33) for details on this decision. Feel free to contact us with any questions or comments!


# WIP MacOs Support

MacOs binaries are not yet officially available.However, you can see the [building from source](https://gimel-studio.readthedocs.io/en/latest/getting_started/building_from_source.html#macos) documentation to build it from the source code yourself.

**Please note that there are still [known issues](https://github.com/Correct-Syntax/Gimel-Studio/issues/29) with support on MacOs.**


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


# News

[v0.5.2 beta](https://github.com/Correct-Syntax/Gimel-Studio/releases/tag/v0.5.2-beta) is now available.

See the <a href="https://correctsyntax.com/blog/">Correct Syntax blog</a> for news and updates on releases and upcoming features.


# Download Releases

Head to the <a href="https://correctsyntax.com/projects/gimel-studio/">Gimel Studio homepage</a> to download the latest release for Windows and Linux.


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
