from PIL import Image, ImageEnhance 

from GimelStudio.api import (Color, RenderImage, List, ArrayFromImage,
                         ArrayToImage, NodeBase, ParameterDefinition,
                         PropertyDefinition, RegisterNode)

 
class NodeDefinition(NodeBase):
    
    @property
    def NodeName(self):
        return "corenode_sharpness"

    @property
    def NodeLabel(self):
        return "Sharpness"

    @property
    def NodeCategory(self):
        return "FILTER"

    @property
    def NodeDescription(self):
        return "Sharpens the image by the given amount." 

    @property
    def NodeVersion(self):
        return "1.0.2" 

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software" 

    @property
    def NodeProperties(self):
        return [
            PropertyDefinition('Amount',
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

        current_amount_value = self.NodeGetPropertyValue('Amount')

        amount_label = ui.StaticText(parent, label="Amount:")
        sizer.Add(amount_label, pos=(2, 0), flag=ui.LEFT|ui.TOP, border=10)

        self.amountspinctrl = ui.SpinCtrl(parent, -1, "", (30, 50))
        self.amountspinctrl.SetRange(1, 500)
        self.amountspinctrl.SetValue(current_amount_value)
        sizer.Add(self.amountspinctrl, pos=(2, 1), span=(1, 3), flag=ui.TOP|ui.EXPAND, border=5)

        parent.Bind(ui.EVT_SPINCTRL, self.OnAmountSpin, self.amountspinctrl)

    def OnAmountSpin(self, event):
        self.NodePropertiesUpdate('Amount', self.amountspinctrl.GetValue())
    
    def NodeEvaluation(self, eval_info):
        image1 = eval_info.EvaluateParameter('Image')
        Amount = eval_info.EvaluateProperty('Amount')
        
        image = RenderImage()
        enhancer = ImageEnhance.Sharpness(image1.GetImage())
        image.SetAsImage(enhancer.enhance(Amount).convert('RGBA'))
        self.NodeSetThumbnail(image.GetImage())
        return image


RegisterNode(NodeDefinition)
