## ----------------------------------------------------------------------------
## Gimel Studio © 2020 CorrectSyntax Software, Noah Rahm. All rights reserved.
##
## FILE: registry.py
## AUTHOR(S): Noah Rahm
## PURPOSE: -
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
