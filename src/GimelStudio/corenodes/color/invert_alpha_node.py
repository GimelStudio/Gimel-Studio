from PIL import Image, ImageChops

from GimelStudio.api import (Color, RenderImage, List, ArrayFromImage,
                         ArrayToImage, NodeBase, ParameterDefinition,
                         PropertyDefinition, RegisterNode)

 
class NodeDefinition(NodeBase):
    
    @property
    def NodeName(self):
        return "corenode_invertalpha"

    @property
    def NodeLabel(self):
        return "Invert Alpha"

    @property
    def NodeCategory(self):
        return "COLOR"

    @property
    def NodeDescription(self):
        return "Inverts an image alpha channel." 

    @property
    def NodeVersion(self):
        return "1.0.2" 

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


    def NodePropertiesUI(self, node, ui, parent, sizer):
        self.NodePropertiesHelperInit(node, ui, parent, sizer)


    def NodeEvaluation(self, eval_info):
        image1 = eval_info.EvaluateParameter('Image')
        
        image = RenderImage()
        image.SetAsImage(ImageChops.invert(image1.GetImage()).convert('RGBA'))
        self.NodeSetThumbnail(image.GetImage())
        return image


RegisterNode(NodeDefinition)
