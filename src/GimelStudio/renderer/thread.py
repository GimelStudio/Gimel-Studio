## ----------------------------------------------------------------------------
## Gimel Studio Copyright 2020 Noah Rahm, Correct Syntax. All rights reserved.
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##    http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
##
## FILE: thread.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the thread worker for the renderer
## ----------------------------------------------------------------------------

from threading import *

import wx


# Define notification event for thread completion
EVT_RESULT_ID = wx.NewIdRef()

def EVT_RENDER_RESULT(win, func):
    """ Define result event """
    win.Connect(-1, -1, EVT_RESULT_ID, func)

class ResultEvent(wx.PyEvent):
    """ Simple event to carry arbitrary result data """
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data

class RenderThread(Thread):
    """ Thread class that executes processing """
    def __init__(self, parent):
        """ Init the worker thread"""
        Thread.__init__(self)
        self._parent = parent
        # Starts the thread running
        self.start()

    def run(self):
        """ Run the worker thread """
        # Code executing in the new thread. 
        render_image = self._parent._renderer.Render(self._parent._nodeGraph.GetNodes())

        # The result returned
        wx.PostEvent(self._parent, ResultEvent(render_image))
