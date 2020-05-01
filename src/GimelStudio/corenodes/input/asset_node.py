import os
from PIL import Image

from GimelStudio.api import (Color, RenderImage, NodeBase,
                         ParameterDefinition, PropertyDefinition,
                         RegisterNode)

 
class NodeDefinition(NodeBase):
    
    @property
    def NodeName(self):
        return "corenode_asset"

    @property
    def NodeLabel(self):
        return "Asset"

    @property
    def NodeCategory(self):
        return "INPUT"

    @property
    def NodeDescription(self):
        return "Inputs an image from the asset library." 

    @property
    def NodeVersion(self):
        return "1.0.0" 

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software" 

    @property
    def NodeProperties(self): 
        return [
            PropertyDefinition('Path',
                               prop_type='filepath',
                               value=''
                               ),
        ]


    def NodeEvaluation(self, eval_info):
        path = eval_info.EvaluateProperty('Path')
        print('p->', path)

        image = RenderImage()
        if path != '':
            image.SetAsOpenedImage(path)
        image.SetAsImage(image.GetImage().convert('RGBA'))
        self.NodeSetThumbnail(image.GetImage())
        return image 



RegisterNode(NodeDefinition)
