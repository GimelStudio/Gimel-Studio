import wx
from PIL import Image, ImageFilter

from GimelStudio.api import (Color, RenderImage, List, NodeBase, 
                            Parameter, Property, RegisterNode)

 
class NodeDefinition(NodeBase):
    
    @property
    def NodeIDName(self):
        return "box_blur_node"

    @property
    def NodeLabel(self):
        return "Box Blur"

    @property
    def NodeCategory(self):
        return "FILTER"

    @property
    def NodeDescription(self):
        return "Blurs the given image using the specified blur radius with the Box algorithm." 

    @property
    def NodeVersion(self):
        return "1.0" 

    @property
    def NodeAuthor(self):
        return "Your name!" 

    @property
    def NodeProperties(self):
        return [
            Property('Radius',
                prop_type='INTEGER',
                value=4
                ),
            ]

    @property
    def NodeParameters(self):
        return [
            Parameter('Image',
                param_type='RENDERIMAGE',
                default_value=RenderImage('RGBA', (256, 256), (0, 0, 0, 1))
                ),
        ]

   
    def NodePropertiesUI(self, node, parent, sizer):
        # Get the current property value
        current_radius_value = self.NodeGetPropValue('Radius')

        # wxPython stuff...
        radius_label = wx.StaticText(parent, label="Blur Radius:")
        sizer.Add(radius_label, border=5)

        self.radius_slider = wx.Slider(
            parent, 100, 25, 1, 100,
            style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
            )
        self.radius_slider.SetTickFreq(5)
        self.radius_slider.SetRange(1, 100)
        self.radius_slider.SetValue(current_radius_value)
        sizer.Add(self.radius_slider, flag=wx.EXPAND|wx.ALL, border=5)

        parent.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.OnRadiusChange, self.radius_slider)

    def OnRadiusChange(self, evt):
        # Update the node property "Radius" to be the value that was set
        self.NodePropertiesUpdate('Radius', self.radius_slider.GetValue())
    
    def NodeEvaluation(self, eval_info):
        # Get the parameter
        image1  = eval_info.EvaluateParameter('Image')
        # Get the property
        radius = eval_info.EvaluateProperty('Radius')

        # Just like before, except we edit the image with
        # Pillow's ImageFilter.BoxBlur method
        image = RenderImage()
        image.SetAsImage(image1.GetImage().filter(
            ImageFilter.BoxBlur(radius)
            ).convert('RGBA'))
        self.NodeSetThumb(image.GetImage())
        return image

 
RegisterNode(NodeDefinition)
