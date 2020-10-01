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
##
## FILE: property.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the base node property class and specific property types
## ----------------------------------------------------------------------------

import os

import wx
from wx.lib import buttons
import wx.lib.agw.cubecolourdialog as CCD

# Enum-like constants for widgets
SLIDER_WIDGET = "slider"
SPINBOX_WIDGET = "spinbox"


class Property(object):
    def __init__(self, idname, default, label, visible=True):
        self.idname = idname
        self.value = default
        self.label = label
        self.visible = visible
        self.widget_eventhook = None

    def _RunErrorCheck(self):
        pass

    @property
    def IdName(self): #name
        return self.idname

    def GetIdname(self):
        return self.idname

    def GetValue(self):
        return self.value

    def SetValue(self, value, render=True):
        """ Set the value of the node property.

        NOTE: This is only to be used to AFTER the node init.
        Use ``self.EditProperty`` for other cases, instead.
        """
        self.value = value
        self._RunErrorCheck()
        self.WidgetEventHook(self.idname, self.value, render)

    def GetLabel(self):
        return self.label

    def SetLabel(self, label):
        self.label = label

    def GetIsVisible(self):
        return self.visible

    def SetWidgetEventHook(self, event_hook):
        self.widget_eventhook = event_hook

    def WidgetEventHook(self, idname, value, render):
        self.widget_eventhook(idname, value, render)


class PositiveIntegerProp(Property):
    """ Allows the user to select a positive integer. """
    def __init__(self, idname, default=0, min_val=0,
                max_val=10, widget="slider", label="", visible=True):
        Property.__init__(self, idname, default, label, visible)
        self.min_value = min_val
        self.max_value = max_val
        self.widget = widget

        self._RunErrorCheck()

    def _RunErrorCheck(self):
        if self.value > self.max_value:
            raise TypeError(
        "PositiveIntegerField value must be set to an integer less than 'max_val'"
        )
        if self.value < self.min_value:
            raise TypeError(
        "PositiveIntegerField value must be set to an integer greater than 'min_val'"
        )

    def GetMinValue(self):
        return self.min_value

    def GetMaxValue(self):
        return self.max_value

    def CreateUI(self, parent, sizer):
        label = wx.StaticText(parent, label=self.GetLabel())
        sizer.Add(label, flag=wx.LEFT|wx.TOP, border=5)

        if self.widget == "slider":
            self.slider = wx.Slider(
                parent,
                id=wx.ID_ANY,
                value=self.GetValue(),
                minValue=self.GetMinValue(),
                maxValue=self.GetMaxValue(),
                style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
                )
            self.slider.SetTickFreq(10)
            sizer.Add(self.slider, flag=wx.EXPAND|wx.ALL, border=5)
            self.slider.Bind(
                wx.EVT_SCROLL_THUMBRELEASE,
                self.WidgetEvent
                )

        elif self.widget == "spinbox":
            self.spinbox = wx.SpinCtrl(
                parent,
                id=wx.ID_ANY,
                min=self.GetMinValue(),
                max=self.GetMaxValue(),
                initial=self.GetValue()
                )
            sizer.Add(self.spinbox, flag=wx.ALL|wx.EXPAND, border=5)
            self.spinbox.Bind(
                wx.EVT_SPINCTRL,
                self.WidgetEvent
                )
            self.spinbox.Bind(
                wx.EVT_TEXT,
                self.WidgetEvent
                )

        else:
            raise TypeError(
        "PositiveIntegerField 'widget' param must be either: 'spinbox' or 'slider'!"
        )

    def WidgetEvent(self, event):
        if self.widget == "slider":
            self.SetValue(self.slider.GetValue())
        elif self.widget == "spinbox":
            self.SetValue(self.spinbox.GetValue())


class ChoiceProp(Property):
    """ Allows the user to select from a list of choices. """
    def __init__(self, idname, default="", choices=[], label="", visible=True):
        Property.__init__(self, idname, default, label, visible)
        self.choices = choices

        self._RunErrorCheck()

    def GetChoices(self):
        return self.choices

    def CreateUI(self, parent, sizer):
        label = wx.StaticText(parent, label=self.GetLabel())
        sizer.Add(label, flag=wx.LEFT|wx.TOP, border=5)

        self.combobox = wx.ComboBox(
            parent,
            id=wx.ID_ANY,
            value=self.GetValue(),
            choices=self.GetChoices(),
            style=wx.CB_READONLY
            )
        sizer.Add(self.combobox, flag=wx.EXPAND|wx.ALL, border=5)
        self.combobox.Bind(
            wx.EVT_COMBOBOX,
            self.WidgetEvent
            )

    def WidgetEvent(self, event):
        value = event.GetString()
        if not value:
            return
        self.SetValue(value)


class BooleanProp(Property):
    """ Allows the user to select a True or False value. """
    def __init__(self, idname, default=False, cb_label="Boolean",
                label="", visible=True):
        Property.__init__(self, idname, default, label, visible)
        self.cb_label = cb_label

        self._RunErrorCheck()

    def GetCBLabel(self):
        return self.cb_label

    def CreateUI(self, parent, sizer):
        label = wx.StaticText(parent, label=self.GetLabel())
        sizer.Add(label, flag=wx.LEFT|wx.TOP, border=5)

        self.checkbox = wx.CheckBox(
            parent,
            id=wx.ID_ANY,
            label=self.GetCBLabel()
            )
        self.checkbox.SetValue(self.GetValue())
        sizer.Add(self.checkbox, flag=wx.EXPAND|wx.ALL, border=5)
        self.checkbox.Bind(
            wx.EVT_CHECKBOX,
            self.WidgetEvent
            )

    def WidgetEvent(self, event):
        self.SetValue(event.IsChecked())


class ColorProp(Property):
    """ Allows the user to select an RGBA color. """
    def __init__(self, idname, default=(0, 0, 0, 255), label="", visible=True):
        Property.__init__(self, idname, default, label, visible)

        self._RunErrorCheck()

    def _RunErrorCheck(self):
        if len(self.value) < 4 or type(self.value) != tuple:
            raise TypeError("ColorField value must be an RGBA tuple!")

    def CreateUI(self, parent, sizer):
        self.colordata = wx.ColourData()
        self.colordata.SetColour(self.GetValue())

        label = wx.StaticText(parent, label=self.GetLabel())
        sizer.Add(label, flag=wx.TOP, border=5)

        color_vbox = wx.BoxSizer(wx.VERTICAL)
        color_hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.button = buttons.GenButton(
            parent,
            wx.ID_ANY
            )
        self.button.SetBezelWidth(0)
        self.CalcBtnUpdate(self.colordata.GetColour())
        color_hbox.Add(self.button, flag=wx.LEFT, border=5)
        self.button.Bind(
            wx.EVT_BUTTON,
            self.WidgetEvent
            )

        color_vbox.Add(color_hbox, flag=wx.EXPAND)
        sizer.Add(color_vbox, flag=wx.ALL|wx.EXPAND, border=5)

    def WidgetEvent(self, event):
        self.colordialog = CCD.CubeColourDialog(None, self.colordata)
        if self.colordialog.ShowModal() == wx.ID_OK:
            self.colordata = self.colordialog.GetColourData()
            colordata = self.colordata.GetColour()
            self.SetValue((
                colordata.Red(),
                colordata.Green(),
                colordata.Blue(),
                colordata.Alpha()
                ))
            self.CalcBtnUpdate(colordata)

    def CalcBtnUpdate(self, color):
        self.button.SetBackgroundColour(wx.Colour(color))
        self.button.SetLabel(str(" {} ".format(color)))

        if color.Red() > 128 and color.Green() > 128 and color.Blue() > 128:
            self.button.SetForegroundColour(wx.Colour("#000"))
        else:
            self.button.SetForegroundColour(wx.Colour("#fff"))


class OpenFileChooserProp(Property):
    """ Allows the user to select a file to open.

    (e.g: use this to open an .PNG, .JPG, .JPEG image, etc.)
    """
    def __init__(self, idname, default="", dlg_msg="Choose file...",
                wildcard="All files (*.*)|*.*", btn_lbl="Choose...",
                label="", visible=True):
        Property.__init__(self, idname, default, label, visible)
        self.dlg_msg = dlg_msg
        self.wildcard = wildcard
        self.btn_lbl = btn_lbl

        self._RunErrorCheck()

    def _RunErrorCheck(self):
        if type(self.value) != str:
            raise TypeError("OpenFileChooserField value must be a string!")

    def GetDlgMessage(self):
        return self.dlg_msg

    def GetWildcard(self):
        return self.wildcard

    def GetBtnLabel(self):
        return self.btn_lbl

    def CreateUI(self, parent, sizer):
        label = wx.StaticText(parent, label=self.GetLabel())
        sizer.Add(label, flag=wx.LEFT|wx.TOP, border=5)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.textcontrol = wx.TextCtrl(
            parent,
            id=wx.ID_ANY,
            value=self.GetValue(),
            style=wx.TE_READONLY
            )
        hbox.Add(self.textcontrol, proportion=1)

        self.button = wx.Button(
            parent,
            id=wx.ID_ANY,
            label=self.GetBtnLabel()
            )
        hbox.Add(self.button, flag=wx.LEFT, border=5)
        self.button.Bind(
            wx.EVT_BUTTON,
            self.WidgetEvent
            )

        vbox.Add(hbox, flag=wx.EXPAND)
        sizer.Add(vbox, flag=wx.ALL|wx.EXPAND, border=5)

    def WidgetEvent(self, event):
        dlg = wx.FileDialog(
            None,
            message=self.GetDlgMessage(),
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=self.GetWildcard(),
            style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW
            )

        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            self.SetValue(paths[0])
            self.textcontrol.ChangeValue(self.GetValue())


class LabelProp(Property):
    """ Allows setting and resetting text on a label. """
    def __init__(self, idname, default="", label="", visible=True):
        Property.__init__(self, idname, default, label, visible)

        self._RunErrorCheck()

    def CreateUI(self, parent, sizer):
        label = wx.StaticText(parent, label=self.GetLabel())
        sizer.Add(label, flag=wx.LEFT|wx.TOP, border=5)

        static_label = wx.StaticText(parent, label=self.GetValue())
        sizer.Add(static_label, flag=wx.LEFT|wx.TOP, border=5)


class SizeProp(Property):
    """ Allows the user to select an X and Y size. """
    def __init__(self, idname, default=[255, 255], min_val=0,
                max_val=6000, label="", visible=True):
        Property.__init__(self, idname, default, label, visible)
        self.min_value = min_val
        self.max_value = max_val

        self._RunErrorCheck()

    def GetMinValue(self):
        return self.min_value

    def GetMaxValue(self):
        return self.max_value

    def CreateUI(self, parent, sizer):
        label = wx.StaticText(parent, label=self.GetLabel())
        sizer.Add(label, flag=wx.LEFT|wx.TOP, border=5)

        self.spinbox_x = wx.SpinCtrl(
            parent,
            id=wx.ID_ANY,
            min=self.GetMinValue(),
            max=self.GetMaxValue(),
            initial=self.GetValue()[0]
            )
        sizer.Add(self.spinbox_x, flag=wx.ALL|wx.EXPAND, border=5)
        self.spinbox_x.Bind(
            wx.EVT_SPINCTRL,
            self.WidgetEvent
            )
        self.spinbox_x.Bind(
            wx.EVT_TEXT,
            self.WidgetEvent
            )

        self.spinbox_y = wx.SpinCtrl(
            parent,
            id=wx.ID_ANY,
            min=self.GetMinValue(),
            max=self.GetMaxValue(),
            initial=self.GetValue()[1]
            )
        sizer.Add(self.spinbox_y, flag=wx.ALL|wx.EXPAND, border=5)
        self.spinbox_y.Bind(
            wx.EVT_SPINCTRL,
            self.WidgetEvent
            )
        self.spinbox_y.Bind(
            wx.EVT_TEXT,
            self.WidgetEvent
            )

    def WidgetEvent(self, event):
        self.SetValue(
            [self.spinbox_x.GetValue(),
            self.spinbox_y.GetValue()]
            )





if __name__ == '__main__':
    """
    Test demo app
    """
    class TestApp(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None, title="Test", size=(300, 500))
            sz = wx.BoxSizer(wx.VERTICAL)

            f1 = PositiveIntegerProp(
                "Size y",
                default=3,
                min_val=0,
                max_val=10,
                widget=SPINBOX_WIDGET,
                label="Int:",
                )
            f1.SetValue(6)
            f1.CreateUI(self, sz)

            f2 = PositiveIntegerProp(
                "Size x",
                default=3,
                min_val=0,
                max_val=10,
                widget=SLIDER_WIDGET,
                label="Int:",
                )
            f2.SetValue(1)
            f2.CreateUI(self, sz)

            f3 = ChoiceProp(
                "Choice",
                default="RED",
                label="Choice:",
                choices=["RED", "BLUE", "GREEN"])
            f3.SetValue("BLUE")
            f3.CreateUI(self, sz)

            f4 = ColorProp(
                "Color",
                label="Color:",
                default=(255, 255, 255, 255),
                visible=False
                )
            if f4.GetIsVisible() == True:
                f4.CreateUI(self, sz)
            f4.SetValue((4, 4, 4, 4))
            print(f4.GetValue())

            wildcard = "All files (*.*)|*.*|" \
                    "JPEG file (*.jpeg)|*.jpeg|" \
                    "JPG file (*.jpg)|*.jpg|" \
                    "PNG file (*.png)|*.png|" \
                    "BMP file (*.bmp)|*.bmp|" \
                    "WEBP file (*.webp)|*.webp|" \
                    "TGA file (*.tga)|*.tga|" \
                    "TIFF file (*.tiff)|*.tiff"

            f5 = OpenFileChooserProp(
                "File",
                default="",
                dlg_msg="Choose file...",
                wildcard=wildcard,
                btn_lbl="Choose...",
                label="Open file chooser:"
                )
            f5.CreateUI(self, sz)

            self.SetSizer(sz)

    # Create the app and startup
    app = wx.App(redirect=False)
    frame = TestApp()
    frame.Show()
    app.SetTopWindow(frame)
    app.MainLoop()