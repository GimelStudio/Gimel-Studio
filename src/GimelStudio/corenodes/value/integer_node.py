from PIL import Image

from GimelStudio.api import (Color, RenderImage, NodeBase,
                         ParameterDefinition, PropertyDefinition,
                         RegisterNode)
 
class NodeDefinition(NodeBase):
     
    @property
    def NodeName(self):
        return "integer"
 
    @property
    def NodeLabel(self):
        return "Integer" 

    @property
    def NodeCategory(self):
        return "VALUE"

    @property
    def NodeDescription(self):
        return "Inputs an integer."

    @property
    def NodeIsDepreciated(self):
        return True

    @property
    def NodeVersion(self):
        return "1.0.0" 

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software" 

    @property
    def NodeOutput(self):
        return "integer"

    @property
    def NodeProperties(self):
        return [
            PropertyDefinition('integer',
                               prop_type='integer',
                               value=1
                               ),
        ]

    def NodePropertiesUI(self, node, ui, parent, sizer):
        self.NodePropertiesHelperInit(node, ui, parent, sizer)

        integerlabel = ui.StaticText(parent, label="Value:")
        sizer.Add(integerlabel, pos=(2, 0), flag=ui.LEFT|ui.TOP, border=10)
        
        self.integer_sc = ui.SpinCtrl(parent, -1, "", (80, 50))
        self.integer_sc.SetRange(1, 8000)
        current_value = self.NodeGetPropertyValue('integer')
        self.integer_val = int(current_value)
        self.integer_sc.SetValue(current_value)

        parent.Bind(ui.EVT_SPINCTRL, self.OnIntegerSpin, self.integer_sc)
        sizer.Add(self.integer_sc, pos=(2, 1), span=(1, 3), flag=ui.TOP|ui.EXPAND, border=5)


    def OnIntegerSpin(self, event):
        self.NodePropertiesUpdate('integer', self.integer_sc.GetValue())

    
    def NodeEvaluation(self, eval_info):
        integer = eval_info.EvaluateProperty('integer')
        return integer 


RegisterNode(NodeDefinition)
