## THIS FILE IS A PART OF GIMEL STUDIO AND IS LICENSED UNDER THE SAME TERMS:
## ----------------------------------------------------------------------------
## Gimel Studio Copyright 2020 Noah Rahm, Correct Syntax. All rights reserved.
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


import wx
import wx.adv
from PIL import Image, ImageDraw, ImageFont

from GimelStudio.api import (Color, RenderImage, List, NodeBase, 
                            Parameter, Property, RegisterNode)


class SystemFontsComboBox(wx.adv.OwnerDrawnComboBox):
    """ This ComboBox class graphically displays the various fonts that are available on the user's system, making it easy for the user to choose the font they want.
    """

    # Overridden from OwnerDrawnComboBox, called to draw each
    # item in the list
    def OnDrawItem(self, dc, rect, item, flags):
        if item == wx.NOT_FOUND:
            # painting the control, but there is no valid item selected yet
            return

        r = wx.Rect(*rect)  # make a copy
        r.Deflate(3, 5)

        if flags & wx.adv.ODCB_PAINTING_CONTROL:

            # for painting the control itself
            dc.DrawText(self.GetString(item),
                        r.x+5, r.y+r.height/2 - (dc.GetCharHeight()/2)
                        )

        else:
            # for painting the items in the popup
            dc.SetFont(wx.Font(wx.FontInfo(12).FaceName(self.GetString(item))))

            dc.DrawText(self.GetString( item ),
                        r.x + 3,
                        (r.y + 0) + ( (r.height/2) - (dc.GetCharHeight()/2) )/2
                        )

    # Overridden from OwnerDrawnComboBox, called for drawing the
    # background area of each item.
    def OnDrawBackground(self, dc, rect, item, flags):
        # If the item is selected, or its item # iseven, or we are painting the
        # combo control itself, then use the default rendering.
        if (item & 1 == 0 or flags & (wx.adv.ODCB_PAINTING_CONTROL |
                                      wx.adv.ODCB_PAINTING_SELECTED)):
            wx.adv.OwnerDrawnComboBox.OnDrawBackground(self, dc, rect, item, flags)
            return

    # Overridden from OwnerDrawnComboBox, should return the height
    # needed to display an item in the popup, or -1 for default
    def OnMeasureItem(self, item):
        return 34

    # Overridden from OwnerDrawnComboBox.  Callback for item width, or
    # -1 for default/undetermined
    def OnMeasureItemWidth(self, item):
        return -1; # default - will be measured from text width


 
class NodeDefinition(NodeBase):
    
    @property
    def NodeIDName(self):
        return "gimelstudiocorenode_addtext"

    @property
    def NodeLabel(self):
        return "Add Text"

    @property
    def NodeCategory(self):
        return "DRAW"

    @property
    def NodeDescription(self):
        return "Adds text to the image." 

    @property
    def NodeVersion(self):
        return "1.0" 

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software" 

    @property
    def NodeProperties(self):
        return [
            Property('Text',
                prop_type='STRING',
                value='hello'
                ), 
            Property('Font',
                prop_type='STRING',
                value=''
                ), 
            Property('Font Size',
                prop_type='INTEGER',
                value=14
                ), 
            Property('Text Fill Color',
                prop_type='COLOR',
                value=(0, 0, 0, 255)
                ), 
            Property('Text Stroke Width',
                prop_type='INTEGER',
                value=1
                ), 
            Property('Text Stroke Fill Color',
                prop_type='COLOR',
                value=(0, 0, 0, 255)
                ), 
            Property('Coordinates',
                prop_type='REGLIST',
                value=[0, 0]
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

        # Get the system fonts
        font_enumerator = wx.FontEnumerator()
        font_enumerator.EnumerateFacenames()
        font_styles_list = font_enumerator.GetFacenames()
        font_styles_list.sort()

        # Get current values
        current_text_value = self.NodeGetPropValue('Text')
        current_font_value = self.NodeGetPropValue('Font')
        current_font_size = self.NodeGetPropValue('Font Size')

        # Text
        text_label = wx.StaticText(parent, label="Text:")
        sizer.Add(text_label, border=5)

        self.text_textctrl = wx.TextCtrl(parent, 
                        wx.ID_ANY, current_text_value, 
                        size=(200, 100), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        sizer.Add(self.text_textctrl, flag=wx.EXPAND|wx.ALL, border=5)

        # Font
        font_label = wx.StaticText(parent, label="Font:")
        sizer.Add(font_label, border=5)

        self.font_combobox = SystemFontsComboBox(parent, 
                        choices=font_styles_list, 
                        style=wx.CB_READONLY
                        )
        self.font_combobox.SetValue(current_font_value)
        sizer.Add(self.font_combobox, flag=wx.EXPAND|wx.ALL, border=5)

        # Font size
        self.font_size_slider = wx.Slider(
            parent, wx.ID_ANY,
            style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
            )
        self.font_size_slider.SetTickFreq(20)
        self.font_size_slider.SetRange(1, 1000)
        self.font_size_slider.SetValue(current_font_size)
        sizer.Add(self.font_size_slider, flag=wx.EXPAND|wx.ALL, border=5)



        parent.Bind(wx.EVT_COMBOBOX, self.OnFontChange, self.font_combobox)
        parent.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.OnFontSizeChange, self.font_size_slider)
        parent.Bind(wx.EVT_TEXT, self.OnTextChange, self.text_textctrl)

    def OnTextChange(self, event):
        self.NodePropertiesUpdate('Text', self.text_textctrl.GetValue())
 
    def OnFontChange(self, event):
        print(self.font_combobox.GetValue())
        self.NodePropertiesUpdate('Font', self.font_combobox.GetValue())

    def OnFontSizeChange(self, evt):
        self.NodePropertiesUpdate('Font Size', self.font_size_slider.GetValue())
    
    def NodeEvaluation(self, eval_info):
        image1  = eval_info.EvaluateParameter('Image')
        text = eval_info.EvaluateProperty('Text')
        font = eval_info.EvaluateProperty('Font')
        font_size = eval_info.EvaluateProperty('Font Size')
        text_fill = eval_info.EvaluateProperty('Text Fill Color')
        text_stroke_fill = eval_info.EvaluateProperty('Text Stroke Fill Color')
        text_stroke_width = eval_info.EvaluateProperty('Text Stroke Width')

        # Draw text on the image
        img = image1.GetImage().copy()
        draw_text = ImageDraw.Draw(img)

        # Get the coordinates for applying the text to the image
        x = 1
        y = 1

        path = ""
        print(font, "????")
        text_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf".format(font.lower()), font_size)

        # Draw the text
        draw_text.text(
            xy=(x, y), 
            text=text, 
            font=text_font, 
            fill=text_fill, 
            spacing=6, 
            align='left', 
            stroke_width=text_stroke_width, 
            stroke_fill=text_stroke_fill
            )
 
        image = RenderImage()
        image.SetAsImage(img)
        self.NodeSetThumb(image.GetImage())
        return image

 
RegisterNode(NodeDefinition)
