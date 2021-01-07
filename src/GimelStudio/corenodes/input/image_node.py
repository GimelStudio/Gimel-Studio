# THIS FILE IS A PART OF GIMEL STUDIO AND IS LICENSED UNDER THE SAME TERMS:
# ----------------------------------------------------------------------------
# Gimel Studio Copyright 2019-2020 by Noah Rahm and contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------------

import os

from GimelStudio import api
from GimelStudio.renderer import EvalInfo


class ImageNode(api.NodeBase):
    def __init__(self, _id):
        api.NodeBase.__init__(self, _id)

        self._cachedPath = ""
        self._cachedImage = None

    @property
    def NodeMeta(self):
        meta_info = {
            "label": "Image",
            "author": "Correct Syntax",
            "version": (3, 1, 0),
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
        if idname == 'File Path':
            img = self.EvaluateSelf().GetImage()

            info_string = "{}x{}px | RGBA | {}kB".format(
                img.shape[0],
                img.shape[1],
                str(os.path.getsize(value) / 1000)
            )
            self.lbl_prop.SetValue(info_string)
            self.RefreshPropertyPanel()

            self.NodeSetThumb(img, force_refresh=True)

    def NodeEvaluation(self, params, props):
        path = props["File Path"]

        render_image = api.RenderImage()

        if path != "":
            if self._cachedPath != path:
                try:
                    render_image.SetAsOpenedImage(path)
                    img = render_image.GetImage()
                    self._cachedPath = path
                    self._cachedImage = img
                    render_image.SetAsImage(img)
                except FileNotFoundError:
                    print("WARNING: FILE NOT FOUND!")
            else:
                render_image.SetAsImage(self._cachedImage)

        return render_image


api.RegisterNode(ImageNode, "corenode_image")
