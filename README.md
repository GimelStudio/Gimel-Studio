!["Gimel Studio"](/screenshots/gimel-studio-ui-03.jpg?raw=true "Gimel Studio")

Gimel Studio
============

[![Documentation Status](https://readthedocs.org/projects/gimel-studio/badge/?version=latest)](https://gimel-studio.readthedocs.io/en/latest/?badge=latest)
[![GitHub license](https://img.shields.io/github/license/Correct-Syntax/Gimel-Studio?color=light-green)](https://github.com/Correct-Syntax/Gimel-Studio/blob/master/LICENSE)
![Build Gimel Studio](https://github.com/Correct-Syntax/Gimel-Studio/workflows/Build%20Gimel%20Studio/badge.svg)
[![Gitter](https://badges.gitter.im/Gimel-Studio/community.svg)](https://gitter.im/Gimel-Studio/community?utm_source=badge&utm_medium=badge)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/Correct-Syntax/Gimel-Studio/latest?style=flat)


[Website](https://correctsyntax.com/projects/gimel-studio/) | [Downloads](https://correctsyntax.com/projects/gimel-studio/#download) | [Official Manual](https://gimel-studio.readthedocs.io/en/latest/) | [Discord Server](https://discord.gg/RqwbDrVDpK) | [Community Discussion](https://github.com/Correct-Syntax/Gimel-Studio/discussions)


Gimel Studio is a cross-platform, node-based, non-destructive image editor. It has a workflow for compositing, masking, manipulating, generating and editing images and is complete with a registry of 20+ nodes and an API allowing users to script their own custom nodes in Python.

Currently, Gimel Studio provides basic image editing features such as flip, color balance, brightness, contrast and blur effects, as well as more advanced editing capabilities such as generating PBR maps for use in 3D from image textures.

*Still in BETA stage and WIP, but can be considered stable enough for light production work.*

**Please note that the development branches may be unstable and/or have new dependencies from the released version and the master branch.**


# WIP MacOs Support

MacOs binaries are not yet officially available. However, a test binary is in the latest pre-release [here](https://github.com/Correct-Syntax/Gimel-Studio/releases/tag/v0.5.2-pre-beta1).

See the [building from source](https://gimel-studio.readthedocs.io/en/latest/getting_started/building_from_source.html#macos) documentation to build it from the source code yourself.

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


# Project Goals

Here is a little rundown of what the goals of this project are and what they are not at this time. These *may change at any time*, but for now, Gimel Studio will be **focused** into certian areas and avoid other areas entirely.

**Development of Gimel Studio (currently) aims to...**

* include a range of nodes focused on filters, effects, transformations, color grading, etc
* be simple enough for non-technical people to use, yet provide a powerful and streamlined experience for professional editing
* provide fully comprehensive graphical indications in each step of the image editing process
* give users access to a rich API for scripting custom nodes in Python
* deliever a non-destructive, fast workflow and great user experience
* support Linux, Windows & MacOs operating systems seamlessly
* support low system hardware requirements (as much as is reasonably possible), so as to be inclusive of even those who don't have super-computers...
* listen to your feedback on these goals :)

**Development of Gimel Studio does not (currently) aim to...**

* provide any drawing and/or painting tools, except "Add text to image", etc
* be a full-blown procedual texture generator, like many node-based programs out there (though anyone can write their own nodes for that with the API, if they so desire)


# News

[v0.5.1 beta](https://github.com/Correct-Syntax/Gimel-Studio/releases/tag/v0.5.1-beta) is now available.

See the <a href="https://correctsyntax.com/blog/">Correct Syntax blog</a> for news and updates on releases and upcoming features.


# Download Releases

Head to the <a href="https://correctsyntax.com/projects/gimel-studio/">Gimel Studio homepage</a> to download the latest release for Windows and Linux.


# Feature Requests & Bug Reports

Please open an issue in the Github issues *for bug reports, crash reports and installation issues ONLY*.

For feature requests, non-bug report questions, etc please start a new discussion in the repository [Discussions area](https://github.com/Correct-Syntax/Gimel-Studio/discussions) or feel free to email me at <correctsyntax@yahoo.com> if you prefer something a bit more private.

You can also join the Gimel Studio [Discord Server](https://discord.gg/RqwbDrVDpK) or the [Gitter Community](https://gitter.im/Gimel-Studio/general?utm_source=share-link&utm_medium=link&utm_campaign=share-link). (Either ones works fine; whichever you personally prefer!)


# Development

**You Are Welcome to Help Develop Gimel Studio!**

Pull requests are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidlines. Feel  free to join the Gimel Studio [Discord Server](https://discord.gg/RqwbDrVDpK) or [Gitter Community](https://gitter.im/Gimel-Studio/community) if you are interested in discussing design/development of Gimel Studio or have questions.


# Installing from source

Please see the building from source documentation <a href="https://gimel-studio.readthedocs.io/en/latest/install.html#building-from-source">here</a>. Please open a [Github Issue](https://github.com/Correct-Syntax/Gimel-Studio/issues/new/choose) if you have problems building from source.


# Building the documentation from source

The Gimel Studio docs use the Sphinx package.

  * ``pip install -r docs/requirements.txt``
  * ``cd docs``
  * Now run ``make html`` to build the docs.

You will find the HTML docs in the ``build`` folder.


# License

Gimel Studio is licensed under the Apache License, Version 2.0. See the LICENSE and NOTICE files for full copyright and license information.
