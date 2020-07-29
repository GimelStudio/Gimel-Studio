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
## FILE: user_preferences_dialog.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the program user preferences dialog
## ----------------------------------------------------------------------------


import wx
 
 
class UserPreferencesDialog(wx.Dialog):
    def __init__(self, parent, *args, **kw):
        wx.Dialog.__init__(self, parent, *args, **kw)
        self._parent = parent

        self._InitUI()        
        self.SetSize((340, 280))        
        self.SetTitle("User Preferences")
        self.Centre()


    def _InitUI(self):

        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(5, 5)

        ui_theme_sb = wx.StaticBox(panel, label="UI Theme")

        boxsizer = wx.StaticBoxSizer(ui_theme_sb, wx.VERTICAL)
        self.enable_light_theme = wx.CheckBox(panel, label="Enable light theme")
        boxsizer.Add(self.enable_light_theme, flag=wx.ALL, border=5)
        self.node_wire_curving = wx.CheckBox(panel, label="Enable node wire curving")
        boxsizer.Add(self.node_wire_curving, flag=wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)
        sizer.Add(boxsizer, pos=(0, 0), span=(1, 5),
            flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=10)

        render_settings_sb = wx.StaticBox(panel, label="Renderer Settings")

        boxsizer = wx.StaticBoxSizer(render_settings_sb, wx.VERTICAL)
        self.auto_render_checkbox = wx.CheckBox(panel, label="Auto render Node Graph")
        boxsizer.Add(self.auto_render_checkbox, flag=wx.ALL, border=5)
        sizer.Add(boxsizer, pos=(1, 0), span=(1, 5),
            flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=10)


        closeButton = wx.Button(panel, label="Cancel")
        sizer.Add(closeButton, pos=(2, 2), flag=wx.TOP|wx.BOTTOM, border=10)
        okButton = wx.Button(panel, label="OK")
        sizer.Add(okButton, pos=(2, 3), flag=wx.ALL, border=10)

        panel.SetSizer(sizer)
        sizer.Fit(self)

        okButton.Bind(wx.EVT_BUTTON, self.OnOK)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)

        self._OnLoadSettings()

    def _OnLoadSettings(self):

        if self.UserPrefs.GetNodeWireCurving() == 10:
            self.node_wire_curving.SetValue(True) # hard-coded value...
        else:
            self.node_wire_curving.SetValue(False)

        if self.UserPrefs.GetActiveTheme() == "light_theme":
            self.enable_light_theme.SetValue(True)
        else:
            self.enable_light_theme.SetValue(False)


    def _OnSaveSettings(self): 

        if self.node_wire_curving.GetValue() == True:
            self.UserPrefs.SetNodeWireCurving(10) # hard-coded value...
        else:
            self.UserPrefs.SetNodeWireCurving(0)

        if self.enable_light_theme.GetValue() == True:
            self.UserPrefs.SetActiveTheme("light_theme")
        else:
            self.UserPrefs.SetActiveTheme("dark_theme")

        # Update everything in the Node Graph
        self._parent.GetNodeGraph().UpdateAllNodes()

        # Save the settings in the config file
        self.UserPrefs.Save()


    def OnOK(self, event): 
        self._OnSaveSettings()       
        self.Destroy()

    def OnClose(self, event):        
        self.Destroy()

    @property
    def UserPrefs(self):
        return self._parent.GetUserPrefManager()



if __name__ == "__main__":
    app = wx.App()
    dlg = UserPreferencesDialog(None)
    dlg.Show()
    app.MainLoop()