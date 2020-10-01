.. py:module:: GimelStudio.datatypes.data_types
.. py:currentmodule:: GimelStudio.datatypes.data_types


Data Types
==========

Data-type classes for handling data in Gimel Studio.

Use when creating a node, like so:

.. code-block:: python

    from GimelStudio import api

    # Subclass NodeBase
    class MyNode(api.NodeBase):
        def __init__(self, _id):
            api.NodeBase.__init__(self, _id)

        ...

    def NodeEvaluation(self, eval_info):
        ...

        image = api.RenderImage()
        # do something to the image and set it with SetAsImage
        image.SetAsImage(img)

        return image

    # Register the node
    api.RegisterNode(MyNode, "mynode")


.. autoclass:: GimelStudio.datatypes.RenderImage
.. automethod:: GimelStudio.datatypes.RenderImage.GetImage
.. automethod:: GimelStudio.datatypes.RenderImage.SetAsOpenedImage
.. automethod:: GimelStudio.datatypes.RenderImage.SetAsImage
