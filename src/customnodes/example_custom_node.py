import os

import wx
from PIL import Image

from GimelStudio.api import (Color, RenderImage, NodeBase,
                             Parameter, Property,
                             RegisterNode)

 
class NodeDefinition(NodeBase):
    
    @property
    def NodeIDName(self):
        return "example_custom_node"

    @property
    def NodeLabel(self):
        return "Example Custom Node"

    @property
    def NodeCategory(self):
        return "INPUT"

    @property
    def NodeDescription(self):
        return "This is an example custom node showing how you can\n create a custom node with the Gimel Studio API" 

    @property
    def NodeVersion(self):
        return "1.1" 

    @property
    def NodeAuthor(self):
        return "[author's name]"

    @property
    def NodeProperties(self): 
        return [
            Property('Path',
                prop_type='FILEPATH',
                value=''
                ),
        ]

    def NodePropertiesUI(self, node, parent, sizer):
        self.parent = parent
        
        current_value = self.NodeGetPropValue('Path')
 
        pathlabel = wx.StaticText(parent, label="Path:")
        sizer.Add(pathlabel, flag=wx.LEFT|wx.TOP, border=5)

        self.pathtxtctrl = wx.TextCtrl(parent)
        sizer.Add(self.pathtxtctrl, flag=wx.TOP|wx.EXPAND, border=5)
        self.pathtxtctrl.ChangeValue(current_value)

        self.browsepathbtn = wx.Button(parent, label="Browse...")
        sizer.Add(self.browsepathbtn, flag=wx.TOP|wx.RIGHT, border=5)

        parent.Bind(wx.EVT_BUTTON, self.OnFilePathButton, self.browsepathbtn)

    def OnFilePathButton(self, evt):
        # We allow opening only .jpg files here (for fun!)
        wildcard = "JPG file (*.jpg)|*.jpg|"
                   
        dlg = wx.FileDialog(
            self.parent, message="Choose an Image...",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW
            )

        # Show the dialog and retrieve the user response. If it is the OK response,
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            paths = dlg.GetPaths()

            # Update the property and txtctrl with the new file path
            self.NodePropertiesUpdate('Path', paths[0])
            self.pathtxtctrl.ChangeValue(paths[0])

    def NodeEvaluation(self, eval_info):
        # Get the file path from the property
        path = eval_info.EvaluateProperty('Path')

        image = RenderImage()
        if path != '':
            image.SetAsOpenedImage(path)
        image.SetAsImage(image.GetImage().convert('RGBA'))
        self.NodeSetThumb(image.GetImage())
        return image 


RegisterNode(NodeDefinition)
