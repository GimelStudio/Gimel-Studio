# ----------------------------------------------------------------------------
# Gimel Studio Copyright 2019-2021 by Noah Rahm and contributors
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
#
# FILE: application.py
# AUTHOR(S): Noah Rahm
# PURPOSE: Main application class which ties all the elements into one window
# ----------------------------------------------------------------------------

import os
import os.path
import shutil
import platform
import subprocess
import webbrowser

import wx
import wx.lib.agw.aui as aui
import wx.lib.delayedresult as delayedresult
import wx.lib.agw.flatmenu as flatmenu

from GimelStudio import utils
from GimelStudio import meta
from GimelStudio.interface import (NodeGraph, NodePropertyPanel,
                                   ImageViewport, NodeGraphDropTarget,
                                   DeveloperLog, DarkMenuRenderer, ExportImageAs)
from GimelStudio.program import (AboutDialog, LicenseDialog)
from GimelStudio.project import GimelStudioProject
from GimelStudio.renderer import Renderer, RenderThread, EVT_RENDER_RESULT
from GimelStudio.registry import REGISTERED_NODES
from GimelStudio.datafiles import *


class MainApplication(wx.Frame):
    def __init__(self, arguments):
        wx.Frame.__init__(self, None, title=meta.APP_TITLE, size=(1000, 800))

        self._arguments = arguments
        #self._launchedFromBlender = False


        # dirname = os.path.expanduser("~/.gimelstudio/blenderaddontemp/")
        # try:
        #     shutil.rmtree(dirname)
        # except OSError as e:
        #     print("Error: %s - %s." % (e.filename, e.strerror))

        # if not os.path.exists(dirname):
        #     os.makedirs(dirname, exist_ok=True)
        # else:
        #     pass

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
        self._project = GimelStudioProject(self)
        self._renderer = Renderer(self)
        # self._userPrefManager = UserPreferencesManager(self)

        # Load the user preferences from the .json file
        # otherwise use the default, built-in preferences.
        # self._userprefmanager.Load()
        # self._userprefmanager.Save()

    def _InitAUIManagerStyles(self):
        # Setup the AUI window manager and configure settings so
        # that we get the style that we want instead
        # of the yucky default colors. :)
        self._mgr = aui.AuiManager()
        art = self._mgr.GetArtProvider()
        self._mgr.SetManagedWindow(self)
        self._mgr.SetAGWFlags(self._mgr.GetAGWFlags() ^ aui.AUI_MGR_LIVE_RESIZE)

        art.SetMetric(aui.AUI_DOCKART_SASH_SIZE, 3)
        art.SetMetric(aui.AUI_DOCKART_PANE_BORDER_SIZE, 5)
        art.SetMetric(aui.AUI_DOCKART_GRADIENT_TYPE, aui.AUI_GRADIENT_NONE)
        art.SetColour(aui.AUI_DOCKART_BACKGROUND_COLOUR, wx.Colour("#404040"))
        art.SetColour(aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR, wx.Colour("#404040"))
        art.SetColour(aui.AUI_DOCKART_INACTIVE_CAPTION_TEXT_COLOUR, wx.Colour("#fff"))
        art.SetColour(aui.AUI_DOCKART_BORDER_COLOUR, wx.Colour("#404040"))
        art.SetColour(aui.AUI_DOCKART_SASH_COLOUR, wx.Colour("#333"))
        art.SetColour(aui.AUI_DOCKART_GRIPPER_COLOUR, wx.Colour("#404040"))

    def _InitMenuBar(self):
        # Create main sizer
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        # Create the menubar
        self._menubar = flatmenu.FlatMenuBar(self, wx.ID_ANY, 40, 8, options=0)

        # Set the dark theme
        rm = self._menubar.GetRendererManager()
        theme = rm.AddRenderer(DarkMenuRenderer())
        rm.SetTheme(theme)

        self._menubar.Refresh()
        self.Update()

        # Init menus
        file_menu = flatmenu.FlatMenu()
        view_menu = flatmenu.FlatMenu()
        render_menu = flatmenu.FlatMenu()
        window_menu = flatmenu.FlatMenu()
        help_menu = flatmenu.FlatMenu()

        # File
        self.openprojectfile_menuitem = flatmenu.FlatMenuItem(
            file_menu,
            id=wx.ID_ANY,
            label="Open Project\tCtrl+O",
            helpString="Open and load a Gimel Studio project file",
            kind=wx.ITEM_NORMAL,
            subMenu=None
        )

        self.saveprojectfile_menuitem = flatmenu.FlatMenuItem(
            file_menu,
            id=wx.ID_ANY,
            label="Save Project...\tCtrl+S",
            helpString="Save the current project file",
            kind=wx.ITEM_NORMAL,
            subMenu=None
        )

        self.saveprojectfileas_menuitem = flatmenu.FlatMenuItem(
            file_menu,
            id=wx.ID_ANY,
            label="Save Project As...\tCtrl+Shift+S",
            helpString="Save the current project as a Gimel Studio project file",
            kind=wx.ITEM_NORMAL,
            subMenu=None
        )

        self._menubar.AddSeparator()

        self.exportasimage_menuitem = flatmenu.FlatMenuItem(
            file_menu,
            id=wx.ID_ANY,
            label="Export Image As...\tShift+E",
            helpString="Export rendered composite image to a file",
            kind=wx.ITEM_NORMAL,
            subMenu=None
        )

        self._menubar.AddSeparator()

        self.quit_menuitem = flatmenu.FlatMenuItem(
            file_menu,
            id=wx.ID_ANY,
            label="Quit\tShift+Q",
            helpString="Quit Gimel Studio",
            kind=wx.ITEM_NORMAL,
            subMenu=None
        )

        # View
        self.togglenodegraphgrid_menuitem = flatmenu.FlatMenuItem(
            view_menu,
            id=wx.ID_ANY,
            label="Toggle Graph Grid",
            helpString="Toggle the Node Graph grid background",
            kind=wx.ITEM_CHECK,
            subMenu=None
        )

        self.renderasbackground_menuitem = flatmenu.FlatMenuItem(
            view_menu,
            id=wx.ID_ANY,
            label="Toggle Render as Background",
            helpString="Toggle the Render showing behind the Node Graph as the background",
            kind=wx.ITEM_CHECK,
            subMenu=None
        )

        self._menubar.AddSeparator()

        self.centernodegraph_menuitem = flatmenu.FlatMenuItem(
            view_menu,
            id=wx.ID_ANY,
            label="Center Node Graph",
            helpString="Move the view to the center of the Node Graph",
            kind=wx.ITEM_NORMAL,
            subMenu=None
        )

        # Render
        self.toggleautorender_menuitem = flatmenu.FlatMenuItem(
            render_menu,
            id=wx.ID_ANY,
            label="Auto Render",
            helpString="Toggle auto rendering after editing node properties, connections, etc",
            kind=wx.ITEM_CHECK,
            subMenu=None
        )

        self.renderimage_menuitem = flatmenu.FlatMenuItem(
            render_menu,
            id=wx.ID_ANY,
            label="Render Image \tF12",
            helpString="Force an immediate, updated render of the current node graph image",
            kind=wx.ITEM_NORMAL,
            subMenu=None
        )

        # Window
        self.togglefullscreen_menuitem = flatmenu.FlatMenuItem(
            window_menu,
            id=wx.ID_ANY,
            label="Toggle Window Fullscreen",
            helpString="Toggle the window fullscreen",
            kind=wx.ITEM_CHECK,
            subMenu=None
        )

        self.maximizewindow_menuitem = flatmenu.FlatMenuItem(
            window_menu,
            id=wx.ID_ANY,
            label="Maximize Window",
            helpString="Maximize the window size",
            kind=wx.ITEM_NORMAL,
            subMenu=None
        )

        self._menubar.AddSeparator()

        self.toggleimageviewport_menuitem = flatmenu.FlatMenuItem(
            window_menu,
            id=wx.ID_ANY,
            label="Show Image Viewport",
            helpString="Toggle showing the Image Viewport panel",
            kind=wx.ITEM_CHECK,
            subMenu=None
        )

        self.toggledevlog_menuitem = flatmenu.FlatMenuItem(
            window_menu,
            id=wx.ID_ANY,
            label="Show Developer Log",
            helpString="Toggle showing the Developer Log panel (this is useful if you are developing custom nodes with the Python API)",
            kind=wx.ITEM_CHECK,
            subMenu=None
        )

        # Help
        self.onlinedocs_menuitem = flatmenu.FlatMenuItem(
            help_menu,
            id=wx.ID_ANY,
            label="Online Manual",
            helpString="Open the Gimel Studio manual online in a browser",
            kind=wx.ITEM_NORMAL,
            subMenu=None
        )

        self._menubar.AddSeparator()

        self.visithomepage_menuitem = flatmenu.FlatMenuItem(
            help_menu,
            id=wx.ID_ANY,
            label="Visit Homepage",
            helpString="Visit the Gimel Studio homepage online",
            kind=wx.ITEM_NORMAL,
            subMenu=None
        )

        self.feedbacksurvey_menuitem = flatmenu.FlatMenuItem(
            help_menu,
            id=wx.ID_ANY,
            label="Feedback Survey",
            helpString="Take a short survey online about Gimel Studio v0.5.x beta",
            kind=wx.ITEM_NORMAL,
            subMenu=None
        )

        self.license_menuitem = flatmenu.FlatMenuItem(
            help_menu,
            id=wx.ID_ANY,
            label="License",
            helpString="Show Gimel Studio license",
            kind=wx.ITEM_NORMAL,
            subMenu=None
        )

        self._menubar.AddSeparator()

        self.about_menuitem = flatmenu.FlatMenuItem(
            help_menu,
            id=wx.ID_ANY,
            label="About",
            helpString="Show information about GimelStudio",
            kind=wx.ITEM_NORMAL,
            subMenu=None
        )

        # Append menu items to menus
        # file_menu.AppendItem(self.openprojectfile_menuitem)
        # file_menu.AppendItem(self.saveprojectfile_menuitem)
        # file_menu.AppendItem(self.saveprojectfileas_menuitem)
        file_menu.AppendItem(self.exportasimage_menuitem)
        file_menu.AppendItem(self.quit_menuitem)

        view_menu.AppendItem(self.togglenodegraphgrid_menuitem)
        view_menu.AppendItem(self.renderasbackground_menuitem)
        view_menu.AppendItem(self.centernodegraph_menuitem)

        render_menu.AppendItem(self.toggleautorender_menuitem)
        render_menu.AppendItem(self.renderimage_menuitem)

        window_menu.AppendItem(self.togglefullscreen_menuitem)
        window_menu.AppendItem(self.maximizewindow_menuitem)
        window_menu.AppendItem(self.toggleimageviewport_menuitem)
        window_menu.AppendItem(self.toggledevlog_menuitem)

        help_menu.AppendItem(self.onlinedocs_menuitem)
        help_menu.AppendItem(self.visithomepage_menuitem)
        help_menu.AppendItem(self.feedbacksurvey_menuitem)
        help_menu.AppendItem(self.license_menuitem)
        help_menu.AppendItem(self.about_menuitem)

        # Append menus to the menubar
        self._menubar.Append(file_menu, "File")
        self._menubar.Append(view_menu, "View")
        self._menubar.Append(render_menu, "Render")
        self._menubar.Append(window_menu, "Window")
        self._menubar.Append(help_menu, "Help")

        # Set defaults
        self.togglenodegraphgrid_menuitem.Check(True)
        self.toggleautorender_menuitem.Check(True)
        self.toggleimageviewport_menuitem.Check(True)
        self.renderasbackground_menuitem.Check(False)

        # Add menubar to main sizer
        self.mainSizer.Add(self._menubar, 0, wx.EXPAND)
        self.SetSizer(self.mainSizer)
        self.mainSizer.Layout()

        # Bind events
        self.Bind(flatmenu.EVT_FLAT_MENU_SELECTED,
                  self.OnExportImage, self.exportasimage_menuitem)
        self.Bind(flatmenu.EVT_FLAT_MENU_SELECTED,
                  self.OnQuit, self.quit_menuitem)

        self.Bind(flatmenu.EVT_FLAT_MENU_SELECTED,
                  self.OnToggleNodeGraphGrid, self.togglenodegraphgrid_menuitem)
        self.Bind(flatmenu.EVT_FLAT_MENU_SELECTED,
                  self.OnCenterNodeGraph, self.centernodegraph_menuitem)
        self.Bind(flatmenu.EVT_FLAT_MENU_SELECTED,
                  self.OnToggleRenderAsBackground, self.renderasbackground_menuitem)

        self.Bind(flatmenu.EVT_FLAT_MENU_SELECTED,
                  self.OnToggleAutoRender, self.toggleautorender_menuitem)
        self.Bind(flatmenu.EVT_FLAT_MENU_SELECTED,
                  self.OnRender, self.renderimage_menuitem)

        self.Bind(flatmenu.EVT_FLAT_MENU_SELECTED,
                  self.OnToggleFullscreen, self.togglefullscreen_menuitem)
        self.Bind(flatmenu.EVT_FLAT_MENU_SELECTED,
                  self.OnMaximizeWindow, self.maximizewindow_menuitem)
        self.Bind(flatmenu.EVT_FLAT_MENU_SELECTED,
                  self.OnToggleShowImageViewport, self.toggleimageviewport_menuitem)
        self.Bind(flatmenu.EVT_FLAT_MENU_SELECTED,
                  self.OnToggleDeveloperLog, self.toggledevlog_menuitem)

        self.Bind(flatmenu.EVT_FLAT_MENU_SELECTED,
                  self.OnReadOnlineDocs, self.onlinedocs_menuitem)
        self.Bind(flatmenu.EVT_FLAT_MENU_SELECTED,
                  self.OnVisitWebsite, self.visithomepage_menuitem)
        self.Bind(flatmenu.EVT_FLAT_MENU_SELECTED,
                  self.OnFeedbackSurvey, self.feedbacksurvey_menuitem)
        self.Bind(flatmenu.EVT_FLAT_MENU_SELECTED,
                  self.OnLicenseDialog, self.license_menuitem)
        self.Bind(flatmenu.EVT_FLAT_MENU_SELECTED,
                  self.OnAboutDialog, self.about_menuitem)

    def _InitUIPanels(self):
        # Image Viewport Panel
        self._imageViewport = ImageViewport(self)
        self._mgr.AddPane(
            self._imageViewport,
            aui.AuiPaneInfo()
            .Right()
            .Name("ImageViewport")
            .Caption("Image Viewport")
            .Icon(ICON_PANEL_IMAGE_VIEWPORT_LIGHT.GetBitmap())
            .CloseButton(visible=False)
            .BestSize(750, 500)
        )

        # Developer Log Panel
        self._developerLog = DeveloperLog(self)
        self._mgr.AddPane(
            self._developerLog,
            aui.AuiPaneInfo()
            .Left()
            .Name("DeveloperLog")
            .Caption("Developer Log")
            .Icon(ICON_PANEL_DEV_LOG_LIGHT.GetBitmap())
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
            .Icon(ICON_PANEL_NODE_PROPERTY_PANEL_LIGHT.GetBitmap())
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
            .Icon(ICON_PANEL_NODE_GRAPH_LIGHT.GetBitmap())
            .CloseButton(visible=False)
            .BestSize(750, 400)
            .Floatable(False)
            .Movable(False)
        )
        self._nodeGraph.RenderAsBackground(init=True)
        self._nodeGraph.InitMenuButton()

    def _SetupWindowStartup(self):
        # Import and register the nodes
        import GimelStudio.node_importer
        self._nodeRegistry = REGISTERED_NODES

        # Set statusbar
        self._statusBar = self.CreateStatusBar()
        self._statusBar.Hide()

        # Maximize the window & tell the AUI window
        # manager to "commit" all the changes just made, etc
        self.Maximize()
        self._menubar.PositionAUI(self._mgr)
        self._mgr.Update()
        self._menubar.Refresh()

        # Quit prompt dialog
        if meta.APP_DEBUG is not True:
            self.Bind(wx.EVT_CLOSE, self.OnQuit)

        self.Bind(wx.EVT_ACTIVATE, self.OnWindowActivate)

    def _SetupDefaultNodes(self):
        # Calculate center of Node Graph view
        rect = self._nodeGraph.GetSize()

        # 5000px is 1/2 the size of the Node Graph
        x, y = (rect[0] / 2) + 5000, (rect[1] / 2) + 5000


        # Always add the output node
        comp_node = self._nodeGraph.AddNode('corenode_outputcomposite',
                                            pos=wx.Point(x + 150, y))


        # If a path is passed into the "--blender" arg
        # set the Image node file path to that path.
        # if self._arguments.blender == "default":
        #     node = self._nodeGraph.AddNode('corenode_imagefromblender',
        #                                         pos=wx.Point(x - 340, y))
        #     node.NodeEditProp(idname="Layer", value="Layer 0", render=True)

        #     try:
        #         nodes = self._nodeGraph.GetNodesByTypeId("corenode_imagefromblender")
        #         for node in nodes:
        #             node.RefreshLayers()
        #     except:
        #         pass

        # else:
        img_node = self._nodeGraph.AddNode('corenode_image',
                                            pos=wx.Point(x - 340, y))

        if self._arguments.blender != "":
            img_node.NodeEditProp(
                idname="File Path",
                value=self._arguments.blender,
                render=False
            )

        # This node is here just for
        # testing during development.
        if meta.APP_DEBUG is True:
            self._nodeGraph.AddNode('corenode_alphacomposite',  # Put the node id you are testing here
                                    pos=wx.Point(x - 100, y))


    def OnWindowActivate(self, event):
        # Window is being focused
        if event.GetActive() is True:
            #print("focus")

            nodes = self._nodeGraph.GetNodesByTypeId("corenode_imagefromblender")
            for node in nodes:
                node.RefreshLayers()


    def OnExportImage(self, event):
        ExportImageAs(self, self._renderer.GetRender())

    def OnToggleLiveNodePreviewUpdate(self, event):
        if self.livenodepreviewupdate_menuitem.IsChecked() is False:
            self._nodeGraph.SetLiveNodePreviewUpdate(False)
        else:
            self._nodeGraph.SetLiveNodePreviewUpdate(True)

    def OnToggleRenderAsBackground(self, event):
        if self.renderasbackground_menuitem.IsChecked() is False:
            self._nodeGraph.SetRenderAsBackground(False)
        else:
            self._nodeGraph.SetRenderAsBackground(True)

    def OnToggleFullscreen(self, event):
        if self.togglefullscreen_menuitem.IsChecked() is False:
            self.ShowFullScreen(False)
        else:
            self.ShowFullScreen(True,
                                style=wx.FULLSCREEN_NOCAPTION | wx.FULLSCREEN_NOBORDER)

    def OnCenterNodeGraph(self, event):
        self._nodeGraph.CenterNodeGraph()

    def OnMaximizeWindow(self, event):
        self.Maximize()

    def OnToggleStatusbar(self, event):
        if self.togglestatusbar_menuitem.IsChecked() is False:
            self._statusBar.Hide()
        else:
            self._statusBar.Show()
        self.Layout()

    def OnToggleShowImageViewport(self, event):
        if self.toggleimageviewport_menuitem.IsChecked() is False:
            self._mgr.GetPane("ImageViewport").Hide()
        else:
            self._mgr.GetPane("ImageViewport").Show()

        self._mgr.Update()

    def OnToggleDeveloperLog(self, event):
        if self.toggledevlog_menuitem.IsChecked() is False:
            self._mgr.GetPane("DeveloperLog").Hide()
        else:
            self._mgr.GetPane("DeveloperLog").Show()

        self._mgr.Update()

    def OnToggleNodeGraphGrid(self, event):
        if self.togglenodegraphgrid_menuitem.IsChecked() is False:
            self._nodeGraph.SetShouldDrawGrid(False)
        else:
            self._nodeGraph.SetShouldDrawGrid(True)
        self._nodeGraph.RefreshGraph()

    def OnToggleAutoRender(self, event):
        if self.toggleautorender_menuitem.IsChecked() is False:
            self._nodeGraph.SetAutoRender(False)
        else:
            self._nodeGraph.SetAutoRender(True)
        self._nodeGraph.RefreshGraph()

    def OnRender(self, event):
        """ Event handler for rendering the current Node Graph. """
        self.Render()

    def OnQuit(self, event):
        quitdialog = wx.MessageDialog(self,
                                      "Do you really want to quit? You will lose any unsaved data.",
                                      "Quit Gimel Studio?",
                                      wx.YES_NO | wx.YES_DEFAULT)

        if quitdialog.ShowModal() is wx.ID_YES:
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
        if meta.ENABLE_THREADING is True:
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
            if render_image is not None:
                self._imageViewport.UpdateViewerImage(utils.ConvertImageToWx(render_image),
                                                      self._renderer.GetTime())
            self._imageViewport.UpdateInfoText(False)
            self._nodeGraph.UpdateAllNodes()

    def _Render(self, jobID, abort_event):
        """ Internal rendering method. """
        if not abort_event():
            self._imageViewport.UpdateRenderText(True)
            self._renderer.Render(self._nodeGraph.GetNodes())
            render_time = self._renderer.GetTime()
            render_image = self._renderer.GetRender()
            if render_image is not None:
                self._imageViewport.UpdateViewerImage(utils.ConvertImageToWx(render_image),
                                                      render_time)
                self._abortEvent.set()
        else:
            self._abortEvent.clear()

        self._imageViewport.UpdateRenderText(False)
        return jobID

    def _PostRender(self, delayed_result):
        """ Internal post-render misc. """
        try:
            result = delayed_result.get()

            self._imageViewport.UpdateViewerImage(utils.ConvertImageToWx(self._renderer.GetRender()),
                                                  self._renderer.GetTime())
            self._imageViewport.UpdateRenderText(False)
            self._statusBar.SetStatusText("Render Finished in {} sec.".format(self._renderer.GetTime()))

            self._nodeGraph.UpdateAllNodes()

            self._abortEvent.clear()
            return result
        except Exception as exc:
            print('ERROR: PLEASE REPORT THE FOLLOWING ERROR TO THE DEVELOPERS: \n', exc)
            return
