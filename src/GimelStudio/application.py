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

from GimelStudio.meta import (__NAME__, __AUTHOR__, __VERSION__,
                              __DEBUG__, __TITLE__)

from GimelStudio.project import GimelStudioProject
from GimelStudio.renderer import Renderer
from GimelStudio.program import (ProgramUpdateChecker, AboutGimelStudioDialog,
                                GimelStudioLicenseDialog)
from GimelStudio.user_preferences import (UserPreferencesDialog, 
                                         UserPreferencesManager)
from GimelStudio.node_registry import NodeRegistry
from GimelStudio.node_graph import NodeGraph, NodeGraphDropTarget
from GimelStudio.node_property_panel import NodePropertyPanel
from GimelStudio.image_viewport import ImageViewport

from GimelStudio.utils import ConvertImageToWx, ExportRenderedImageToFile

from GimelStudio.stylesheet import *
from GimelStudio.datafiles.icons import *


# Create IDs
ID_MENUITEM_OPENPROJECT = wx.NewIdRef()
ID_MENUITEM_SAVEPROJECT = wx.NewIdRef()
ID_MENUITEM_SAVEPROJECTAS = wx.NewIdRef()
ID_MENUITEM_USERPREFERENCES = wx.NewIdRef()
ID_MENUITEM_QUIT = wx.NewIdRef()
ID_MENUITEM_TOGGLEFULLSCREEN = wx.NewIdRef()
ID_MENUITEM_TAKEFEEDBACKSURVEY = wx.NewIdRef()
ID_MENUITEM_LICENSE = wx.NewIdRef()
ID_MENUITEM_ABOUT = wx.NewIdRef()

ID_RENDERTOOLBAR_RENDERBTN = wx.NewIdRef()
ID_VIEWERTOOLBAR_QUICKEXPORTIMGBTN = wx.NewIdRef()


class MainApplication(wx.Frame):
    def __init__(self, arguments):
        wx.Frame.__init__(self, None, title=__TITLE__,
                          pos=(0, 0), size=(1000, 800))

        self._arguments = arguments
        self._activeprojectfile = None
        self._jobID = 0
        self._abortEvent = delayedresult.AbortEvent()

        # Set the program icon
        self.SetIcon(ICON_GIMELSTUDIO_ICO.GetIcon())
 
        # Init project, renderer and user preferences manager
        self._project = GimelStudioProject(self)
        self._renderer = Renderer(self)
        self._userprefmanager = UserPreferencesManager(
            self
            )

        # Load the user preferences from the .json file
        # otherwise use the default, built-in preferences.
        self._userprefmanager.Load()
        #self._userprefmanager.Save()

        # Setup the AUI window manager and configure settings so
        # that we get the light white theme that we want instead
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
            wx.Colour(self.Theme["app_bg"])
            )
        self._mgr.GetArtProvider().SetColour(
            aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR, 
            wx.Colour(self.Theme["dock_pnl_bg"])
            )
        self._mgr.GetArtProvider().SetColour(
            aui.AUI_DOCKART_INACTIVE_CAPTION_TEXT_COLOUR, 
            wx.Colour(self.Theme["dock_pnl_caption_txt"])
            )
        self._mgr.GetArtProvider().SetColour(
            aui.AUI_DOCKART_BORDER_COLOUR, 
            wx.Colour(self.Theme["dock_pnl_bg"])
            )
        self._mgr.GetArtProvider().SetColour(
            aui.AUI_DOCKART_SASH_COLOUR, 
            wx.Colour(self.Theme["app_bg"])
            )
        self._mgr.GetArtProvider().SetColour(
            aui.AUI_DOCKART_GRIPPER_COLOUR, 
            wx.Colour(self.Theme["app_bg"])
            )

        # Init the panes
        self._imageViewport = ImageViewport(
            self,
            #(500, 600)
            )
        self._nodeRegistry = NodeRegistry(
            self
            )

        self._nodePropertyPanel = NodePropertyPanel(
            self,
            (500, 800)
            )

        self._nodeGraph = NodeGraph(
            self,
            (600, 600)
            )
        # Drag image from dir or Node Registry into 
        # node graph to create image node
        self._nodeGraph.SetDropTarget(NodeGraphDropTarget(self._nodeGraph))


        # self._assetlibrary = AssetLibrary(
        #     self,
        #     )

        # Add the panes to the manager
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
        # self._mgr.AddPane(
        #     self._nodeRegistry, 
        #     aui.AuiPaneInfo()
        #     .Left() 
        #     .Name("NodeRegistry")
        #     .Caption("Node Registry")
        #     .Icon(ICON_PANEL_NODE_REGISTRY_DARK.GetBitmap())
        #     .CloseButton(visible=False)
        #     .BestSize(400, 400)
        #     )


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

        # Build the menubar
        self._BuildMenuBar()

        # Build the UI toolbar(s)
        self._BuildUIToolbars()

        # Maximize the window
        self.Maximize()

        # Tell the AUI window manager to "commit" all the changes just made.
        self._mgr.Update()

        # Default nodes setup
        self._SetupDefaultNodes()

        # Open the given file at the command line, if
        # there is one -otherwise load the default setup.
        if self._arguments.file == 'DEFAULT_FILE':
            print('INFO: LOADING DEFAULT')
            # For some reason, it works only when the default nodes are setup
            # whether or not we are going to open a new file next! It could be a bug.
            pass

        else:
            print('INFO: LOADING FILE {} FROM CMD'.format(self._arguments.file))
            #print(arguments.file, "<<")
            if self._arguments.file.endswith(".gimel-studio-project"):
                self._project.OpenProjectFile(arguments.file) 
                self.OnProjectSetTitle(arguments.file)
            else:
                print("Opening other files from the CMD is not implemented yet!")


        # Quit prompt dialog
        if __DEBUG__ != True:
            self.Bind(wx.EVT_CLOSE, self.OnQuit)

        
    def GetArguments(self):
        return self._arguments

    def GetActiveProjectFile(self):
        return self._activeprojectfile

    def SetActiveProjectFile(self, project_path):
        self._activeprojectfile = project_path

    def GetAUIManager(self):
        return self._mgr
    
    def GetRenderer(self):
        return self._renderer

    def GetProject(self):
        return self._project

    def GetUserPrefManager(self):
        return self._userprefmanager

    @property
    def Theme(self):
        """ Get the active UI theme. """
        return self._userprefmanager.GetTheme()

    def GetImageViewport(self):
        return self._imageViewport

    def GetNodePropertyPanel(self):
        return self._nodePropertyPanel

    def GetNodeGraph(self):
        return self._nodeGraph

    def GetNodeRegistry(self):  
        return self._nodeRegistry

    def _SetupDefaultNodes(self):
        # Calculate center of Node Graph view
        rect = self._nodeGraph.GetSize()

        # 5000px is 1/2 the size of the Node Graph
        x, y = (rect[0]/2)+5000, (rect[1]/2)+5000

        # Add default nodes
        self._nodeGraph.AddNode(
            'gimelstudiocorenode_image', 
            pos=wx.Point(x-340, y)
            )
        
        self._nodeGraph.AddNode(
            'gimelstudiocorenode_outputcomposite', 
            pos=wx.Point(x+150, y)
            )

        # This node is here just for 
        # testing during development.
        if __DEBUG__ == True:
            self._nodeGraph.AddNode(
                'gimelstudiocorenode_addtext', 
                pos=wx.Point(x-100, y)
                )


    def _BuildUIToolbars(self):

        # Render Toolbar
        render_toolbar = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER | wx.TB_HORZ_TEXT)
        render_toolbar.AddTool(
            ID_RENDERTOOLBAR_RENDERBTN, 
            "Render Image", 
            ICON_RENDER_IMAGE_DARK.GetBitmap(), 
            """Force an immediate, updated render of the current node graph image. """
            )

        render_toolbar.Realize()

        # Viewer Toolbar
        viewer_toolbar = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER | wx.TB_HORZ_TEXT)
        viewer_toolbar.AddTool(
            ID_VIEWERTOOLBAR_QUICKEXPORTIMGBTN, 
            "Quick Export", 
            ICON_EXPORT_IMAGE_DARK.GetBitmap(), 
            "Export rendered image as a numbered file in your user home directory."
            )
        viewer_toolbar.Realize()

        # Add the toolbars to the manager
        self._mgr.AddPane(render_toolbar, aui.AuiPaneInfo().
                          Name("RenderToolbar").Caption("Render Toolbar").
                          ToolbarPane().Top().Row(0).Position(1).
                          LeftDockable(False).RightDockable(False))

        self._mgr.AddPane(viewer_toolbar, aui.AuiPaneInfo().
                          Name("ImageViewerToolbar").Caption("Image Viewer Toolbar").
                          ToolbarPane().Top().Row(0).Position(2).
                          LeftDockable(False).RightDockable(False))

        # Bindings
        self.Bind(wx.EVT_TOOL, self.OnRenderImage, id=ID_RENDERTOOLBAR_RENDERBTN)
        self.Bind(wx.EVT_TOOL, self.OnQuickExport, id=ID_VIEWERTOOLBAR_QUICKEXPORTIMGBTN)


    def _BuildMenuBar(self):
        # Menubar        
        self.mainmenubar = wx.MenuBar()

        # File menu
        self.filemenu = wx.Menu()

        self.openproject_menuitem = wx.MenuItem(
            self.filemenu, 
            ID_MENUITEM_OPENPROJECT, 
            "Open Project... \tCtrl+O", 
            "Open and load a Gimel Studio project file"
            )
        self.filemenu.Append(self.openproject_menuitem)

        self.saveproject_menuitem = wx.MenuItem(
            self.filemenu, 
            ID_MENUITEM_SAVEPROJECT, 
            "Save Project... \tCtrl+S", 
            "Save the current Gimel Studio project file"
            )
        self.filemenu.Append(self.saveproject_menuitem)
        if self.GetActiveProjectFile() == None:
            self.saveproject_menuitem.Enable(False)

        self.saveprojectas_menuitem = wx.MenuItem(
            self.filemenu, 
            ID_MENUITEM_SAVEPROJECTAS, 
            "Save Project As... \tCtrl+Shift+S", 
            "Save the current project as a Gimel Studio project file"
            )
        self.filemenu.Append(self.saveprojectas_menuitem)

        self.filemenu.AppendSeparator()

        self.userpreferences_menuitem = wx.MenuItem(
            self.filemenu,
            ID_MENUITEM_USERPREFERENCES,
            "User Preferences",
            "Open the user preferences dialog"
        )
        self.filemenu.Append(self.userpreferences_menuitem)  

        self.filemenu.AppendSeparator()

        self.quit_menuitem = wx.MenuItem(
            self.filemenu, 
            ID_MENUITEM_QUIT, 
            "Quit \tCtrl+Q", 
            "Quit Gimel Studio"
            )
        self.filemenu.Append(self.quit_menuitem)     

        self.mainmenubar.Append(self.filemenu, "File")
 

        # View menu
        self.viewmenu = wx.Menu()

        self.togglefullscreen_menuitem = wx.MenuItem(
            self.viewmenu, 
            ID_MENUITEM_TOGGLEFULLSCREEN, 
            "Fullscreen",  
            "Set the window size to fullscreen", 
            wx.ITEM_CHECK
            )
        self.viewmenu.Append(self.togglefullscreen_menuitem)
        self.viewmenu.Check(ID_MENUITEM_TOGGLEFULLSCREEN, True)

        self.mainmenubar.Append(self.viewmenu, "View")


        # Help menu
        self.helpmenu = wx.Menu()

        self.takefeedbacksurvey_menuitem = wx.MenuItem(
            self.helpmenu, 
            ID_MENUITEM_TAKEFEEDBACKSURVEY, 
            "Feedback Survey", 
            "Take a short survey online about Gimel Studio"
            )
        #self.takefeedbacksurvey_menuitem.SetBitmap(ICON_MENU_ABOUTGIMELSTUDIO.GetBitmap())
        self.helpmenu.Append(self.takefeedbacksurvey_menuitem)
        
        self.license_menuitem = wx.MenuItem(
            self.helpmenu, 
            ID_MENUITEM_LICENSE, 
            "License", 
            "Show Gimel Studio license"
            )
        #self.about_menuitem.SetBitmap(ICON_MENU_ABOUTGIMELSTUDIO.GetBitmap())
        self.helpmenu.Append(self.license_menuitem)

        self.about_menuitem = wx.MenuItem(
            self.helpmenu, 
            ID_MENUITEM_ABOUT, 
            "About", 
            "Show information about GimelStudio"
            )
        #self.about_menuitem.SetBitmap(ICON_MENU_ABOUTGIMELSTUDIO.GetBitmap())
        self.helpmenu.Append(self.about_menuitem)

        self.mainmenubar.Append(self.helpmenu, "Help")


        self.SetMenuBar(self.mainmenubar)

        # Menubar bindings
        self.Bind(wx.EVT_MENU, self.OnOpenFile, id=ID_MENUITEM_OPENPROJECT)
        self.Bind(wx.EVT_MENU, self.OnSaveFile, id=ID_MENUITEM_SAVEPROJECT)
        self.Bind(wx.EVT_MENU, self.OnSaveFileAs, id=ID_MENUITEM_SAVEPROJECTAS)
        self.Bind(wx.EVT_MENU, self.OnUserPreferencesDialog, id=ID_MENUITEM_USERPREFERENCES)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=ID_MENUITEM_QUIT)
        self.Bind(wx.EVT_MENU, self.OnToggleFullscreen, id=ID_MENUITEM_TOGGLEFULLSCREEN)
        self.Bind(wx.EVT_MENU, self.OnTakeFeedbackSurvey, id=ID_MENUITEM_TAKEFEEDBACKSURVEY)
        self.Bind(wx.EVT_MENU, self.OnAboutGimelStudioDialog, id=ID_MENUITEM_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnGimelStudioLicenseDialog, id=ID_MENUITEM_LICENSE)

    def OnAboutGimelStudioDialog(self, event):
        dialog = AboutGimelStudioDialog(self)
        dialog.ShowDialog()

    def OnGimelStudioLicenseDialog(self, event):
        dialog = GimelStudioLicenseDialog(self)
        dialog.ShowDialog()

    def OnUserPreferencesDialog(self, event):
        dialog = UserPreferencesDialog(self)
        dialog.ShowModal() 

    def OnRenderImage(self, event):
        self.Render()

    def OnQuickExport(self, event):
        """ A quick and dirty export option for quick image 
        render comparisons, etc. 
        """
        rendered_img = self.GetRenderedImage()

        if rendered_img != None:
            base_path = os.path.expanduser('~/')
            directory = os.listdir(base_path)
            
            num = 0
            for file in directory:
                if file.startswith("~"):
                    num = num + 1

            path = os.path.join(base_path, "~{}.png".format(num))

            ExportRenderedImageToFile(
                    rendered_image=rendered_img, 
                    export_path=path,
                    )

            notify = wx.adv.NotificationMessage(
                title="Quick Export",
                message="Image was saved to {}.".format(path),
                parent=None, flags=wx.ICON_INFORMATION
                )
            notify.Show(timeout=1) # 1 for short timeout, 100 for long timeout


    def OnTakeFeedbackSurvey(self, event):
        """ Go to the feedback survey webpage. """
        # Will be removed after BETA stage
        url = ("https://www.surveymonkey.com/r/RSRD556")
        webbrowser.open(url) 

    def OnToggleFullscreen(self, event):
        if self.IsMaximized() == False:
            self.Maximize()
        elif self.IsMaximized() == True:
            self.Restore()


    def OnSaveFile(self, event):
        if self.GetActiveProjectFile() != None:
            path = self.GetActiveProjectFile()
            self._project.SaveProjectFile(path)
            
            notify = wx.adv.NotificationMessage(
                title="Project File Saved",
                message="{} was saved.".format(os.path.split(path)[1]),
                parent=None, flags=wx.ICON_INFORMATION
                )
            notify.Show(timeout=1) # 1 for short timeout, 100 for long timeout
            

    def OnSaveFileAs(self, event):
        wildcard = "GIMEL STUDIO PROJECT file (*.gimel-studio-project)|*.gimel-studio-project|" \
                   "All files (*.*)|*.*"

        dlg = wx.FileDialog(
            self, message="Save project file as...",
            defaultDir='',
            defaultFile='default.gimel-studio-project',
            wildcard=wildcard,
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
            )

        if dlg.ShowModal() == wx.ID_OK:
            busy = wx.BusyInfo("Saving File...")
            # This returns a Python list of files that were selected.
            paths = dlg.GetPaths()
            self._project.SaveProjectFile(paths[0])
            self.OnProjectSetTitle(paths[0])

            del busy

            notify = wx.adv.NotificationMessage(
                title="Project File Saved",
                message="Project was saved to \n {}".format(paths[0]),
                parent=None, flags=wx.ICON_INFORMATION
                )
            notify.Show(timeout=2) # 1 for short timeout, 100 for long timeout

            # Enable save file
            self.saveproject_menuitem.Enable(enable=True)
            
    
    def OnOpenFile(self, event):
        wildcard = "GIMEL STUDIO PROJECT file (*.gimel-studio-project)|*.gimel-studio-project|" \
                   "All files (*.*)|*.*"
        styles = wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW
                   
        dlg = wx.FileDialog(
            self, message="Open project file...",
            defaultDir='',
            wildcard=wildcard,
            style=styles
            )

        if dlg.ShowModal() == wx.ID_OK:
            busy = wx.BusyInfo("Loading Project File...")
            wx.Yield()

            # This returns a Python list of files that were selected.
            paths = dlg.GetPaths()
            success = self._project.OpenProjectFile(paths[0])

            if success == True:
                self.OnProjectSetTitle(paths[0])

                notify = wx.adv.NotificationMessage(
                    title="Project File Opened",
                    message="Project opened and loaded from \n {}".format(paths[0]),
                    parent=None, flags=wx.ICON_INFORMATION
                    )
                notify.Show(timeout=2) # 1 for short timeout, 100 for long timeout

                del busy   

                # Enable save file
                self.saveproject_menuitem.Enable(enable=True)

            elif success == False:
                del busy    

                errordialog = wx.MessageDialog(
                    self,
                    "This project could not be opened due to an unknown error.\n Please report this as a bug to the developer and/or upgrade to the latest version of Gimel Studio.", 
                    "Cannot Open Project!", 
                    wx.OK
                    )

                if errordialog.ShowModal() == wx.ID_YES:
                    errordialog.Destroy()


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
    
    def GetRenderedImage(self):
        return self._renderer.GetRenderedImage()

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
            render_time = self._renderer.GetRenderTime()
            render_image = self.GetRenderedImage()
            if render_image != None:
                self._imageViewport.UpdateViewerImage(
                    ConvertImageToWx(render_image),
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
            #print(exc)
            return

    def OnProjectSetTitle(self, project_path):
        """ Sets the window title for when a project is opened or edited. """
        self.SetActiveProjectFile(project_path)
        self.SetTitle("{0} - {1}".format(
            __TITLE__,
            project_path
            ))  
 
    # FIXME
    def RestartProgram(self, new_args):
        """ UNUSED!!
        Restart the program so that the node registry is refreshed.
        """
        python = sys.executable
        os.execl(python, python, *newArgs)
