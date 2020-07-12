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
## FILE: project.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define class which handles .gimel-studio-project save, open, etc.
## ----------------------------------------------------------------------------


# VERY WORK IN PROGRESS!!!


import json
import wx

from GimelStudio.meta import (__NAME__, __AUTHOR__, __VERSION__,
                              __BUILD__, __RELEASE__, __DEBUG__,
                              __TITLE__)

DEFAULT_PROJECT = {
    "nodes": {
        "-31962": {
            "evaldata": {"bind": "-31956"},
            "position": [915, 222],
            "name": "corenode_outputcomposite",
            "disabled": False
            },
        "-31956": {
            "evaldata": {"parameters": [], "properties": [{"name": "Path", "value": ""}]},
            "position": [563, 205],
            "name": "corenode_image",
            "disabled": False
            }
        },
    "meta": {
        "content": "Gimel Studio project file",
        "version": "{}.{}".format(__VERSION__, __RELEASE__)
        },
    "ui": {
        }
    }


class GimelStudioProject(object):
    def __init__(self, parent, version, build, release):
        self._parent = parent
        self._version = version
        self._build = build
        self._release = release
        #self._nodes = {}
        #self._projectData = {}


    def LoadDefaultProjectFile(self):
        """ Load the default project file. """
        print("UNUSED!!")
        # node_data = DEFAULT_PROJECT["nodes"]
        # meta_data = DEFAULT_PROJECT["meta"]
        # ui_data = DEFAULT_PROJECT["ui"]

        # self._CreateNodes(node_data)
        #self._CreateUI(ui_data)

    def OpenProjectFile(self, path):
        """ Opens a Gimel Studio Project file at the given path. """
        with open(path, "r") as project_file:
            project_data = json.load(project_file)
        
        node_data = project_data["nodes"]
        meta_data = project_data["meta"]
        ui_data = project_data["ui"]
        
        self._CreateUI(ui_data)
        self._CreateNodes(node_data)
        
        #self._parent.Render()


    def SaveProjectFile(self, path):
        project_data = {}

        node_data = self._GetNodeData()
        meta_data = self._GetMetaData()
        ui_data = self._GetUIData()

        #print(meta_data, node_data, layout_data)

        project_data["nodes"] = node_data
        project_data["meta"] = meta_data
        project_data["ui"] = ui_data

        #print(project_data)

        with open(path, "w") as project_file:
            json.dump(project_data, project_file)  


    def _GetNodeData(self):   
        node_data = {}
        for nodeId in self._parent._nodeGraph.GetNodes():
            #print(nodeId)
            node = self._parent._nodeGraph._nodes[nodeId]

            #print(node._evaluationData)

            node_data[str(nodeId)] = {
                "evaldata": node.GetEvaluationData(),
                "position": [node.GetRect()[0], node.GetRect()[1]],
                "name": node.GetIDName(),
                #"active": node.IsActive(),
                #"selected": node.IsSelected(),
                "disabled": node.IsDisabled(),
            }

        return node_data

    def _GetMetaData(self):
        meta_data = {}
        meta_data["content"] = "Gimel Studio Project file"
        meta_data["version"] = self._version
        meta_data["build"] = self._build
        meta_data["release"] = self._release

        return meta_data

    def _GetUIData(self):
        ui_data = {}
        ui_data["perspective"] = str(self._parent._mgr.SavePerspective())

        return ui_data

 
    def _CreateNodes(self, node_data):

        self._parent._nodeGraph.ResetToDefault()
        # Should a new ID be assigned to the nodes?
 
        nodes = self._parent._nodeGraph.GetNodes()
        #print(nodes, '<<<--NODES')
        for nodeId in node_data:
            nd = node_data[nodeId]

            node = self._parent._nodeGraph.AddNode(
                nd["name"],  
                int(nodeId),
                wx.Point(nd["position"][0], nd["position"][1])
                )
            node.SetData(nd["evaldata"])
            #print(node._evalData, '<<<<<<<<<<')

            # print(nodeId,  ' ID', nd["name"])

            # if nd["selected"] == True:
            #     node.SetSelected(True)
            # else:
            #     node.SetSelected(False)

            # if nd["active"] == True:
            #     node.SetActive(True)
            # else:
            #     node.SetActive(False)

            # if nd["disabled"] == True:
            #     node.SetDisabled(True)
            # else: 
            #     node.SetDisabled(False)

        nodes = self._parent._nodeGraph.GetNodes()
        #print(nodes, '<<<--NODES')
        for nodeId in nodes:
            if nodes[nodeId].IsCompositeOutput() != True:
                # pass
                for param in node_data[str(nodeId)]["evaldata"]["parameters"]:
                    node2 = nodes[nodeId]
                    node1 = nodes[int(param["bind"])]
                    #print(param["bind"], nodeId)
                    node1.FindPlug('Output').Connect(node2.FindPlug(param["name"]), render=False)
            else:
                if node_data[str(nodeId)]["evaldata"] != '':
                    node2 = nodes[nodeId]
                    node1 = nodes[int(node_data[str(nodeId)]["evaldata"]["bind"])]
                    node1.FindPlug('Output').Connect(node2.FindPlug('Image'), render=False)
                    #self._parent.nodegraph.RefreshGraph()

            # We need these redraws here (even though we draw again later)
            # otherwise one node seems to not be drawn on file open.
            #nodes[nodeId].Draw(self._parent.nodegraph.GetPDC())
 
            # for plug in nodes[nodeId].GetPlugs():
            #     for wire in plug.GetWires():
            #         wire.Draw(self._parent.nodegraph.GetPDC())
         
        self._parent._nodeGraph.UpdateAllNodes()
        self._parent._nodeGraph.RefreshGraph()
        self._parent._nodeGraph._parent.Render()


    def _CreateUI(self, ui_data):
        #pass
        try:
            pass
            #self._parent._mgr.LoadPerspective(ui_data["perspective"])
        except:
            pass

  
