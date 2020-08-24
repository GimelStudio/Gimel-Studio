import os

import wx
from PIL import Image

from GimelStudio.api import (Color, RenderImage, List, NodeBase, 
                            Parameter, Property, RegisterNode)

  
class NodeDefinition(NodeBase):
    
    @property
    def NodeIDName(self):
        return "gimelstudiocorenode_noiseimage"

    @property
    def NodeLabel(self):
        return "Noise Image"

    @property
    def NodeCategory(self):
        return "INPUT"
 
    @property
    def NodeDescription(self):
        return "Generates a Gaussian noise image centered around 128." 

    @property
    def NodeVersion(self):
        return "1.0" 

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software" 

    @property
    def NodeProperties(self):
        return [
            Property('Sigma',
                prop_type='INTEGER',
                value=50
                ),
            Property('Size',
                prop_type='REGLIST',
                value=[256, 256]
                ),
            ]


    def NodePropertiesUI(self, node, parent, sizer):

        # Sigma
        current_sigma_value = self.NodeGetPropValue('Sigma')
        
        sigma_label = wx.StaticText(parent, label="Sigma:")
        sizer.Add(sigma_label, border=5)

        self.sigma_slider = wx.Slider(
            parent, wx.ID_ANY,
            style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
            )
        self.sigma_slider.SetTickFreq(10)
        self.sigma_slider.SetRange(1, 500)
        self.sigma_slider.SetValue(current_sigma_value)
        sizer.Add(self.sigma_slider, flag=wx.EXPAND|wx.ALL, border=5)

        # Size
        current_x_value = self.NodeGetPropValue('Size')[0]

        xsize_label = wx.StaticText(parent, label="X:")
        sizer.Add(xsize_label, flag=wx.TOP, border=5)

        self.xsize_spinctrl = wx.SpinCtrl(
            parent, id=wx.ID_ANY, 
            min=1, max=8000,
            initial=int(current_x_value)
            )
        self.size_x = int(current_x_value)
        sizer.Add(self.xsize_spinctrl, flag=wx.ALL|wx.EXPAND, border=5)


        # Y Size
        current_y_value = self.NodeGetPropValue('Size')[1]

        ysize_label = wx.StaticText(parent, label="Y:")
        sizer.Add(ysize_label, flag=wx.TOP, border=5)

        self.ysize_spinctrl = wx.SpinCtrl(
            parent, id=wx.ID_ANY, 
            min=1, max=8000,
            initial=int(current_y_value)
            )
        self.size_y = int(current_y_value)
        sizer.Add(self.ysize_spinctrl, flag=wx.ALL|wx.EXPAND, border=5)
        
        # Bindings
        parent.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.OnSigmaChange, self.sigma_slider)
        parent.Bind(wx.EVT_SPINCTRL, self.OnXSizeChange, self.xsize_spinctrl)
        parent.Bind(wx.EVT_SPINCTRL, self.OnYSizeChange, self.ysize_spinctrl)
        parent.Bind(wx.EVT_TEXT, self.OnXSizeChange, self.xsize_spinctrl)
        parent.Bind(wx.EVT_TEXT, self.OnYSizeChange, self.ysize_spinctrl)

    def OnSigmaChange(self, event):
        self.NodePropertiesUpdate('Sigma', self.sigma_slider.GetValue())

    def OnXSizeChange(self, event):
        self.size_x = self.xsize_spinctrl.GetValue()
        self.NodePropertiesUpdate('Size', self.GetSize())

    def OnYSizeChange(self, event):
        self.size_y = self.ysize_spinctrl.GetValue()
        self.NodePropertiesUpdate('Size', self.GetSize())

    def GetSize(self):
        return [self.size_x, self.size_y]
     
    def NodeEvaluation(self, eval_info):
        sigma = eval_info.EvaluateProperty('Sigma')
        imgsize = eval_info.EvaluateProperty('Size')

        image = RenderImage()
        image.SetAsImage(
            Image.effect_noise((imgsize[0], imgsize[1]), sigma).convert("RGBA")
            )
        self.NodeSetThumb(image.GetImage())
        return image

 
RegisterNode(NodeDefinition)