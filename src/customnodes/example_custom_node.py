import os
from PIL import Image

from GimelStudio.api import (Color, RenderImage, NodeBase,
                             ParameterDefinition, PropertyDefinition,
                             RegisterNode)

 
class NodeDefinition(NodeBase):
    
    @property
    def NodeName(self):
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
        return "1.0.0" 

    @property
    def NodeAuthor(self):
        return "[author's name]"

    @property
    def NodeProperties(self): 
        return [
            PropertyDefinition('path',
                               prop_type='filepath',
                               value=''
                               ),
        ]

    def NodePropertiesUI(self, node, ui, parent, sizer):
        self.NodePropertiesHelperInit(node, ui, parent, sizer)
        current_value = self.NodeGetPropertyValue('path')
 
        pathlabel = ui.StaticText(parent, label="Path:")
        sizer.Add(pathlabel, pos=(2, 0), flag=ui.LEFT|ui.TOP, border=10)

        self.pathtxtctrl = ui.TextCtrl(parent)
        sizer.Add(self.pathtxtctrl, pos=(2, 1), span=(1, 3), flag=ui.TOP|ui.EXPAND, border=5)
        self.pathtxtctrl.ChangeValue(current_value)

        self.browsepathbtn = ui.Button(parent, label="Browse...")
        sizer.Add(self.browsepathbtn, pos=(2, 4), flag=ui.TOP|ui.RIGHT, border=5)

        parent.Bind(ui.EVT_BUTTON, self.OnFilePathButton, self.browsepathbtn)

    def OnFilePathButton(self, evt):
        wildcard = "JPG file (*.jpg)|*.jpg|" \
                   "PNG file (*.png)|*.png|" \
                   "All files (*.*)|*.*"
                   
        dlg = self.ui.FileDialog(
            self.parent, message="Choose an Image",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=self.ui.FD_OPEN | self.ui.FD_CHANGE_DIR | self.ui.FD_FILE_MUST_EXIST | self.ui.FD_PREVIEW
            )

        # Show the dialog and retrieve the user response. If it is the OK response,
        # process the data.
        if dlg.ShowModal() == self.ui.ID_OK:
            # This returns a Python list of files that were selected.
            paths = dlg.GetPaths()
            self.NodePropertiesUpdate('path', paths[0])
            self.pathtxtctrl.ChangeValue(paths[0])

    def NodeEvaluation(self, eval_info):
        path = eval_info.EvaluateProperty('path')
        image = RenderImage()
        if path != '':
            image.SetAsOpenedImage(path)
        image.SetAsImage(image.GetImage().convert('RGBA'))
        self.NodeSetThumbnail(image.GetImage())
        return image 



RegisterNode(NodeDefinition)
