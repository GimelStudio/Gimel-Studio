from PIL import Image

from GimelStudio.api import (Color, List, RenderImage, NodeBase,
                         ParameterDefinition, PropertyDefinition,
                         RegisterNode)

 
class NodeDefinition(NodeBase):
    
    @property
    def NodeName(self):
        return "corenode_resize"

    @property
    def NodeLabel(self):
        return "Resize"

    @property
    def NodeCategory(self):
        return "DISTORT"

    @property
    def NodeDescription(self):
        return "Resizes the given image." 

    @property
    def NodeVersion(self):
        return "1.1.0" 

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software" 

    @property
    def NodeProperties(self):
        return [
            PropertyDefinition('Resample',
                               prop_type='list',
                               value=List([
                                 'NEAREST',
                                 'ANTIALIAS',
                                 'BOX',
                                 'BILINEAR',
                                 'HAMMING',
                                 'BICUBIC',
                                 'LANCZOS'
                                 ], 'NEAREST')
                               ),
            PropertyDefinition('Size',
                               prop_type='reglist',
                               value=[256, 256]
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
        
        # Resample
        current_resample_value = self.NodeGetPropertyValue('Resample')

        resamplelabel = ui.StaticText(parent, label="Resample:")
        sizer.Add(resamplelabel, pos=(2, 0), flag=ui.LEFT|ui.TOP, border=10)

        self.resamplecombobox = ui.ComboBox(parent, id=ui.ID_ANY, 
             value=current_resample_value, choices=[
                                 'NEAREST',
                                 'ANTIALIAS',
                                 'BOX',
                                 'BILINEAR',
                                 'HAMMING',
                                 'BICUBIC',
                                 'LANCZOS'
                                 ], style=ui.CB_READONLY)
        sizer.Add(self.resamplecombobox, pos=(2, 1), span=(1, 3), flag=ui.TOP|ui.EXPAND, border=5)

        # X Size
        current_x_value = self.NodeGetPropertyValue('Size')[0]

        x_sizelabel = ui.StaticText(parent, label="X:")
        sizer.Add(x_sizelabel, pos=(3, 0), flag=ui.LEFT|ui.TOP, border=10)

        self.x_sizespinctrl = ui.SpinCtrl(parent, -1, "", (30, 50))
        self.x_sizespinctrl.SetRange(1, 8000)
        self.size_x = int(current_x_value)
        self.x_sizespinctrl.SetValue(current_x_value)
        sizer.Add(self.x_sizespinctrl, pos=(3, 1), span=(1, 3), flag=ui.TOP|ui.EXPAND, border=5)


        # Y Size
        current_y_value = self.NodeGetPropertyValue('Size')[1]

        y_sizelabel = ui.StaticText(parent, label="Y:")
        sizer.Add(y_sizelabel, pos=(4, 0), flag=ui.LEFT|ui.TOP, border=10)

        self.y_sizespinctrl = ui.SpinCtrl(parent, -1, "", (30, 50))
        self.y_sizespinctrl.SetRange(1, 8000)
        self.size_y = int(current_y_value)
        self.y_sizespinctrl.SetValue(current_y_value)
        sizer.Add(self.y_sizespinctrl, pos=(4, 1), span=(1, 3), flag=ui.TOP|ui.EXPAND, border=5)

        # Bindings
        parent.Bind(ui.EVT_COMBOBOX, self.EvtChoice, self.resamplecombobox)
        parent.Bind(ui.EVT_SPINCTRL, self.OnXSpin, self.x_sizespinctrl)
        parent.Bind(ui.EVT_SPINCTRL, self.OnYSpin, self.y_sizespinctrl)

    def EvtChoice(self, evt):
        value = evt.GetString()
        if not value:
            return
        self.NodePropertiesUpdate('Resample', value)

    def OnXSpin(self, evt):
        self.size_x = self.x_sizespinctrl.GetValue()
        self.NodePropertiesUpdate('Size', self.GetSize())

    def OnYSpin(self, evt):
        self.size_y = self.y_sizespinctrl.GetValue()
        self.NodePropertiesUpdate('Size', self.GetSize())

    def GetSize(self):
        return [self.size_x, self.size_y]
 
    def NodeEvaluation(self, eval_info):
        image1 = eval_info.EvaluateParameter('Image')

        resample = eval_info.EvaluateProperty('Resample')
        size = eval_info.EvaluateProperty('Size')

        if resample == 'ANTIALIAS':
            RESIZE_RESAMPLE = Image.ANTIALIAS

        elif resample == 'BOX':
            RESIZE_RESAMPLE = Image.BOX

        elif resample == 'BILINEAR':
            RESIZE_RESAMPLE = Image.BILINEAR

        elif resample == 'HAMMING':
            RESIZE_RESAMPLE = Image.HAMMING

        elif resample == 'BICUBIC':
            RESIZE_RESAMPLE = Image.BICUBIC

        elif resample == 'LANCZOS':
            RESIZE_RESAMPLE = Image.LANCZOS

        else: 
            RESIZE_RESAMPLE = Image.NEAREST 

        image = RenderImage()
        image.SetAsImage(image1.GetImage().resize(
            (size[0],
             size[1]),
            resample=RESIZE_RESAMPLE))
        self.NodeSetThumbnail(image.GetImage())
        return image


RegisterNode(NodeDefinition)
