import os
import imghdr
from PIL import Image

from GimelStudio.api import (Color, RenderImage, NodeBase,
                         ParameterDefinition, PropertyDefinition,
                         RegisterNode)

 
class NodeDefinition(NodeBase):
    
    @property
    def NodeName(self):
        return "corenode_image"

    @property
    def NodeLabel(self):
        return "Image"

    @property
    def NodeCategory(self):
        return "INPUT"

    @property
    def NodeDescription(self):
        return "Inputs an image from the specified file path." 

    @property
    def NodeVersion(self):
        return "2.0.5" 

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software" 

    @property
    def NodeProperties(self): 
        return [
            PropertyDefinition('Path',
                               prop_type='filepath',
                               value=''
                               ),
        ]

    def NodePropertiesUI(self, node, ui, parent, sizer):
        self.NodePropertiesHelperInit(node, ui, parent, sizer)
        current_value = self.NodeGetPropertyValue('Path')
 
        pathlabel = ui.StaticText(parent, label="Path:")
        sizer.Add(pathlabel, pos=(2, 0), flag=ui.LEFT|ui.TOP, border=10)

        self.pathtxtctrl = ui.TextCtrl(parent)
        sizer.Add(self.pathtxtctrl, pos=(2, 1), span=(1, 3), flag=ui.TOP|ui.EXPAND, border=5)
        self.pathtxtctrl.ChangeValue(current_value)

        self.browsepathbtn = ui.Button(parent, label="Browse...")
        sizer.Add(self.browsepathbtn, pos=(2, 4), flag=ui.TOP|ui.RIGHT, border=5)

        infolabellbl = ui.StaticText(parent, label="Meta: ")
        sizer.Add(infolabellbl, pos=(3, 0), flag=ui.LEFT|ui.TOP, border=10)

        self.infolabellbl = ui.StaticText(parent, label="")
        sizer.Add(self.infolabellbl, pos=(3, 1), flag=ui.LEFT|ui.TOP, border=10)

        if current_value != '':
            self.UpdateInfoLabel(current_value)
            self.infolabellbl.SetLabel(self.GetInfoLabel())

        parent.Bind(ui.EVT_BUTTON, self.OnFilePathButton, self.browsepathbtn)


    def OnFilePathButton(self, evt):
        wildcard = "All files (*.*)|*.*|" \
                   "JPG file (*.jpg)|*.jpg|" \
                   "PNG file (*.png)|*.png|" \
                   "BMP file (*bmp)|*bmp"

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

            filename_ext = imghdr.what(paths[0])
            if filename_ext in ['jpg', 'jpeg', 'bmp', 'png']:
                self.NodePropertiesUpdate('Path', paths[0])
                self.pathtxtctrl.ChangeValue(paths[0])
                self.UpdateInfoLabel(paths[0])
                self.infolabellbl.SetLabel(self.GetInfoLabel())
            else:
                dlg = self.ui.MessageDialog(
                    None, 
                    "That file type isn't currently supported!", 
                    "Cannot Open File!", 
                    style=self.ui.ICON_EXCLAMATION
                    )
                dlg.ShowModal()
                return False       

    def UpdateInfoLabel(self, imagepath):
        try:
            img = Image.open(imagepath)
            info_string = "{}x{}px | {} | {}kB".format(
                img.size[0], 
                img.size[1],
                img.mode,
                str(os.path.getsize(imagepath)/1000)
                )
            self.infolabel = info_string
        except FileNotFoundError:
            self.infolabel = 'IMAGE COULD NOT FOUND!'

    def GetInfoLabel(self):
        return self.infolabel


    def NodeEvaluation(self, eval_info):
        path = eval_info.EvaluateProperty('Path')
        #print('p->', path)
        image = RenderImage()
        if path != '':
            try:
                image.SetAsOpenedImage(path)
                image.SetAsImage(image.GetImage().convert('RGBA'))
            except FileNotFoundError:
                pass

        self.NodeSetThumbnail(image.GetImage())
        return image 



RegisterNode(NodeDefinition)
