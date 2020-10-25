## THIS FILE IS A PART OF GIMEL STUDIO AND IS LICENSED UNDER THE SAME TERMS:
## ----------------------------------------------------------------------------
## Gimel Studio Copyright 2019-2020 by Noah Rahm and contributors
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##    http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
## ----------------------------------------------------------------------------

import os
from PIL import Image

from GimelStudio import api
from GimelStudio.renderer import EvalInfo


class ImageNode(api.NodeBase):
    def __init__(self, _id):
        api.NodeBase.__init__(self, _id)

        self._cachedPath = ""

    @property
    def NodeMeta(self):
        meta_info = {
            "label": "Image",
            "author": "Correct Syntax",
            "version": (3, 0, 5),
            "supported_app_version": (0, 5, 0),
            "category": "INPUT",
            "description": "Loads an image from the specified file path."
        }
        return meta_info

    def NodeInitProps(self):
        wildcard = "All files (*.*)|*.*|" \
                "JPEG file (*.jpeg)|*.jpeg|" \
                "JPG file (*.jpg)|*.jpg|" \
                "PNG file (*.png)|*.png|" \
                "BMP file (*.bmp)|*.bmp|" \
                "WEBP file (*.webp)|*.webp|" \
                "TGA file (*.tga)|*.tga|" \
                "TIFF file (*.tiff)|*.tiff"

        self.fp_prop = api.OpenFileChooserProp(
            idname="File Path",
            default="",
            dlg_msg="Choose image...",
            wildcard=wildcard,
            btn_lbl="Choose...",
            label="Image path:"
            )
        self.lbl_prop = api.LabelProp(
            idname="Meta Info",
            default="",
            label="Meta info:"
            )

        self.NodeAddProp(self.fp_prop)
        self.NodeAddProp(self.lbl_prop)

    def WidgetEventHook(self, idname, value):
    #     pass
        # import time
        # t = time.time()
        if idname == 'File Path':
            img = self.NodeEvaluation(EvalInfo(self)).GetImage() #Image.open(value) #

            info_string = "{}x{}px | {} | {}kB".format(
                img.size[0],
                img.size[1],
                img.mode,
                str(os.path.getsize(value)/1000)
                )
            self.lbl_prop.SetValue(info_string)
            self.RefreshPropertyPanel()

            self.NodeSetThumb(img, force_refresh=True)

        # print(">>>", time.time() - t)

    def NodeEvaluation(self, eval_info):
        path = eval_info.EvaluateProperty('File Path')
        image = api.RenderImage()

        if path != "":
            if self._cachedPath != path:
                try:
                    image.SetAsOpenedImage(path)
                    img = image.GetImage().convert('RGBA')
                    self._cachedPath = path
                    self._cachedImage = img
                    image.SetAsImage(img)
                except FileNotFoundError:
                    print("FILE NOT FOUND")
            else:
                image.SetAsImage(self._cachedImage)

        # if path != '':
        #     try:
        #         image.SetAsOpenedImage(path)
        #         image.SetAsImage(image.GetImage().convert('RGBA'))
        #     except FileNotFoundError:
        #         pass

        self.NodeSetThumb(image.GetImage())
        return image


api.RegisterNode(ImageNode, "corenode_image")