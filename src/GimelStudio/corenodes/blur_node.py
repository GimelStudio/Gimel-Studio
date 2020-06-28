
import wx
from PIL import Image, ImageFilter

from GimelStudio.api import (Color, RenderImage, List, NodeBase, ParameterDefinition,
                         PropertyDefinition, RegisterNode)

 
class NodeDefinition(NodeBase):
    
    @property
    def NodeIDName(self):
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
                               prop_type='INTEGER',
                               value=2
                               ),
            ]

    @property
    def NodeParameters(self):
        return [
            ParameterDefinition('Image',
                                param_type='RENDERIMAGE',
                                default_value=RenderImage('RGBA', (256, 256), (0, 0, 0, 1))),
        ]


  
    def NodePropertiesUI(self, node, parent, sizer):


        inner_sizer = wx.BoxSizer(wx.HORIZONTAL)

        flagsExpand = wx.SizerFlags(1)
        flagsExpand.Expand().Border(wx.ALL, 10)

        current_radius_value = self.NodeGetPropertyValue('Radius')

        radius_label = wx.StaticText(parent, label="Blur Radius:")
        inner_sizer.Add(radius_label, flagsExpand)

        self.radiusspinctrl = wx.Slider(
            parent, 100, 25, 1, 100, size=(250, -1),
            style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
            )

        self.radiusspinctrl.SetTickFreq(5)

        self.radiusspinctrl.SetRange(1, 100)
        self.radiusspinctrl.SetValue(current_radius_value)
        inner_sizer.Add(self.radiusspinctrl, flagsExpand)

        sizer.Add(inner_sizer)

        parent.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.OnRadiusSpin, self.radiusspinctrl)


    def OnRadiusSpin(self, evt):
        self.NodePropertiesUpdate('Radius', self.radiusspinctrl.GetValue())
    
    def NodeEvaluation(self, eval_info):
        image1 = eval_info.EvaluateParameter('Image')

        # Get the values
        Radius = eval_info.EvaluateProperty('Radius')
        
        image = RenderImage()
        image.SetAsImage(image1.GetImage().filter(ImageFilter.GaussianBlur(Radius)).convert('RGBA'))
        #self.NodeSetThumbnail(image.GetImage())
        return image


RegisterNode(NodeDefinition)
