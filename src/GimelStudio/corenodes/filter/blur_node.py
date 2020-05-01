from PIL import Image, ImageFilter

from GimelStudio.api import (Color, RenderImage, List, ArrayFromImage,
                         ArrayToImage, NodeBase, ParameterDefinition,
                         PropertyDefinition, RegisterNode)

 
class NodeDefinition(NodeBase):
    
    @property
    def NodeName(self):
        return "corenode_blur"

    @property
    def NodeLabel(self):
        return "Blur"

    @property
    def NodeCategory(self):
        return "FILTER"

    @property
    def NodeDescription(self):
        return "Blurs the given image using the specified blur type." 

    @property
    def NodeVersion(self):
        return "2.0.0" 

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software" 

    @property
    def NodeProperties(self):
        return [
            PropertyDefinition('Radius',
                               prop_type='integer',
                               value=2
                               ),
            ]

    @property
    def NodeParameters(self):
        return [
            ParameterDefinition('Image',
                                param_type='image',
                                default_value=RenderImage('RGBA', (256, 256), (0, 0, 0, 1))),
        ]


 
    def NodePropertiesUI(self, node, ui, parent, sizer):
        self.NodePropertiesHelperInit(node, ui, parent, sizer)

        current_radius_value = self.NodeGetPropertyValue('Radius')

        radius_label = ui.StaticText(parent, label="Blur Radius:")
        sizer.Add(radius_label, pos=(2, 0), flag=ui.LEFT|ui.TOP, border=10)

        self.radiusspinctrl = ui.SpinCtrl(parent, -1, "", (30, 50))
        self.radiusspinctrl.SetRange(1, 500)
        self.radiusspinctrl.SetValue(current_radius_value)
        sizer.Add(self.radiusspinctrl, pos=(2, 1), span=(1, 3), flag=ui.TOP|ui.EXPAND, border=5)

        parent.Bind(ui.EVT_SPINCTRL, self.OnRadiusSpin, self.radiusspinctrl)


    def OnRadiusSpin(self, evt):
        self.NodePropertiesUpdate('Radius', self.radiusspinctrl.GetValue())
    
    def NodeEvaluation(self, eval_info):
        image1 = eval_info.EvaluateParameter('Image')

        # Get the values
        Radius = eval_info.EvaluateProperty('Radius')
        
        image = RenderImage()
        image.SetAsImage(image1.GetImage().filter(ImageFilter.GaussianBlur(Radius)).convert('RGBA'))
        self.NodeSetThumbnail(image.GetImage())
        return image


RegisterNode(NodeDefinition)
