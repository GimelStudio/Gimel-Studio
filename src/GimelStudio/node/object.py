# ----------------------------------------------------------------------------
# Gimel Studio Copyright 2019-2021 by Noah Rahm and contributors
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
# FILE: object.py
# AUTHOR(S): Noah Rahm
# PURPOSE: Define a class to tie together the model & view of the node
# ----------------------------------------------------------------------------

from .model import NodeModel
from .view import NodeView


class NodeObject(object):
    """ Base node object which ties together the model and view. """

    def __init__(self, _id):
        self._model = NodeModel(_id)
        self._view = NodeView(_id)

    @property
    def Model(self):
        """ Return the node model.

        :returns: the node model object.
        """
        return self._model

    @property
    def View(self):
        """ Return the node view.

        :returns: the node view object.
        """
        return self._view

    def UpdateView(self):
        """ Update the view from the model. """
        self.View._viewData = self.Model.ModelViewData
