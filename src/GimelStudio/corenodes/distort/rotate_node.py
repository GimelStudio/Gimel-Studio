from PIL import Image
import wx.lib.agw.cubecolourdialog as CCD

from GimelStudio.api import (Color, List, RenderImage, NodeBase,
                         ParameterDefinition, PropertyDefinition,
                         RegisterNode)

 
class NodeDefinition(NodeBase):
    
    @property
    def NodeName(self):
        return "corenode_rotate"

    @property
    def NodeLabel(self):
        return "Rotate"

    @property
    def NodeCategory(self):
        return "DISTORT"

    @property
    def NodeDescription(self):
        return "Rotates the given image." 

    @property
    def NodeVersion(self):
        return "1.0.0" 

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
                                 'BILINEAR',
                                 'BICUBIC',
                                 ], 'NEAREST')
                               ),
            PropertyDefinition('Angle',
                               prop_type='list',
                               value=List([
                                 '45',
                                 '90',
                                 '135',
                                 '180',
                                 '360',
                                 ], '90')
                               ),
            PropertyDefinition('Fillcolor',
                                prop_type='color',
                                value=(0, 0, 0, 1)
                                ),
            PropertyDefinition('Expand',
                               prop_type='boolean',
                               value=True
                               )
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
                                 'BILINEAR',
                                 'BICUBIC',
                                 ], style=ui.CB_READONLY)
        sizer.Add(self.resamplecombobox, pos=(2, 1), span=(1, 3), flag=ui.TOP|ui.EXPAND, border=5)

        # Angle
        current_angle_value = self.NodeGetPropertyValue('Angle')

        anglelabel = ui.StaticText(parent, label="Angle:")
        sizer.Add(anglelabel, pos=(3, 0), flag=ui.LEFT|ui.TOP, border=10)

        self.anglecombobox = ui.ComboBox(parent, id=ui.ID_ANY, 
             value=current_angle_value, choices=[
                                 '45',
                                 '90',
                                 '135',
                                 '180',
                                 '360',
                                 ], style=ui.CB_READONLY)
        sizer.Add(self.anglecombobox, pos=(3, 1), span=(1, 3), flag=ui.TOP|ui.EXPAND, border=5)

        # Expand 
        current_expand_value = self.NodeGetPropertyValue('Expand')

        expandlabel = ui.StaticText(parent, label="Expand:")
        sizer.Add(expandlabel, pos=(4, 0), flag=ui.LEFT|ui.TOP, border=10)

        self.expandcheckbox = ui.CheckBox(parent, id=ui.ID_ANY)
        self.expandcheckbox.SetValue(current_expand_value)
        sizer.Add(self.expandcheckbox, pos=(4, 1), span=(1, 3), flag=ui.TOP|ui.EXPAND, border=5)

        # Fillcolor
        current_fillcolor_value = self.NodeGetPropertyValue('Fillcolor')
        self.fillcolordata = ui.ColourData()
        self.fillcolordata.SetColour(current_fillcolor_value)

        fillcolorlabel = ui.StaticText(parent, label="Fillcolor: ")
        sizer.Add(fillcolorlabel, pos=(5, 0), flag=ui.LEFT|ui.TOP, border=10)

        self.fillcolortxtctrl = ui.TextCtrl(parent)
        sizer.Add(self.fillcolortxtctrl, pos=(5, 1), span=(1, 3), flag=ui.TOP|ui.EXPAND, border=5)
        self.fillcolortxtctrl.ChangeValue(str(current_fillcolor_value))

        self.fillcolorbtn = ui.Button(parent, label="Select...")
        sizer.Add(self.fillcolorbtn, pos=(5, 4), flag=ui.TOP|ui.RIGHT, border=5)

        # Bindings
        parent.Bind(ui.EVT_COMBOBOX, self.ResampleEvtChoice, self.resamplecombobox)
        parent.Bind(ui.EVT_COMBOBOX, self.AngleEvtChoice, self.anglecombobox)
        parent.Bind(ui.EVT_CHECKBOX, self.OnExpandCheckbox, self.expandcheckbox)
        parent.Bind(ui.EVT_BUTTON, self.OnFillColorButton, self.fillcolorbtn)


    def ResampleEvtChoice(self, evt):
        value = evt.GetString()
        if not value:
            return
        self.NodePropertiesUpdate('Resample', value)

    def AngleEvtChoice(self, evt):
        value = evt.GetString()
        if not value:
            return
        self.NodePropertiesUpdate('Angle', value)

    def OnExpandCheckbox(self, evt):
        value = evt.IsChecked()
        self.NodePropertiesUpdate('Expand', value)

    def OnFillColorButton(self, evt):
        self.colordialog = CCD.CubeColourDialog(self.parent, self.fillcolordata)
        if self.colordialog.ShowModal() == self.ui.ID_OK:

            self.colordata = self.colordialog.GetColourData()
            colordata = self.fillcolordata.GetColour()
            self.NodePropertiesUpdate(
                'Fillcolor',
                (colordata.Red(),
                 colordata.Green(),
                 colordata.Blue(),
                 colordata.Alpha())
                )
            self.fillcolortxtctrl.ChangeValue(str((colordata.Red(),
                                            colordata.Green(),
                                            colordata.Blue(),
                                            colordata.Alpha()
                                            )))
 
    def NodeEvaluation(self, eval_info):
        image1 = eval_info.EvaluateParameter('Image')

        resample = eval_info.EvaluateProperty('Resample')
        angle = eval_info.EvaluateProperty('Angle')
        expand = eval_info.EvaluateProperty('Expand')
        fillcolor = eval_info.EvaluateProperty('Fillcolor')

        if resample == 'BILINEAR':
            RESAMPLE = Image.BILINEAR

        elif resample == 'BICUBIC':
            RESAMPLE = Image.BICUBIC

        elif resample == 'LANCZOS':
            RESAMPLE = Image.LANCZOS

        else: 
            RESAMPLE = Image.NEAREST 

        image = RenderImage()
        rotated_img = image1.GetImage().rotate(
            angle=int(angle),
            expand=expand,
            fillcolor=fillcolor,
            resample=RESAMPLE
        )
        image.SetAsImage(rotated_img)
        self.NodeSetThumbnail(image.GetImage())
        return image


RegisterNode(NodeDefinition)
