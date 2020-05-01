from PIL import Image, ImageEnhance 

from GimelStudio.api import (Color, RenderImage, List, ArrayFromImage,
                         ArrayToImage, NodeBase, ParameterDefinition,
                         PropertyDefinition, RegisterNode)

 
class NodeDefinition(NodeBase):
    
    @property
    def NodeName(self):
        return "corenode_colorbalance"

    @property
    def NodeLabel(self):
        return "Color Balance"

    @property
    def NodeCategory(self):
        return "COLOR"

    @property
    def NodeDescription(self):
        return "Adjusts the image color balance." 

    @property
    def NodeVersion(self):
        return "1.0.1" 

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software" 

    @property
    def NodeProperties(self):
        return [
            PropertyDefinition('Amount',
                               prop_type='integer',
                               value=1
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

        self.amountspinctrl = ui.SpinCtrlDouble(
            parent, pos=(30, 50),
            value=str(current_amount_value),
            min=0.0, max=6.0, inc=0.05
            )
        self.amountspinctrl.SetDigits(2)
        sizer.Add(self.amountspinctrl, pos=(2, 1), span=(1, 3), flag=ui.TOP|ui.EXPAND, border=5)

        parent.Bind(ui.EVT_SPINCTRLDOUBLE, self.OnAmountSpin, self.amountspinctrl)

    def OnAmountSpin(self, event):
        self.NodePropertiesUpdate('Amount', self.amountspinctrl.GetValue())
    
    def NodeEvaluation(self, eval_info):
        image1 = eval_info.EvaluateParameter('Image')
        Amount = eval_info.EvaluateProperty('Amount')
        
        image = RenderImage()
        enhancer = ImageEnhance.Color(image1.GetImage())
        image.SetAsImage(enhancer.enhance(Amount).convert('RGBA'))
        self.NodeSetThumbnail(image.GetImage())
        return image


RegisterNode(NodeDefinition)
