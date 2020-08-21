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
## FILE: api.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define end-user API functions, methods, classes at a higher-level
## ----------------------------------------------------------------------------

from GimelStudio.node import ParameterDefinition, PropertyDefinition
from GimelStudio.node_registry import _NodeRegistryBase


def RegisterNode(nodedef):
    """ Registers the given node in the Node Registry. Wrapper of the 
    internal Node Registry ``RegisterNode`` method.

    :param nodedef: subclass of ``NodeBase`` defining the node to be registered
    """
    _NodeRegistryBase.RegisterNode(nodedef)


def UnregisterNode(name):
    """ Not implemented. """
    raise NotImplementedError


# Shorten the names for the API
Parameter = ParameterDefinition
Property = PropertyDefinition
