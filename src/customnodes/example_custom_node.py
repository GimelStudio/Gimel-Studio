# This example file (example_custom_node.py) is public domain under the condition
# that it is NOT sold in any way and is used ONLY in the context of Gimel Studio.
# AKA: You are free to use this as a template for your own custom nodes.
#
# This is an example node script showing how you can use the Gimel Studio API
# to script your own custom nodes in Python.
#
# Updated for: v0.5.0 beta

from PIL import ImageEnhance

from GimelStudio import api


class ExampleCustomNode(api.NodeBase):
    def __init__(self, _id):
        api.NodeBase.__init__(self, _id)

    @property
    def NodeMeta(self):
        meta_info = {
            "label": "Example Custom Node",
            "author": "Your Name...",
            "version": (0, 0, 1),
            "supported_app_version": (0, 5, 0),
            "category": "COLOR",
            "description": "Example custom node showing how you can create a custom node with the Gimel Studio API"
        }
        return meta_info

    def NodeInitProps(self):
        p = api.PositiveIntegerProp(
            idname="Amount",
            default=1,
            min_val=0,
            max_val=25,
            widget=api.SLIDER_WIDGET,
            label="Amount:",
        )
        self.NodeAddProp(p)

    def NodeInitParams(self):
        p = api.RenderImageParam('Image')

        self.NodeAddParam(p)

    def NodeEvaluation(self, eval_info):
        image1 = eval_info.EvaluateParameter('Image')
        amount = eval_info.EvaluateProperty('Amount')

        image = api.RenderImage()
        enhancer = ImageEnhance.Brightness(image1.GetImage())
        image.SetAsImage(enhancer.enhance(amount).convert('RGBA'))

        self.NodeSetThumb(image.GetImage())
        return image


api.RegisterNode(ExampleCustomNode, "examplecustomnode_brightness")
