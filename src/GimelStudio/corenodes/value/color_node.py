from PIL import Image
import wx.lib.agw.cubecolourdialog as CCD


from GimelStudio.api import (Color, RenderImage, NodeBase,
                         ParameterDefinition, PropertyDefinition,
                         RegisterNode)
 
class NodeDefinition(NodeBase):
     
    @property
    def NodeName(self):
        return "color"
 
    @property
    def NodeLabel(self):
        return "Color" 

    @property
    def NodeCategory(self):
        return "VALUE"

    @property
    def NodeDescription(self):
        return "Inputs an RGBA color." 

    @property
    def NodeVersion(self):
        return "1.0.0" 

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software" 

    @property
    def NodeOutput(self):
        return "color"

    @property
    def NodeProperties(self):
        return [
            PropertyDefinition('color',
                               prop_type='color',
                               value=Color(0.0, 0.0, 0.0, 1.0)
                               ),
        ]

    def NodePropertiesUI(self, node, ui, parent, sizer):
        self.NodePropertiesHelperInit(node, ui, parent, sizer)

        current_value = self.NodeGetPropertyValue('color')
        if type(current_value) != tuple:
            current_value = self.NodeGetPropertyValue('color').GetColors()

        self.colourdata = ui.ColourData()
        self.colourdata.SetColour(current_value)

        colorlabel = ui.StaticText(parent, label="Value: ")
        sizer.Add(colorlabel, pos=(2, 0), flag=ui.LEFT|ui.TOP, border=10)

        self.colortxtctrl = ui.TextCtrl(parent)
        sizer.Add(self.colortxtctrl, pos=(2, 1), span=(1, 3), flag=ui.TOP|ui.EXPAND, border=5)
        self.colortxtctrl.ChangeValue(str(current_value))

        self.colorbtn = ui.Button(parent, label="Select...")
        sizer.Add(self.colorbtn, pos=(2, 4), flag=ui.TOP|ui.RIGHT, border=5)

        parent.Bind(ui.EVT_BUTTON, self.OnColorButton, self.colorbtn)


    def OnColorButton(self, event):
        self.colordialog = CCD.CubeColourDialog(self.parent, self.colourdata)
        if self.colordialog.ShowModal() == self.ui.ID_OK:

            self.colourdata = self.colordialog.GetColourData()
            colourdata = self.colourdata.GetColour()
            self.NodePropertiesUpdate(
                'color',
                (colourdata.Red(),
                 colourdata.Green(),
                 colourdata.Blue(),
                 colourdata.Alpha())
                )
            self.colortxtctrl.ChangeValue(str((colourdata.Red(),
                                               colourdata.Green(),
                                               colourdata.Blue(),
                                               colourdata.Alpha()
                                               )))

##            self.node.SetLabel('Color {}'.format(str((colourdata.Red(),
##                                                       colourdata.Green(),
##                                                       colourdata.Blue(),
##                                                       colourdata.Alpha()
##                                                       ))))
            

    def NodeEvaluation(self, eval_info):
        colors = eval_info.EvaluateProperty('color')
        if type(colors) != tuple:
            color = colors
            self.NodeSetThumbnail(Image.new('RGBA', (50, 50), colors.GetColors()))

        else:
            color = Color(colors[0], colors[1], colors[2], colors[3])
            self.NodeSetThumbnail(Image.new('RGBA', (50, 50), (colors[0], colors[1], colors[2], colors[3])))
        return color 


RegisterNode(NodeDefinition)
