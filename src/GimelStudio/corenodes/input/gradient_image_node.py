import os
import wx.lib.agw.cubecolourdialog as CCD
from PIL import Image, ImageOps

from GimelStudio.api import (Color, List, RenderImage, NodeBase,
                         ParameterDefinition, PropertyDefinition,
                         RegisterNode)

 
class NodeDefinition(NodeBase):
    
    @property
    def NodeName(self):
        return "corenode_gradientimage"

    @property
    def NodeLabel(self):
        return "Gradient Image"

    @property
    def NodeCategory(self):
        return "INPUT"

    @property
    def NodeDescription(self):
        return "Creates a gradient image." 

    @property
    def NodeVersion(self):
        return "1.1.2" 

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software" 

    @property
    def NodeProperties(self): 
        return [
            PropertyDefinition('Gradient',
                               prop_type='list',
                               value=List([
                                 '0.1',
                                 '0.2',
                                 '0.5',
                                 '0.75',
                                 '1.0',
                                 '1.5',
                                 '2.0'
                                 ], '0.5')
                               ),
            PropertyDefinition('Color1',
                                prop_type='color',
                                value=(255, 255, 255, 255)
                                ),
            PropertyDefinition('Color2',
                                prop_type='color',
                                value=(0, 0, 0, 1)
                                ),
            PropertyDefinition('Size',
                               prop_type='reglist',
                               value=[256, 256]
                               ),
        ]

    def NodePropertiesUI(self, node, ui, parent, sizer):
        self.NodePropertiesHelperInit(node, ui, parent, sizer)

        # Gradient
        current_gradient_value = self.NodeGetPropertyValue('Gradient')

        gradientlabel = ui.StaticText(parent, label="Gradient:")
        sizer.Add(gradientlabel, pos=(2, 0), flag=ui.LEFT|ui.TOP, border=10)

        self.gradientcombobox = ui.ComboBox(parent, id=ui.ID_ANY, 
             value=current_gradient_value, choices=[
                                 '0.1',
                                 '0.2',
                                 '0.5',
                                 '0.75',
                                 '1.0',
                                 '1.5',
                                 '2.0'
                                 ], style=ui.CB_READONLY)
        sizer.Add(self.gradientcombobox, pos=(2, 1), span=(1, 3), flag=ui.TOP|ui.EXPAND, border=5)

        # Color 1
        current_color1_value = self.NodeGetPropertyValue('Color1')
        self.color1data = ui.ColourData()
        self.color1data.SetColour(current_color1_value)

        color1label = ui.StaticText(parent, label="Color 1: ")
        sizer.Add(color1label, pos=(3, 0), flag=ui.LEFT|ui.TOP, border=10)

        self.color1txtctrl = ui.TextCtrl(parent)
        sizer.Add(self.color1txtctrl, pos=(3, 1), span=(1, 3), flag=ui.TOP|ui.EXPAND, border=5)
        self.color1txtctrl.ChangeValue(str(current_color1_value))

        self.color1btn = ui.Button(parent, label="Select...")
        sizer.Add(self.color1btn, pos=(3, 4), flag=ui.TOP|ui.RIGHT, border=5)

        # Color 2
        current_color2_value = self.NodeGetPropertyValue('Color2')
        self.color2data = ui.ColourData()
        self.color2data.SetColour(current_color2_value)

        color2label = ui.StaticText(parent, label="Color 2: ")
        sizer.Add(color2label, pos=(4, 0), flag=ui.LEFT|ui.TOP, border=10)

        self.color2txtctrl = ui.TextCtrl(parent)
        sizer.Add(self.color2txtctrl, pos=(4, 1), span=(1, 3), flag=ui.TOP|ui.EXPAND, border=5)
        self.color2txtctrl.ChangeValue(str(current_color2_value))

        self.color2btn = ui.Button(parent, label="Select...")
        sizer.Add(self.color2btn, pos=(4, 4), flag=ui.TOP|ui.RIGHT, border=5)

        # X Size
        current_x_value = self.NodeGetPropertyValue('Size')[0]

        x_sizelabel = ui.StaticText(parent, label="X Size:")
        sizer.Add(x_sizelabel, pos=(5, 0), flag=ui.LEFT|ui.TOP, border=10)

        self.x_sizespinctrl = ui.SpinCtrl(parent, -1, "", (30, 50))
        self.x_sizespinctrl.SetRange(1, 8000)
        self.size_x = int(current_x_value)
        self.x_sizespinctrl.SetValue(current_x_value)
        sizer.Add(self.x_sizespinctrl, pos=(5, 1), span=(1, 3), flag=ui.TOP|ui.EXPAND, border=5)

        # Y Size
        current_y_value = self.NodeGetPropertyValue('Size')[1]

        y_sizelabel = ui.StaticText(parent, label="Y Size:")
        sizer.Add(y_sizelabel, pos=(6, 0), flag=ui.LEFT|ui.TOP, border=10)

        self.y_sizespinctrl = ui.SpinCtrl(parent, -1, "", (30, 50))
        self.y_sizespinctrl.SetRange(1, 8000)
        self.size_y = int(current_y_value)
        self.y_sizespinctrl.SetValue(current_y_value)
        sizer.Add(self.y_sizespinctrl, pos=(6, 1), span=(1, 3), flag=ui.TOP|ui.EXPAND, border=5)
 
        parent.Bind(ui.EVT_COMBOBOX, self.EvtGradientChoice, self.gradientcombobox)
        parent.Bind(ui.EVT_BUTTON, self.OnColor1Button, self.color1btn)
        parent.Bind(ui.EVT_BUTTON, self.OnColor2Button, self.color2btn)
        parent.Bind(ui.EVT_SPINCTRL, self.OnXSpin, self.x_sizespinctrl)
        parent.Bind(ui.EVT_SPINCTRL, self.OnYSpin, self.y_sizespinctrl)

    def OnXSpin(self, evt):
        self.size_x = self.x_sizespinctrl.GetValue()
        self.NodePropertiesUpdate('Size', self.GetSize())

    def OnYSpin(self, evt):
        self.size_y = self.y_sizespinctrl.GetValue()
        self.NodePropertiesUpdate('Size', self.GetSize())

    def GetSize(self):
        return [self.size_x, self.size_y]

    def EvtGradientChoice(self, event):
        value = event.GetString()
        if not value:
            return
        self.NodePropertiesUpdate('Gradient', value)

    def OnColor1Button(self, event):
        self.color1dialog = CCD.CubeColourDialog(self.parent, self.color1data)
        if self.color1dialog.ShowModal() == self.ui.ID_OK:

            self.color1data = self.color1dialog.GetColourData()
            colordata = self.color1data.GetColour()
            self.NodePropertiesUpdate(
                'Color1',
                (colordata.Red(),
                 colordata.Green(),
                 colordata.Blue(),
                 colordata.Alpha())
                )
            self.color1txtctrl.ChangeValue(str((colordata.Red(),
                                            colordata.Green(),
                                            colordata.Blue(),
                                            colordata.Alpha()
                                            )))

    def OnColor2Button(self, event):
        self.color2dialog = CCD.CubeColourDialog(self.parent, self.color2data)
        if self.color2dialog.ShowModal() == self.ui.ID_OK:

            self.color2data = self.color2dialog.GetColourData()
            colordata = self.color2data.GetColour()
            self.NodePropertiesUpdate(
                'Color2',
                (colordata.Red(),
                 colordata.Green(),
                 colordata.Blue(),
                 colordata.Alpha())
                )
            self.color2txtctrl.ChangeValue(str((colordata.Red(),
                                            colordata.Green(),
                                            colordata.Blue(),
                                            colordata.Alpha()
                                            )))


    def NodeEvaluation(self, eval_info):
        gradientvalue = eval_info.EvaluateProperty('Gradient')
        color1 = eval_info.EvaluateProperty('Color1')
        color2 = eval_info.EvaluateProperty('Color2')
        imgsize = eval_info.EvaluateProperty('Size')

        gradientimage = Image.new("L", (imgsize[0], 1))
        for x in range(imgsize[0]):
            gradientimage.putpixel((x, 0), int(225. * (1. - float(gradientvalue) * float(x)/imgsize[0])))

        gradient_image = ImageOps.colorize(gradientimage.resize((imgsize[0], imgsize[1])),
                                      color1, color2)
        image = RenderImage()
        image.SetAsImage(gradient_image.convert('RGBA'))
        self.NodeSetThumbnail(image.GetImage())
        return image 



RegisterNode(NodeDefinition)
