## ----------------------------------------------------------------------------
## Gimel Studio © 2020 Correct Syntax, Noah Rahm. All rights reserved.
##
## FILE: application.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Main application class which ties all the elements into one window
## ----------------------------------------------------------------------------

import os
import webbrowser
import wx
import wx.lib.agw.aui as aui

from GimelStudio.meta import (__NAME__, __AUTHOR__, __VERSION__,
                              __BUILD__, __RELEASE__, __DEBUG__,
                              __TITLE__)

from GimelStudio.project import Project
from GimelStudio.renderer import Renderer
from GimelStudio.program import (ProgramUpdateChecker, AboutGimelStudioDialog,
                                 GimelStudioLicenseDialog)
from GimelStudio.node_importer import *
from GimelStudio.nodedef import NODE_REGISTRY 

from GimelStudio.ui import (UserPreferencesManager, ImageViewport,
                            NodeRegistry, NodeGraph, NodePropertyPanel,
                            AssetLibrary, NodeGraphFileDrop,
                            NodeGraphNodeDrop)

from GimelStudio.stylesheet import *
from GimelStudio.datafiles.icons import *

 
# Create IDs
ID_RENDERTOOLBAR_RENDERBTN = wx.NewIdRef()
ID_RENDERTOOLBAR_AUTORENDERCB = wx.NewIdRef()
ID_VIEWERTOOLBAR_EXPORTIMGBTN = wx.NewIdRef()

ID_MENU_OPENFILEMENUITEM = wx.NewIdRef()
ID_MENU_SAVEFILEMENUITEM = wx.NewIdRef()
ID_MENU_SAVEFILEASMENUITEM = wx.NewIdRef()
ID_MENU_QUITMENUITEM = wx.NewIdRef()
ID_MENU_TOGGLEFULLSCREENMENUITEM = wx.NewIdRef()
ID_MENU_TAKEFEEDBACKSURVEYMENUITEM = wx.NewIdRef()
ID_MENU_LICENSEMENUITEM = wx.NewIdRef()
ID_MENU_ABOUTMENUITEM = wx.NewIdRef()


class MainApplication(wx.Frame):
    def __init__(self, arguments):
        wx.Frame.__init__(self, None, title=__TITLE__,
                          pos=(0, 0), size=(1000, 800))

        self._arguments = arguments

        # Set the program icon
        self.SetIcon(ICON_GIMELSTUDIO_ICO.GetIcon())

        # Init project, renderer and user preferences manager
        self._project = Project(
            self,
            __VERSION__,
            __BUILD__,
            __RELEASE__
            )
        self._renderer = Renderer(
            self
            )
        self._userprefmanager = UserPreferencesManager(
            self
            )

        # Load the user preferences from the .json file
        # otherwise use the default, built-in preferences.
        self._userprefmanager.Load()

        # Setup the AUI window manager and configure settings so
        # that we get the dark grey and white theme that we want.
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
            wx.Colour(STYLE_APPLICATION_BG)
            )
        self._mgr.GetArtProvider().SetColour(
            aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR, 
            wx.Colour(STYLE_DOCK_PANEL_BG)
            )
        self._mgr.GetArtProvider().SetColour(
            aui.AUI_DOCKART_INACTIVE_CAPTION_TEXT_COLOUR, 
            wx.Colour(STYLE_DOCK_PANEL_CAPTION_TEXT_FG)
            )
        self._mgr.GetArtProvider().SetColour(
            aui.AUI_DOCKART_BORDER_COLOUR, 
            wx.Colour(STYLE_DOCK_PANEL_BG)
            )
        self._mgr.GetArtProvider().SetColour(
            aui.AUI_DOCKART_SASH_COLOUR, 
            wx.Colour(STYLE_APPLICATION_BG)
            )
        self._mgr.GetArtProvider().SetColour(
            aui.AUI_DOCKART_GRIPPER_COLOUR, 
            wx.Colour(STYLE_APPLICATION_BG)
            )

        # Init the panes
        self._imageviewport = ImageViewport(
            self
            )
        self._nodepropertypanel = NodePropertyPanel(
            self,
            (400, 800)
            )
        self._nodegraph = NodeGraph(
            self,
            self._nodepropertypanel,
            self._project,
            (2000, 2000)
            )
        # Drag image into graph to create image node
        fdt = NodeGraphFileDrop(self._nodegraph)
        self._nodegraph.SetDropTarget(fdt)

        # Drag node item from node registry
        nrdt = NodeGraphNodeDrop(self._nodegraph)
        self._nodegraph.SetDropTarget(nrdt) 

        self._noderegistry = NodeRegistry(
            self,
            NODE_REGISTRY
            )
        # self._assetlibrary = AssetLibrary(
        #     self,
        #     )

        # Add the panes to the manager
        self._mgr.AddPane(
            self._imageviewport, 
            aui.AuiPaneInfo()
            .Top()
            .Name("ImageViewport")
            .Caption("Image Viewport")
            .Icon(ICON_PANEL_IMAGE_VIEWPORT_DARK.GetBitmap())
            .CloseButton(visible=False)
            .BestSize(400, 400)
            )
        self._mgr.AddPane(
            self._nodepropertypanel, 
            aui.AuiPaneInfo()
            .Right()
            .Name("NodeProperties")
            .Caption("Node Properties")
            .Icon(ICON_PANEL_NODE_PROPERTY_PANEL_DARK.GetBitmap())
            .CloseButton(visible=False)
            .BestSize(400, 400)
            )
        self._mgr.AddPane(
            self._nodegraph, 
            aui.AuiPaneInfo()
            .Center()
            .Name("NodeGraph")
            .Caption("Node Graph")
            .Icon(ICON_PANEL_NODE_GRAPH_DARK.GetBitmap())
            .CloseButton(visible=False)
            )

        self._mgr.AddPane(
            self._noderegistry, 
            aui.AuiPaneInfo()
            .Left()
            .Name("NodeRegistry")
            .Caption("Node Registry")
            .Icon(ICON_PANEL_NODE_REGISTRY_DARK.GetBitmap())
            .CloseButton(visible=False)
            .BestSize(400, 400)
            )

##        self._mgr.AddPane(
##            self._assetlibrary, 
##            aui.AuiPaneInfo()
##            .Bottom()
##            .Name("AssetLibrary")
##            .Caption("Asset Library")
##            .Icon(ICON_PANEL_NODEGRAPH.GetBitmap())
##            .CloseButton(visible=False)
##            )

        # Build the menubar
        self.BuildMenuBar()

        # Render Toolbar
        render_toolbar = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER | wx.TB_HORZ_TEXT)
        render_toolbar.AddTool(
            ID_RENDERTOOLBAR_RENDERBTN, 
            "Render", 
            ICON_RENDER_IMAGE_DARK.GetBitmap(), 
            "Render the current node graph"
            )
        render_toolbar.AddSeparator()

        self._autoRenderCheckbox = wx.CheckBox(
            render_toolbar, 
            ID_RENDERTOOLBAR_AUTORENDERCB, 
            "Auto Render"
            )
        self._autoRenderCheckbox.SetValue(True)

        render_toolbar.AddControl(
            self._autoRenderCheckbox,
            )
        render_toolbar.Realize()

        # Viewer Toolbar
        viewer_toolbar = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER | wx.TB_HORZ_TEXT)
        viewer_toolbar.AddTool(
            ID_VIEWERTOOLBAR_EXPORTIMGBTN, 
            "Export Image", 
            ICON_EXPORT_IMAGE_DARK.GetBitmap(), 
            "Export the current rendered image to a file"
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






        

        # Maximize the window
        self.Maximize()

        # Tell the AUI window manager to "commit" all the changes just made.
        self._mgr.Update()

        # Check for updates
        #programupdatechecker = ProgramUpdateChecker(__VERSION__)
        #programupdatechecker.run()




        self._imageviewport.InitModeRadioButtonWidgets()
##
##        from PIL import Image
##        from GimelStudio.utils import ConvertImageToWx
##        img= Image.open('Garden.jpg')
##        img.thumbnail((200, 200))
##        picture = wx.Bitmap(ConvertImageToWx(img))
##        self._assetlibrary.InsertPicture(1, picture)


        # Open the given file at the command line, if
        # there is one -otherwise load the default file.
        if self._arguments.file == 'DEFAULT_FILE':
            print('INFO: LOADING DEFAULT FILE')
            self._project.LoadDefaultProjectFile()
        else:
            print('INFO: LOADING FILE {} FROM CMD'.format(self._arguments.file))
            #self._project.OpenProjectFile(arguments.file)

##        from PIL import Image
##        renderimage = Image.new('RGBA', (256, 256), 'red')
##        self._imageviewport.RefreshViewerImage(
##            renderimage,
##            1.00
##            )
        #self._imageviewport.UpdateImage(renderimage)

        # Bindings
        self.Bind(wx.EVT_TOOL, self.OnRenderImage, id=ID_RENDERTOOLBAR_RENDERBTN)
        self.Bind(wx.EVT_TOOL, self.OnExportImage, id=ID_VIEWERTOOLBAR_EXPORTIMGBTN)
        if __DEBUG__ != True:
            self.Bind(wx.EVT_CLOSE, self.OnQuit)

        
    def GetArguments(self):
        return self._arguments

    def GetAUIManager(self):
        return self._mgr
    
    def GetRenderer(self):
        return self._renderer

    def GetProject(self):
        return self._project

    def GetUserPrefManager(self):
        return self._userprefmanager

    def GetImageViewport(self):
        return self._imageviewport

    def GetNodePropertyPanel(self):
        return self._nodepropertypanel

    def GetNodeGraph(self):
        return self._nodegraph

    def GetNodeRegistry(self): 
        return self._noderegistry

    def GetAutoRenderBoolean(self):
        return self._autoRenderCheckbox.GetValue()

    def OnAboutGimelStudioDialog(self, event):
        dialog = AboutGimelStudioDialog(self)
        dialog.ShowDialog()

    def OnGimelStudioLicenseDialog(self, event):
        dialog = GimelStudioLicenseDialog(self)
        dialog.ShowDialog()

    def OnExportImage(self, event):
        wildcard = "JPG file (*.jpg)|*.jpg|" \
                   "PNG file (*.png)|*.png|" \
                   "All files (*.*)|*.*"

        image = self._renderer.GetRenderedImage()

        dlg = wx.FileDialog(
            self, 
            message="Export rendered image as...", 
            defaultDir=os.getcwd(),
            defaultFile="image.png", 
            wildcard=wildcard, 
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
            )

        # This sets the default filter that the user will initially see. Otherwise,
        # the first filter in the list will be used by default.
        dlg.SetFilterIndex(2)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            image.save(path)
            #self.statusbar.SetStatusText("Image saved as: {}".format(path))
        dlg.Destroy()

    def OnRenderImage(self, event):
        self.Render()

    def OnTakeFeedbackSurvey(self, event):
        """ Go to the feedback survey webpage. """
        url = ("https://www.surveymonkey.com/r/RSRD556")
        webbrowser.open(url) 

    def OnToggleFullscreen(self, event):
        if self.IsMaximized() == False:
            self.Maximize()
        elif self.IsMaximized() == True:
            self.Restore()

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

        # Show the dialog and retrieve the user response. If it is the OK response,
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            paths = dlg.GetPaths()
            self._project.SaveProjectFile(paths[0])
            self.SetTitle("{0} - {1}".format(
                __TITLE__,
                dlg.GetFilename()
                ))
            
    
    def OnOpenFile(self, event):
        wildcard = "GIMEL STUDIO PROJECT file (*.gimel-studio-project)|*.gimel-studio-project|" \
                   "All files (*.*)|*.*"
                   
        dlg = wx.FileDialog(
            self, message="Open project file...",
            defaultDir='',
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW
            )

        # Show the dialog and retrieve the user response. If it is the OK response,
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            paths = dlg.GetPaths()
            self._project.OpenProjectFile(paths[0])
            self.SetTitle("{0} - {1}".format(
                __TITLE__,
                dlg.GetFilename()
                ))

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
            event.Veto()


    def BuildMenuBar(self):
        # Menubar        
        self.mainmenubar = wx.MenuBar()

        # File menu
        self.filemenu = wx.Menu()

        self.openfile_menuitem = wx.MenuItem(
            self.filemenu, 
            ID_MENU_OPENFILEMENUITEM, 
            "Open Project File...", 
            "Open and load a Gimel Studio project file"
            )
        self.filemenu.Append(self.openfile_menuitem)
        self.savefile_menuitem = wx.MenuItem(
            self.filemenu, 
            ID_MENU_SAVEFILEASMENUITEM, 
            "Save Project File As...", 
            "Save the current project as a Gimel Studio project file"
            )
        self.filemenu.Append(self.savefile_menuitem)
        self.filemenu.AppendSeparator()
        self.quit_menuitem = wx.MenuItem(
            self.filemenu, 
            ID_MENU_QUITMENUITEM, 
            "Quit", 
            "Quit Gimel Studio"
            )
        self.filemenu.Append(self.quit_menuitem)     

        self.mainmenubar.Append(self.filemenu, "File")


        # View menu
        self.viewmenu = wx.Menu()
        self.togglefullscreen_menuitem = wx.MenuItem(
            self.viewmenu, 
            ID_MENU_TOGGLEFULLSCREENMENUITEM, 
            "Fullscreen",  
            "Set the window size to fullscreen", wx.ITEM_CHECK
            )
        self.viewmenu.Append(self.togglefullscreen_menuitem)
        self.viewmenu.Check(ID_MENU_TOGGLEFULLSCREENMENUITEM, True)

        self.mainmenubar.Append(self.viewmenu, "View")

 
        # Help menu
        self.helpmenu = wx.Menu()

        self.takefeedbacksurvey_menuitem = wx.MenuItem(
            self.helpmenu, 
            ID_MENU_TAKEFEEDBACKSURVEYMENUITEM, 
            "Feedback Survey", 
            "Take a short survey online about what features you would like to see added and what needs to be improved in Gimel Studio"
            )
        #self.takefeedbacksurvey_menuitem.SetBitmap(ICON_MENU_ABOUTGIMELSTUDIO.GetBitmap())
        self.helpmenu.Append(self.takefeedbacksurvey_menuitem)
        
        self.license_menuitem = wx.MenuItem(
            self.helpmenu, 
            ID_MENU_LICENSEMENUITEM, 
            "License", 
            "Show Gimel Studio license"
            )
        #self.about_menuitem.SetBitmap(ICON_MENU_ABOUTGIMELSTUDIO.GetBitmap())
        self.helpmenu.Append(self.license_menuitem)

        self.about_menuitem = wx.MenuItem(
            self.helpmenu, 
            ID_MENU_ABOUTMENUITEM, 
            "About", 
            "Show information about GimelStudio"
            )
        #self.about_menuitem.SetBitmap(ICON_MENU_ABOUTGIMELSTUDIO.GetBitmap())
        self.helpmenu.Append(self.about_menuitem)

        self.mainmenubar.Append(self.helpmenu, "Help")


        self.SetMenuBar(self.mainmenubar)

        # Menubar bindings
        self.Bind(wx.EVT_MENU, self.OnOpenFile, id=ID_MENU_OPENFILEMENUITEM)
        #self.Bind(wx.EVT_MENU, self.OnSaveFile, id=ID_MENU_SAVEFILEMENUITEM)
        self.Bind(wx.EVT_MENU, self.OnSaveFileAs, id=ID_MENU_SAVEFILEASMENUITEM)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=ID_MENU_QUITMENUITEM)
        self.Bind(wx.EVT_MENU, self.OnToggleFullscreen, id=ID_MENU_TOGGLEFULLSCREENMENUITEM)
        self.Bind(wx.EVT_MENU, self.OnTakeFeedbackSurvey, id=ID_MENU_TAKEFEEDBACKSURVEYMENUITEM)
        self.Bind(wx.EVT_MENU, self.OnAboutGimelStudioDialog, id=ID_MENU_ABOUTMENUITEM)
        self.Bind(wx.EVT_MENU, self.OnGimelStudioLicenseDialog, id=ID_MENU_LICENSEMENUITEM)


    def Render(self):
        self._renderer.Render(self._nodegraph.GetNodes())
        renderimage = self._renderer.GetRenderTime()
        if renderimage != None:
            self._imageviewport.RefreshViewerImage(
                self._renderer.GetRenderedImage(),
                renderimage
                )
            self._imageviewport.SetNodesUsed(
                self._renderer.GetRenderedNodeCount()
                )
            self._nodegraph.UpdateAllNodes()  
