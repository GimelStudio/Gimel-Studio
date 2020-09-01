.. py:module:: GimelStudio.datatypes.data_types
.. py:currentmodule:: GimelStudio.datatypes.data_types


Data Types
==========

Data-type classes for handling data in Gimel Studio. 

Use these when creating a custom node with Parameters:
    
.. code-block:: python

    from GimelStudio.api import (NodeBase, RegisterNode, 
                                Parameter, RenderImage)
    
    # Subclass NodeBase
    class NodeDefinition(NodeBase):
        ...

        # Define parameters
        @property
        def NodeParameters(self):
            return [
                Parameter('Image',
                    param_type='RENDERIMAGE',
                    default_value=RenderImage('RGBA', (256, 256), (0, 0, 0, 1))
                    ),
            ]
        ...

    # Register the node
    RegisterNode(NodeDefinition)


.. autoclass:: GimelStudio.datatypes.RenderImage
.. automethod:: GimelStudio.datatypes.RenderImage.GetImage
.. automethod:: GimelStudio.datatypes.RenderImage.SetAsOpenedImage
.. automethod:: GimelStudio.datatypes.RenderImage.SetAsImage

.. autoclass:: GimelStudio.datatypes.List
.. automethod:: GimelStudio.datatypes.List.GetItems
.. automethod:: GimelStudio.datatypes.List.GetDefault
.. automethod:: GimelStudio.datatypes.List.SetAsValue

.. autoclass:: GimelStudio.datatypes.Color

.. note::

    ``Color`` is unused and has not been maintained for a while.

.. automethod:: GimelStudio.datatypes.Color.GetColors
.. automethod:: GimelStudio.datatypes.Color.GetHex

