from PIL import Image

from GimelStudio.api import (Color, RenderImage, NodeBase,
                         ParameterDefinition, PropertyDefinition,
                         RegisterNode)

class NodeDefinition(NodeBase):

    @property
    def NodeName(self):
        return "corenode_outputcomposite"

    @property
    def NodeLabel(self):
        return "Composite"

    @property
    def NodeCategory(self):
        return "OUTPUT"

    @property
    def NodeDescription(self):
        return """The most important node of them all. :) 
         This is registered here for the UI -the evaluation is handled elsewhere."""  

    @property
    def NodeVersion(self):
        return "1.0.0" 

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software" 

    @property
    def NodeParameters(self):
        return [
            ParameterDefinition('Image',
                                param_type='image',
                                default_value=RenderImage('RGBA', (256, 256), (0, 0, 0, 1))),
        ]

    def NodeEvaluation(self, eval_info):
        pass



RegisterNode(NodeDefinition)


