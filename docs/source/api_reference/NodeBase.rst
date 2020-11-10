.. py:module:: GimelStudio.node.nodebase
.. py:currentmodule:: GimelStudio.node.nodebase


NodeBase
========

Base class for all nodes which defines a node's core attributes.

Subclass this to create a custom node:

.. code-block:: python

    from GimelStudio import api

    # Subclass NodeBase
    class MyNode(api.NodeBase):
        def __init__(self, _id):
            api.NodeBase.__init__(self, _id)

        ...



    # Register the node
    api.RegisterNode(MyNode, "mynode")


.. autoclass:: GimelStudio.node.NodeBase


Utility Methods
^^^^^^^^^^^^^^^

.. automethod:: GimelStudio.node.NodeBase.GetType
.. automethod:: GimelStudio.node.NodeBase.GetId
.. automethod:: GimelStudio.node.NodeBase.IsOutputNode
.. automethod:: GimelStudio.node.NodeBase.GetRect
.. automethod:: GimelStudio.node.NodeBase.SetRect
.. automethod:: GimelStudio.node.NodeBase.IsSelected
.. automethod:: GimelStudio.node.NodeBase.SetSelected
.. automethod:: GimelStudio.node.NodeBase.IsActive
.. automethod:: GimelStudio.node.NodeBase.SetActive
.. automethod:: GimelStudio.node.NodeBase.IsMuted
.. automethod:: GimelStudio.node.NodeBase.SetMuted
.. automethod:: GimelStudio.node.NodeBase.GetPosition
.. automethod:: GimelStudio.node.NodeBase.SetPosition
.. automethod:: GimelStudio.node.NodeBase.GetSockets
.. automethod:: GimelStudio.node.NodeBase.GetLabel
.. autoproperty:: GimelStudio.node.NodeBase.Parameters
.. autoproperty:: GimelStudio.node.NodeBase.Properties
.. autoproperty:: GimelStudio.node.NodeBase.EvaluateNode
.. autoproperty:: GimelStudio.node.NodeBase.NodeGraphMethods


Core Methods
^^^^^^^^^^^^

.. autoproperty:: GimelStudio.node.NodeBase.NodeMeta

.. automethod:: GimelStudio.node.NodeBase.NodeInitProps
.. automethod:: GimelStudio.node.NodeBase.NodeInitParams
.. automethod:: GimelStudio.node.NodeBase.NodeAddProp
.. automethod:: GimelStudio.node.NodeBase.NodeAddParam
.. automethod:: GimelStudio.node.NodeBase.NodeEditProp
.. automethod:: GimelStudio.node.NodeBase.NodePanelUI
.. automethod:: GimelStudio.node.NodeBase.NodeEvaluation
.. automethod:: GimelStudio.node.NodeBase.WidgetEventHook
.. automethod:: GimelStudio.node.NodeBase.Draw
.. automethod:: GimelStudio.node.NodeBase.RefreshNodeGraph
.. automethod:: GimelStudio.node.NodeBase.RefreshPropertyPanel
.. automethod:: GimelStudio.node.NodeBase.HitTest
.. automethod:: GimelStudio.node.NodeBase.NodeSetThumb
