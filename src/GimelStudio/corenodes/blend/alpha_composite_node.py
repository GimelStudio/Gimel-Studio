from PIL import Image, ImageChops, ImageOps

from GimelStudio.api import (Color, RenderImage, List, NodeBase,
                         ParameterDefinition, PropertyDefinition,
                         RegisterNode)
 
class NodeDefinition(NodeBase):

    @property
    def NodeName(self):
        return "corenode_alphacomposite"

    @property
    def NodeLabel(self):
        return "Alpha Composite"

    @property
    def NodeCategory(self):
        return "BLEND"

    @property
    def NodeDescription(self):
        return "Alpha composites two images based on the alpha of\n the given mask." 

    @property
    def NodeVersion(self):
        return "1.0.0"  

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software" 

    @property
    def NodeParameters(self):
        return [
            ParameterDefinition('Image 1',
                                param_type='image',
                                default_value=RenderImage('RGBA', (256, 256), (0, 0, 0, 1))),
            ParameterDefinition('Image 2',
                                param_type='image',
                                default_value=RenderImage('RGBA', (256, 256), (0, 0, 0, 1))),
            ParameterDefinition('Mask',
                                param_type='image',
                                default_value=RenderImage('RGBA', (256, 256), (0, 0, 0, 1))),
        ]


    def NodePropertiesUI(self, node, ui, parent, sizer):
        self.NodePropertiesHelperInit(node, ui, parent, sizer)
        
    def NodeEvaluation(self, eval_info):
        image1 = eval_info.EvaluateParameter('Image 1')
        image2 = eval_info.EvaluateParameter('Image 2')
        mask = eval_info.EvaluateParameter('Mask')

        image = RenderImage() 
        main_image = image1.GetImage()
        layer_image = ImageOps.fit(image2.GetImage(), main_image.size)
        mask_image = ImageOps.fit(mask.GetImage(), main_image.size).convert('RGBA')
        image.SetAsImage(Image.composite(main_image, layer_image, mask_image))

        self.NodeSetThumbnail(image.GetImage())
        return image

RegisterNode(NodeDefinition)