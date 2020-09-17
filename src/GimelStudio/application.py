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
## FILE: application.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Main application class which ties all the elements into one window
## ----------------------------------------------------------------------------

import os 
import webbrowser

import wx
import wx.lib.agw.aui as aui
import wx.lib.delayedresult as delayedresult

from GimelStudio.interface import (
    NodeGraph, NodePropertyPanel, 
    ImageViewport
    )
from GimelStudio.program import (
    AboutDialog, LicenseDialog
    ) 
from GimelStudio.renderer import Renderer
from GimelStudio import utils
from GimelStudio import meta
from GimelStudio.datafiles import *


# Create IDs
# ID_MENUITEM_OPENPROJECT = wx.NewIdRef()
# ID_MENUITEM_SAVEPROJECT = wx.NewIdRef()
# ID_MENUITEM_SAVEPROJECTAS = wx.NewIdRef()
# ID_MENUITEM_USERPREFERENCES = wx.NewIdRef()
# ID_MENUITEM_QUIT = wx.NewIdRef()
# ID_MENUITEM_TOGGLEFULLSCREEN = wx.NewIdRef()
# ID_MENUITEM_RENDERIMAGE = wx.NewIdRef()
# ID_MENUITEM_FEEDBACKSURVEY = wx.NewIdRef()
# ID_MENUITEM_DOCS = wx.NewIdRef()
# ID_MENUITEM_LICENSE = wx.NewIdRef()
# ID_MENUITEM_ABOUT = wx.NewIdRef()


class MainApplication(wx.Frame):
    def __init__(self, arguments):
        wx.Frame.__init__(self, None, title=meta.APP_TITLE, size=(1000, 800))

        self._jobID = 0
        self._abortEvent = delayedresult.AbortEvent()

        # Set the program icon
        self.SetIcon(ICON_GIMELSTUDIO_ICO.GetIcon())

        # Init everything
        self._InitApp()

        self.SetBackgroundColour(wx.Colour("#C7C7C7"))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("")
        self.statusbar.SetBackgroundColour(wx.Colour("#C7C7C7"))
        self.statusbar.SetForegroundColour(wx.Colour("white"))


        self._nodeGraph.AddNode("corenode_outputcomposite", 
        wx.NewIdRef(), pos=wx.Point(5010, 5010))

        self._nodeGraph.AddNode("corenode_image", 
        wx.NewIdRef(), pos=wx.Point(5160, 5160))
        self._nodeGraph.AddNode("corenode_image", 
        wx.NewIdRef(), pos=wx.Point(5360, 5160))
        self._nodeGraph.AddNode("corenode_image", 
        wx.NewIdRef(), pos=wx.Point(5390, 5190))

        self._nodeGraph.AddNode("corenode_mix", 
        wx.NewIdRef(), pos=wx.Point(5460, 5460))

        self._nodeGraph.AddNode("corenode_mix", 
        wx.NewIdRef(), pos=wx.Point(5260, 5260))

        self._nodeGraph.AddNode("corenode_brightness", 
        wx.NewIdRef(), pos=wx.Point(5660, 5660))

        self._nodeGraph.AddNode("examplecustomnode_brightness", 
        wx.NewIdRef(), pos=wx.Point(5960, 5660))


    def _InitApp(self):
        self._InitProgramBackend()
        self._InitAUIManagerStyles()
        self._InitMenuBar()
        self._InitUIPanels()

        self._SetupWindowStartup()

    def _InitProgramBackend(self):
        # Init project, renderer and user preferences manager
        #self._project = GimelStudioProject(self)
        self._renderer = Renderer(self)
        #self._userPrefManager = UserPreferencesManager(self)

        # Load the user preferences from the .json file
        # otherwise use the default, built-in preferences.
        #self._userprefmanager.Load()
        #self._userprefmanager.Save()

    def _InitAUIManagerStyles(self):
        # Setup the AUI window manager and configure settings so
        # that we get the style that we want instead
        # of the yucky default colors. :)
        self._mgr = aui.AuiManager()
        self._mgr.SetManagedWindow(self) 
        self._mgr.SetAGWFlags(
            self._mgr.GetAGWFlags() ^ aui.AUI_MGR_LIVE_RESIZE
            )
        self._mgr.GetArtProvider().SetMetric(
            aui.AUI_DOCKART_SASH_SIZE,
            6
            )
        self._mgr.GetArtProvider().SetMetric(
            aui.AUI_DOCKART_PANE_BORDER_SIZE,
            2
            )
        self._mgr.GetArtProvider().SetMetric(
            aui.AUI_DOCKART_GRADIENT_TYPE, 
            aui.AUI_GRADIENT_NONE
            )
        self._mgr.GetArtProvider().SetColour(
            aui.AUI_DOCKART_BACKGROUND_COLOUR, 
            wx.Colour("#fff")
            )
        self._mgr.GetArtProvider().SetColour(
            aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR, 
            wx.Colour("#fff")
            )
        self._mgr.GetArtProvider().SetColour(
            aui.AUI_DOCKART_INACTIVE_CAPTION_TEXT_COLOUR, 
            wx.Colour("#000")
            )
        self._mgr.GetArtProvider().SetColour(
            aui.AUI_DOCKART_BORDER_COLOUR, 
            wx.Colour("#fff")
            )
        self._mgr.GetArtProvider().SetColour(
            aui.AUI_DOCKART_SASH_COLOUR, 
            wx.Colour("#fff")
            )
        self._mgr.GetArtProvider().SetColour(
            aui.AUI_DOCKART_GRIPPER_COLOUR, 
            wx.Colour("#fff")
            )
 
    def _InitMenuBar(self):
        # Menubar        
        self.mainmenubar = wx.MenuBar()

        # File menu
        self.filemenu = wx.Menu()

        self.openproject_menuitem = wx.MenuItem(
            self.filemenu, 
            wx.ID_ANY, 
            "Open Project... \tCtrl+O", 
            "Open and load a Gimel Studio project file"
            )
        self.filemenu.Append(self.openproject_menuitem)

        self.saveproject_menuitem = wx.MenuItem(
            self.filemenu, 
            wx.ID_ANY, 
            "Save Project... \tCtrl+S", 
            "Save the current Gimel Studio project file"
            )
        self.filemenu.Append(self.saveproject_menuitem)
        #if self.GetActiveProjectFile() == None:
        #    self.saveproject_menuitem.Enable(False)

        self.saveprojectas_menuitem = wx.MenuItem(
            self.filemenu, 
            wx.ID_ANY, 
            "Save Project As... \tCtrl+Shift+S", 
            "Save the current project as a Gimel Studio project file"
            )
        self.filemenu.Append(self.saveprojectas_menuitem)

        self.filemenu.AppendSeparator()

        self.export_menuitem = wx.MenuItem(
            self.filemenu, 
            wx.ID_ANY, 
            "Export Image", 
            "Export rendered composite image to file as-is"
            )
        self.filemenu.Append(self.export_menuitem)    

        self.filemenu.AppendSeparator()

        self.quit_menuitem = wx.MenuItem(
            self.filemenu, 
            wx.ID_ANY, 
            "Quit \tCtrl+Q", 
            "Quit Gimel Studio"
            )
        self.filemenu.Append(self.quit_menuitem)     

        self.mainmenubar.Append(self.filemenu, "File")

        # Edit menu
        self.editmenu = wx.Menu()

        self.userpreferences_menuitem = wx.MenuItem(
            self.editmenu,
            wx.ID_ANY,
            "Preferences",
            "Open the user preferences dialog"
        )
        self.editmenu.Append(self.userpreferences_menuitem)  

        self.mainmenubar.Append(self.editmenu, "Edit")


        # View menu
        self.viewmenu = wx.Menu()

        self.togglefullscreen_menuitem = wx.MenuItem(
            self.viewmenu, 
            wx.ID_ANY, 
            "Fullscreen",  
            "Set the window size to fullscreen", 
            wx.ITEM_CHECK
            )
        self.viewmenu.Append(self.togglefullscreen_menuitem)
        self.viewmenu.Check(self.togglefullscreen_menuitem.GetId(), True)

        self.togglenodegraphgrid_menuitem = wx.MenuItem(
            self.viewmenu, 
            wx.ID_ANY, 
            "Show Grid",  
            "Toggle the Node Graph grid background", 
            wx.ITEM_CHECK
            )
        self.viewmenu.Append(self.togglenodegraphgrid_menuitem)
        self.viewmenu.Check(self.togglenodegraphgrid_menuitem.GetId(), True)

        self.mainmenubar.Append(self.viewmenu, "View")


        # Render menu
        self.rendermenu = wx.Menu()

        self.toggleautorender_menuitem = wx.MenuItem(
            self.rendermenu, 
            wx.ID_ANY, 
            "Auto Render",  
            "Toggle whether to auto render after editing node properties, connections, etc", 
            wx.ITEM_CHECK
            )
        self.rendermenu.Append(self.toggleautorender_menuitem)
        self.rendermenu.Check(self.toggleautorender_menuitem.GetId(), True)

        self.renderimage_menuitem = wx.MenuItem(
            self.rendermenu, 
            wx.ID_ANY, 
            "Render Image \tF12",  
            "Force an immediate, updated render of the current node graph image."
            )
        self.rendermenu.Append(self.renderimage_menuitem)

        self.mainmenubar.Append(self.rendermenu, "Render")


        # Help menu
        self.helpmenu = wx.Menu()

        self.onlinedocs_menuitem = wx.MenuItem(
            self.helpmenu, 
            wx.ID_ANY, 
            "Online Documentation", 
            "Open the Gimel Studio documentation in browser"
            )
        self.helpmenu.Append(self.onlinedocs_menuitem)

        self.helpmenu.AppendSeparator()

        self.visithomepage_menuitem = wx.MenuItem(
            self.helpmenu, 
            wx.ID_ANY, 
            "Visit Website", 
            "Visit the Gimel Studio home page"
            )
        self.helpmenu.Append(self.visithomepage_menuitem)

        self.feedbacksurvey_menuitem = wx.MenuItem(
            self.helpmenu, 
            wx.ID_ANY, 
            "Feedback Survey", 
            "Take a short survey online about Gimel Studio v0.5.x beta"
            )
        #self.feedbacksurvey_menuitem.SetBitmap(
        # ICON_MENU_ABOUTGIMELSTUDIO.GetBitmap())
        self.helpmenu.Append(self.feedbacksurvey_menuitem)

        self.license_menuitem = wx.MenuItem(
            self.helpmenu, 
            wx.ID_ANY, 
            "License", 
            "Show Gimel Studio license"
            )
        #self.about_menuitem.SetBitmap(ICON_MENU_ABOUTGIMELSTUDIO.GetBitmap())
        self.helpmenu.Append(self.license_menuitem)

        self.helpmenu.AppendSeparator()

        self.about_menuitem = wx.MenuItem(
            self.helpmenu, 
            wx.ID_ANY, 
            "About", 
            "Show information about GimelStudio"
            )
        #self.about_menuitem.SetBitmap(ICON_MENU_ABOUTGIMELSTUDIO.GetBitmap())
        self.helpmenu.Append(self.about_menuitem)

        self.mainmenubar.Append(self.helpmenu, "Help")


        self.SetMenuBar(self.mainmenubar)


        # Menubar bindings
        self.Bind(wx.EVT_MENU, self.OnToggleFullscreen, 
            self.togglefullscreen_menuitem
            )
        self.Bind(wx.EVT_MENU, 
            self.OnToggleNodeGraphGrid, 
            self.togglenodegraphgrid_menuitem
            ) 

        self.Bind(wx.EVT_MENU, self.OnToggleAutoRender, 
            self.toggleautorender_menuitem
            )
        self.Bind(wx.EVT_MENU, self.OnRender, 
            self.renderimage_menuitem
            )

        self.Bind(wx.EVT_MENU, self.OnReadOnlineDocs, 
            self.onlinedocs_menuitem
            ) 
        self.Bind(wx.EVT_MENU, self.OnVisitWebsite, 
            self.visithomepage_menuitem
            )
        self.Bind(wx.EVT_MENU, self.OnFeedbackSurvey, 
            self.feedbacksurvey_menuitem
            )
        self.Bind(wx.EVT_MENU, self.OnLicenseDialog, 
            self.license_menuitem
            )
        self.Bind(wx.EVT_MENU, self.OnAboutDialog, 
            self.about_menuitem
            )


    def _InitUIPanels(self):
        # Image Viewport Panel
        self._imageViewport = ImageViewport(
            self,
            )
        self._mgr.AddPane(
            self._imageViewport, 
            aui.AuiPaneInfo()
            .Right()
            .Name("ImageViewport")
            .Caption("Image Viewport")
            .Icon(ICON_PANEL_IMAGE_VIEWPORT_DARK.GetBitmap())
            .CloseButton(visible=False)
            .BestSize(750, 500)
            )

        # Node Properties Panel
        self._nodePropertyPanel = NodePropertyPanel(
            self,
            (500, 800)
            )
        self._mgr.AddPane(
            self._nodePropertyPanel, 
            aui.AuiPaneInfo()
            .Right()
            .Name("NodeProperties")
            .Caption("Node Properties")
            .Icon(ICON_PANEL_NODE_PROPERTY_PANEL_DARK.GetBitmap())
            .CloseButton(visible=False)
            .BestSize(750, 400)
            )

        # Node Graph Panel
        self._nodeGraph = NodeGraph(
            self,
            (600, 600)
            )
        self._mgr.AddPane(
            self._nodeGraph, 
            aui.AuiPaneInfo()
                .Center()
                .Name("NodeGraph")
                .Caption("Node Graph")
                .Icon(ICON_PANEL_NODE_GRAPH_DARK.GetBitmap())
                .CloseButton(visible=False)
                .BestSize(750, 400)
                .Floatable(False)
                .Movable(False)
            )


    def _SetupWindowStartup(self):
        # Maximize the window & tell the AUI window 
        # manager to "commit" all the changes just made.
        self.Maximize()
        self._mgr.Update()

        # Quit prompt dialog
        if meta.APP_DEBUG != True:
            self.Bind(wx.EVT_CLOSE, self.OnQuit)


    def OnToggleFullscreen(self, event):
        if self.IsMaximized() == False:
            self.Maximize()
        elif self.IsMaximized() == True:
            self.Restore()

    def OnToggleNodeGraphGrid(self, event):
        if self.togglenodegraphgrid_menuitem.IsChecked() == False:
            self._nodeGraph.SetShouldDrawGrid(False)
        else:
            self._nodeGraph.SetShouldDrawGrid(True)
        self._nodeGraph.RefreshGraph()

    def OnToggleAutoRender(self, event):
        if self.toggleautorender_menuitem.IsChecked() == False:
            print("no auto render")
        else:
            print("render")
        self._nodeGraph.RefreshGraph()

    def OnRender(self, event):
        """ Event handler for rendering the current Node Graph. """
        self.Render()  

    def OnQuit(self, event):
        quitdialog = wx.MessageDialog(
            self, 
            "Do you really want to quit? You will lose any unsaved data.", 
            "Quit Gimel Studio?", 
            wx.YES_NO|wx.YES_DEFAULT
            )

        if quitdialog.ShowModal() == wx.ID_YES:
            quitdialog.Destroy()
            self._mgr.UnInit()
            del self._mgr
            self.Destroy()
        else:
            event.Skip()

    def OnFeedbackSurvey(self, event):
        """ Go to the feedback survey webpage. """
        # Will be removed after BETA stage
        url = ("https://www.surveymonkey.com/r/RSRD556")
        webbrowser.open(url) 

    def OnReadOnlineDocs(self, event):
        """ Go to the Gimel Studio documentation online. """
        url = ("https://gimel-studio.readthedocs.io/en/latest/")
        webbrowser.open(url) 

    def OnVisitWebsite(self, event):
        """ Go to the Gimel Studio home page. """
        url = ("https://correctsyntax.com/projects/gimel-studio/")
        webbrowser.open(url) 

    def OnAboutDialog(self, event):
        dialog = AboutDialog(self)
        dialog.ShowDialog()

    def OnLicenseDialog(self, event):
        dialog = LicenseDialog(self)
        dialog.ShowDialog()

    def Render(self):
        """ Callable render method. This is intended to be the 'master' render
        method, called when the Node Graph image is to be rendered.
        """
        self._abortEvent.clear()
        self._jobID += 1
        #print( "Starting job %s in thread: GUI remains responsive" % self._jobID )
        delayedresult.startWorker(
            self._postRender, 
            self._Render,
            wargs=(self._jobID, self._abortEvent), 
            jobID=self._jobID
            )
        
    def _Render(self, jobID, abort_event):
        """ Internal rendering method. """
        if not abort_event():
            self._imageViewport.UpdateRenderText(True)
            self._renderer.Render(self._nodeGraph.GetNodes())
            render_time = self._renderer.GetTime()
            render_image = self._renderer.GetRender()
            if render_image != None:
                self._imageViewport.UpdateViewerImage(
                    utils.ConvertImageToWx(render_image),
                    render_time
                    )
                self._abortEvent.set()
        else:
            self._abortEvent.clear()

        self._imageViewport.UpdateRenderText(False)
        return jobID

    def _postRender(self, delayedResult):
        """ Internal post-render misc. """
        try:
            result = delayedResult.get()
            #print("Aborting result for job %s" % self.jobID)
            self._nodeGraph.UpdateAllNodes()
            self._abortEvent.clear()
            return result
        except Exception as exc:
            print('ERROR: PLEASE REPORT THE FOLLOWING ERROR TO THE DEVELOPERS: \n', exc)
            return



