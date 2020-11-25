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
##
## FILE: application.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Main application class which ties all the elements into one window
## ----------------------------------------------------------------------------

import os
import platform
import subprocess
import webbrowser

import wx
import wx.lib.agw.aui as aui
import wx.lib.delayedresult as delayedresult

from GimelStudio import utils
from GimelStudio import meta
from GimelStudio.file_support import SupportFTSave
from GimelStudio.interface import (
    NodeGraph, NodePropertyPanel,
    ImageViewport, NodeGraphDropTarget,
    DeveloperLog
    )
from GimelStudio.program import (
    AboutDialog, LicenseDialog
    )
from GimelStudio.renderer import (
    Renderer, RenderThread, EVT_RENDER_RESULT
    )
from GimelStudio.datafiles import *

from GimelStudio.registry import REGISTERED_NODES


class MainApplication(wx.Frame):
    def __init__(self, arguments):
        wx.Frame.__init__(self, None, title=meta.APP_TITLE, size=(1000, 800))

        self._arguments = arguments

        # Threading
        self._jobID = 0
        self._abortEvent = delayedresult.AbortEvent()

        # Set the program icon
        self.SetIcon(ICON_GIMELSTUDIO_ICO.GetIcon())

        # Init everything
        self._InitApp()

    def _InitApp(self):
        self._InitProgramBackend()
        self._InitAUIManagerStyles()
        self._InitMenuBar()
        self._InitUIPanels()
        self._SetupWindowStartup()
        self._SetupDefaultNodes()

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
        art = self._mgr.GetArtProvider()
        self._mgr.SetManagedWindow(self)
        self._mgr.SetAGWFlags(self._mgr.GetAGWFlags() ^ aui.AUI_MGR_LIVE_RESIZE)

        art.SetMetric(aui.AUI_DOCKART_SASH_SIZE, 2)
        art.SetMetric(aui.AUI_DOCKART_PANE_BORDER_SIZE, 3)
        art.SetMetric(aui.AUI_DOCKART_GRADIENT_TYPE, aui.AUI_GRADIENT_NONE)
        art.SetColour(aui.AUI_DOCKART_BACKGROUND_COLOUR, wx.Colour("#fff"))
        art.SetColour(aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR, wx.Colour("#fff"))
        art.SetColour(aui.AUI_DOCKART_INACTIVE_CAPTION_TEXT_COLOUR, wx.Colour("#000"))
        art.SetColour(aui.AUI_DOCKART_BORDER_COLOUR, wx.Colour("#fff"))
        art.SetColour(aui.AUI_DOCKART_SASH_COLOUR, wx.Colour("#fff"))
        art.SetColour(aui.AUI_DOCKART_GRIPPER_COLOUR, wx.Colour("#fff"))

    def _InitMenuBar(self):
        # Menubar
        self.mainmenubar = wx.MenuBar()

        # File menu
        self.filemenu = wx.Menu()

        # self.openproject_menuitem = wx.MenuItem(
        #     self.filemenu,
        #     wx.ID_ANY,
        #     "Open Project... \tCtrl+O",
        #     "Open and load a Gimel Studio project file"
        #     )
        # self.filemenu.Append(self.openproject_menuitem)

        # self.saveproject_menuitem = wx.MenuItem(
        #     self.filemenu,
        #     wx.ID_ANY,
        #     "Save Project... \tCtrl+S",
        #     "Save the current Gimel Studio project file"
        #     )
        # self.filemenu.Append(self.saveproject_menuitem)
        # #if self.GetActiveProjectFile() == None:
        # #    self.saveproject_menuitem.Enable(False)

        # self.saveprojectas_menuitem = wx.MenuItem(
        #     self.filemenu,
        #     wx.ID_ANY,
        #     "Save Project As... \tCtrl+Shift+S",
        #     "Save the current project as a Gimel Studio project file"
        #     )
        # self.filemenu.Append(self.saveprojectas_menuitem)

        # self.filemenu.AppendSeparator()

        self.exportimage_menuitem = wx.MenuItem(
            self.filemenu,
            wx.ID_ANY,
            "Export Image As... \tCtrl+E",
            "Export rendered composite image to a file"
            )
        self.filemenu.Append(self.exportimage_menuitem)

        self.filemenu.AppendSeparator()

        self.quit_menuitem = wx.MenuItem(
            self.filemenu,
            wx.ID_ANY,
            "Quit \tCtrl+Q",
            "Quit Gimel Studio"
            )
        self.filemenu.Append(self.quit_menuitem)

        self.mainmenubar.Append(self.filemenu, "File")

        # View menu
        self.viewmenu = wx.Menu()

        self.livenodepreviewupdate_menuitem = wx.MenuItem(
            self.viewmenu,
            wx.ID_ANY,
            "Live Node Previews",
            "Toggle showing live node previews as the renderer is processing each node, at the cost of a slightly longer render",
            wx.ITEM_CHECK
            )
        #self.viewmenu.Append(self.livenodepreviewupdate_menuitem)
        #self.viewmenu.Check(self.livenodepreviewupdate_menuitem.GetId(), True)

        self.togglenodegraphgrid_menuitem = wx.MenuItem(
            self.viewmenu,
            wx.ID_ANY,
            "Node Graph Grid",
            "Toggle the Node Graph grid background",
            wx.ITEM_CHECK
            )
        self.viewmenu.Append(self.togglenodegraphgrid_menuitem)
        self.viewmenu.Check(self.togglenodegraphgrid_menuitem.GetId(), True)

        self.viewmenu.AppendSeparator()

        self.centernodegraph_menuitem = wx.MenuItem(
            self.viewmenu,
            wx.ID_ANY,
            "Center Node Graph",
            "Move the view to the center of the Node Graph"
            )
        self.viewmenu.Append(self.centernodegraph_menuitem)

        self.mainmenubar.Append(self.viewmenu, "View")


        # Render menu
        self.rendermenu = wx.Menu()

        self.toggleautorender_menuitem = wx.MenuItem(
            self.rendermenu,
            wx.ID_ANY,
            "Auto Render",
            "Toggle auto rendering after editing node properties, connections, etc",
            wx.ITEM_CHECK
            )
        self.rendermenu.Append(self.toggleautorender_menuitem)
        self.rendermenu.Check(self.toggleautorender_menuitem.GetId(), True)

        self.renderimage_menuitem = wx.MenuItem(
            self.rendermenu,
            wx.ID_ANY,
            "Render Image \tF12",
            "Force an immediate, updated render of the current node graph image"
            )
        self.rendermenu.Append(self.renderimage_menuitem)

        self.mainmenubar.Append(self.rendermenu, "Render")


        # Window menu
        self.windowmenu = wx.Menu()

        self.togglefullscreen_menuitem = wx.MenuItem(
            self.windowmenu,
            wx.ID_ANY,
            "Toggle Window Fullscreen",
            "Toggle the window fullscreen",
            wx.ITEM_CHECK
            )
        self.windowmenu.Append(self.togglefullscreen_menuitem)

        self.maximizewindow_menuitem = wx.MenuItem(
            self.windowmenu,
            wx.ID_ANY,
            "Maximize Window",
            "Maximize the window size"
            )
        self.windowmenu.Append(self.maximizewindow_menuitem)

        self.windowmenu.AppendSeparator()

        self.toggleimageviewport_menuitem = wx.MenuItem(
            self.windowmenu,
            wx.ID_ANY,
            "Show Image Viewport",
            "Toggle showing the Image Viewport panel",
            wx.ITEM_CHECK
            )
        self.windowmenu.Append(self.toggleimageviewport_menuitem)
        self.windowmenu.Check(self.toggleimageviewport_menuitem.GetId(), True)

        self.togglestatusbar_menuitem = wx.MenuItem(
            self.windowmenu,
            wx.ID_ANY,
            "Show Statusbar",
            "Toggle showing the statusbar",
            wx.ITEM_CHECK
            )
        self.windowmenu.Append(self.togglestatusbar_menuitem)
        self.windowmenu.Check(self.togglestatusbar_menuitem.GetId(), True)

        self.windowmenu.AppendSeparator()

        self.toggledevlog_menuitem = wx.MenuItem(
            self.windowmenu,
            wx.ID_ANY,
            "Show Developer Log",
            "Toggle showing the Developer Log panel (this is useful if you are developing custom nodes with the Python API)",
            wx.ITEM_CHECK
            )
        self.windowmenu.Append(self.toggledevlog_menuitem)
        self.windowmenu.Check(self.toggledevlog_menuitem.GetId(), False)

        self.mainmenubar.Append(self.windowmenu, "Window")


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
        self.Bind(wx.EVT_MENU,
            self.OnExportImage,
            self.exportimage_menuitem
            )
        self.Bind(wx.EVT_MENU,
            self.OnQuit,
            self.quit_menuitem
            )

        self.Bind(wx.EVT_MENU,
            self.OnToggleLiveNodePreviewUpdate,
            self.livenodepreviewupdate_menuitem
            )
        self.Bind(wx.EVT_MENU,
            self.OnToggleNodeGraphGrid,
            self.togglenodegraphgrid_menuitem
            )
        self.Bind(wx.EVT_MENU,
            self.OnCenterNodeGraph,
            self.centernodegraph_menuitem
            )

        self.Bind(wx.EVT_MENU, self.OnToggleFullscreen,
            self.togglefullscreen_menuitem
            )
        self.Bind(wx.EVT_MENU,
            self.OnToggleStatusbar,
            self.togglestatusbar_menuitem
            )
        self.Bind(wx.EVT_MENU,
            self.OnToggleShowImageViewport,
            self.toggleimageviewport_menuitem
            )
        self.Bind(wx.EVT_MENU,
            self.OnToggleDeveloperLog,
            self.toggledevlog_menuitem
            )



        self.Bind(wx.EVT_MENU,
            self.OnMaximizeWindow,
            self.maximizewindow_menuitem
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
        self._imageViewport = ImageViewport(self)
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

        self._developerLog = DeveloperLog(self)
        self._mgr.AddPane(
            self._developerLog,
            aui.AuiPaneInfo()
            .Left()
            .Name("DeveloperLog")
            .Caption("Developer Log")
            .Icon(ICON_PANEL_DEV_LOG_DARK.GetBitmap())
            .CloseButton(visible=False)
            .BestSize(750, 500)
            .Hide()
            )

        # Node Properties Panel
        self._nodePropertyPanel = NodePropertyPanel(self, (500, 800))
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
        self._nodeGraph = NodeGraph(self, (600, 600))
        # Drag image from dir or Node Registry into
        # node graph to create image node
        self._nodeGraph.SetDropTarget(NodeGraphDropTarget(self._nodeGraph))
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
        self._nodeGraph.InitMenuButton()

    def _SetupWindowStartup(self):
        # Import and register the nodes
        import GimelStudio.node_importer

        # Set statusbar
        self._statusBar = self.CreateStatusBar()

        #FIXME: move
        self._nodeRegistry = REGISTERED_NODES

        # Maximize the window & tell the AUI window
        # manager to "commit" all the changes just made.
        self.Maximize()
        self._mgr.Update()

        # Quit prompt dialog
        if meta.APP_DEBUG != True:
            self.Bind(wx.EVT_CLOSE, self.OnQuit)

    def _SetupDefaultNodes(self):
        # Calculate center of Node Graph view
        rect = self._nodeGraph.GetSize()

        # 5000px is 1/2 the size of the Node Graph
        x, y = (rect[0]/2)+5000, (rect[1]/2)+5000

        # Add default nodes
        img_node = self._nodeGraph.AddNode(
            'corenode_image',
            pos=wx.Point(x-340, y)
            )

        comp_node = self._nodeGraph.AddNode(
            'corenode_outputcomposite',
            pos=wx.Point(x+150, y)
            )

        # This node is here just for
        # testing during development.
        if meta.APP_DEBUG == True:
            self._nodeGraph.AddNode(
                'corenode_alphacomposite', # Put the node id you are testing here
                pos=wx.Point(x-100, y)
                )

        # If a path is passed into the "--blender" arg
        # set the Image node file path to that path.
        if self._arguments.blender != "":
            img_node.NodeEditProp(
                idname="File Path",
                value=self._arguments.blender,
                render=False
            )


    def OnExportImage(self, event):
        wildcard = "JPG file (*.jpg)|*.jpg|" \
                   "JPEG file (*.jpeg)|*.jpeg|" \
                   "PNG file (*.png)|*.png|" \
                   "BMP file (*.bmp)|*.bmp|" \
                   "GIF file (*.gif)|*.gif|" \
                   "EPS file (*.eps)|*.eps|" \
                   "PCX file (*.pcx)|*.pcx|" \
                   "XBM file (*.xbm)|*.xbm|" \
                   "WEBP file (*.webp)|*.webp|" \
                   "TGA file (*.tga)|*.tga|" \
                   "TIFF file (*.tiff)|*.tiff|" \
                   "All files (*.*)|*.*"

        dlg = wx.FileDialog(
            self,
            message="Export rendered image as...",
            defaultDir=os.getcwd(),
            defaultFile="untitled.png",
            wildcard=wildcard,
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
            )
        dlg.Center()

        # This sets the default filter that the user will initially see.
        # Otherwise, the first filter in the list will be used by default.
        dlg.SetFilterIndex(11)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            filetype = os.path.splitext(path)[1]

            if filetype not in SupportFTSave(list_all=True):
                dlg = wx.MessageDialog(
                    None,
                    "That file type isn't currently supported!",
                    "Cannot Save Image!",
                    style=wx.ICON_EXCLAMATION
                    )
                dlg.ShowModal()

            else:

                # Export the image with the export options
                utils.ExportRenderedImageToFile(
                    self._renderer.GetRender(),
                    path
                    )

                self.PopOpenExplorer(path)

                notify = wx.adv.NotificationMessage(
                    title="Image Exported Sucessfully",
                    message="Your image was exported to \n {}".format(path),
                    parent=None, flags=wx.ICON_INFORMATION)
                notify.Show(timeout=2) # 1 for short timeout, 100 for long timeout

        dlg.Destroy()

    def PopOpenExplorer(self, path):
        """ Method for opening the path in the system's File Explorer or Image viewer.

        Copied directly from:
        https://stackoverflow.com/questions/6631299/python-opening-a-folder-in-explorer-nautilus-finder
        """
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    def OnToggleLiveNodePreviewUpdate(self, event):
        if self.livenodepreviewupdate_menuitem.IsChecked() == False:
            self._nodeGraph.SetLiveNodePreviewUpdate(False)
        else:
            self._nodeGraph.SetLiveNodePreviewUpdate(True)


    def OnToggleFullscreen(self, event):
        if self.togglefullscreen_menuitem.IsChecked() == False:
            self.ShowFullScreen(False)
        else:
            self.ShowFullScreen(
                True,
                style=wx.FULLSCREEN_NOCAPTION | wx.FULLSCREEN_NOBORDER
                )

    def OnCenterNodeGraph(self, event):
        self._nodeGraph.CenterNodeGraph()

    def OnMaximizeWindow(self, event):
        self.Maximize()

    def OnToggleStatusbar(self, event):
        if self.togglestatusbar_menuitem.IsChecked() == False:
            self._statusBar.Hide()
        else:
            self._statusBar.Show()
        self.Layout()

    def OnToggleShowImageViewport(self, event):
        if self.toggleimageviewport_menuitem.IsChecked() == False:
            self._mgr.GetPane("ImageViewport").Hide()
        else:
            self._mgr.GetPane("ImageViewport").Show()

        #self._mgr.MaximizePane(self._mgr.GetPane("NodeGraph"))
        #RestoreMaximizedPane()
        self._mgr.Update()

    def OnToggleDeveloperLog(self, event):
        if self.toggledevlog_menuitem.IsChecked() == False:
            self._mgr.GetPane("DeveloperLog").Hide()
        else:
            self._mgr.GetPane("DeveloperLog").Show()

        self._mgr.Update()

    def OnToggleNodeGraphGrid(self, event):
        if self.togglenodegraphgrid_menuitem.IsChecked() == False:
            self._nodeGraph.SetShouldDrawGrid(False)
        else:
            self._nodeGraph.SetShouldDrawGrid(True)
        self._nodeGraph.RefreshGraph()

    def OnToggleAutoRender(self, event):
        if self.toggleautorender_menuitem.IsChecked() == False:
            self._nodeGraph.SetAutoRender(False)
        else:
            self._nodeGraph.SetAutoRender(True)
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
        url = ("https://www.surveymonkey.com/r/V23MV7Q")
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
        method, called when the Node Graph image is to be rendered. After this is
        complete, the result event will be called.
        """
        if meta.ENABLE_THREADING == True:
            self._abortEvent.clear()
            self._jobID += 1
            delayedresult.startWorker(
                self._PostRender,
                self._Render,
                wargs=(self._jobID, self._abortEvent),
                jobID=self._jobID
            )
        else:
            self._imageViewport.UpdateInfoText(True)
            self._renderer.Render(self._nodeGraph.GetNodes())
            render_image = self._renderer.GetRender()
            if render_image != None:
                self._imageViewport.UpdateViewerImage(
                    utils.ConvertImageToWx(render_image),
                    self._renderer.GetTime()
                    )
            self._imageViewport.UpdateInfoText(False)
            self._nodeGraph.UpdateAllNodes()

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

    def _PostRender(self, delayed_result):
        """ Internal post-render misc. """
        try:
            result = delayed_result.get()

            self._imageViewport.UpdateViewerImage(
                utils.ConvertImageToWx(self._renderer.GetRender()),
                self._renderer.GetTime()
                )
            self._imageViewport.UpdateRenderText(False)
            self._statusBar.SetStatusText(
                "Render Finished in {} sec.".format(self._renderer.GetTime())
                )

            self._nodeGraph.UpdateAllNodes()

            self._abortEvent.clear()
            return result
        except Exception as exc:
            print('ERROR: PLEASE REPORT THE FOLLOWING ERROR TO THE DEVELOPERS: \n', exc)
            return
