

import io
import pickle
import os.path

import wx
from PIL import Image
import numpy as np

from GimelStudio import meta


class GimelStudioProject(object):
    def __init__(self, parent):
        self._parent = parent
        self._version = meta.APP_VERSION

    def OpenProject(self, path):
        pass
