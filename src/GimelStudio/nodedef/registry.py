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
## FILE: registry.py
## AUTHOR(S): Noah Rahm
## PURPOSE: -
##
## This file includes code that was modified from imagegen 
## (https://github.com/nfactorial/imagegen) which is licensed 
## under the Apache License Version 2.0 
## Copyright 2016 nfactorial
## ----------------------------------------------------------------------------

from .node import Node


# This dictionary contains all the nodes currently registered.
NODE_REGISTRY = {}


class NodeExistsError(Exception):
    """ This exception is raised when a node is registered that already exists. """
    def __init__(self, name):
        """ Prepares the exception for use by the application. """
        super(NodeExistsError, self).__init__(name)
        self.name = name

    def __str__(self):
        """ Creates a string representation of the exception. """
        return 'The node {} already exists within the registry.'.format(self.name)


def RegisterNode(node_definition):
    """ Attempts to register a new node with the node registry. """
    name = node_definition()._name
    if name == "":
        raise TypeError('This node does not have a name specified.')
    else:
        if name in NODE_REGISTRY:
            raise NodeExistsError(name)

        NODE_REGISTRY[name] = node_definition


def UnregisterNode(name):
    """ Removes a registered node from the applications registry. """
    if name in NODE_REGISTRY:
        del NODE_REGISTRY[name]


def CreateNode(parent, node_type, _id, pos):
    """ Create an instance of a node associated with the specified name. """
    if node_type in NODE_REGISTRY:
        # Initialize the base class here so that a new instance is created for each node.
        return Node(parent, NODE_REGISTRY[node_type](), pos, _id)
    raise TypeError('The specified node type {} could not be found.'.format(node_type))
