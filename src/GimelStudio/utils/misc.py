# ----------------------------------------------------------------------------
# Gimel Studio Copyright 2019-2020 by Noah Rahm and contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# FILE: misc.py
# AUTHOR(S): Noah Rahm
# PURPOSE: Provide utility misc functions
# ----------------------------------------------------------------------------

import os
import platform
import subprocess


def PopOpenExplorer(path):
    """ Method for opening the path in the system's File Explorer or Image viewer.

    Copied directly from:
    https://stackoverflow.com/questions/6631299/python-opening-a-folder-in-explorer-nautilus-finder
    """
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])
