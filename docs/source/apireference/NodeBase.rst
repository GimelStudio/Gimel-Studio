.. py:module:: GimelStudio.node.nodebase
.. py:currentmodule:: GimelStudio.node.nodebase


NodeBase
========

Base class for all nodes which defines a node's core attributes. 

Subclass this to create a custom node:
    
.. code-block:: python

    from GimelStudio.api import NodeBase, RegisterNode
    
    # Subclass NodeBase
    class NodeDefinition(NodeBase):
        ...
	
        # Override methods to customize the base node
        @property
        def NodeLabel(self):
            return "Example Node Label"
        ...

    # Register the node
    RegisterNode(NodeDefinition)


.. autoclass:: GimelStudio.node.NodeBase
 
.. autoproperty:: GimelStudio.node.NodeBase.Node
.. autoproperty:: GimelStudio.node.NodeBase.NodeAuthor
.. autoproperty:: GimelStudio.node.NodeBase.NodeVersion
.. autoproperty:: GimelStudio.node.NodeBase.NodeDescription

.. autoproperty:: GimelStudio.node.NodeBase.NodeSupportsImagePacking
.. versionadded:: 0.4.0

.. autoproperty:: GimelStudio.node.NodeBase.NodeIDName
.. autoproperty:: GimelStudio.node.NodeBase.NodeLabel
.. autoproperty:: GimelStudio.node.NodeBase.NodeCategory
.. autoproperty:: GimelStudio.node.NodeBase.NodeOutputType
.. autoproperty:: GimelStudio.node.NodeBase.NodeProperties
.. autoproperty:: GimelStudio.node.NodeBase.NodeParameters

.. automethod:: GimelStudio.node.NodeBase.NodePropertiesUI
.. automethod:: GimelStudio.node.NodeBase.NodeEvaluation

.. automethod:: GimelStudio.node.NodeBase.NodePropertiesUpdate
.. automethod:: GimelStudio.node.NodeBase.NodePropertiesUI
.. automethod:: GimelStudio.node.NodeBase.NodeSetThumb
.. automethod:: GimelStudio.node.NodeBase.NodeGetPropValue