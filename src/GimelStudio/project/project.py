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

import io
import pickle
import os.path
import json

import wx

from PIL import Image
import numpy as np

from GimelStudio.meta import (__NAME__, __AUTHOR__, __VERSION__,
                              __DEBUG__, __TITLE__)



class GimelStudioProject(object):
    def __init__(self, parent):
        self._parent = parent
        self._version = __VERSION__

        #self._nodes = {}
        #self._projectData = {}

    def OpenProjectFile(self, path):
        """ Opens a Gimel Studio Project file at the given path. """
        # with open(path, "r") as project_file:
        #     project_data = json.load(project_file)

        with open(path, 'rb') as project_file:
            project_data = pickle.load(project_file)
        
        node_data = project_data["nodes"]
        meta_data = project_data["meta"]
        #ui_data = project_data["ui"]
        
        if meta_data["application_version"] == "0.4.0":

            #self._CreateUI(ui_data)
            self._CreateNodes(node_data)

        else:
            print("Files earlier than v0.4.0")
        
        #self._parent.Render()


    def SaveProjectFile(self, path):
        project_data = {}

        node_data = self._GetNodeData()
        meta_data = self._GetMetaData()
        #ui_data = self._GetUIData()

        #print(meta_data, node_data, layout_data)

        project_data["nodes"] = node_data
        project_data["meta"] = meta_data
        #project_data["ui"] = ui_data

        #print(project_data)

        # with open(path, "w") as project_file:
        #     json.dump(project_data, project_file)  

        with open(path, 'wb') as project_file:
            pickle.dump(project_data, project_file, pickle.DEFAULT_PROTOCOL)


    def _GetNodeData(self):   
        node_data = {}

        for node_id in self._parent._nodeGraph.GetNodes():
            node = self._parent._nodeGraph._nodes[node_id]
            node_id = str(node_id)

            node_data[node_id] = {
                "evaldata": node.GetEvaluationData(),
                "position": [node.GetRect()[0], node.GetRect()[1]],
                "name": node.GetIDName(),
                "active": node.IsActive(),
                "selected": node.IsSelected(),
                "disabled": node.IsDisabled(),
            }

            # Check if the node supports packing 
            # images into the file.
            if node.GetSupportsImagePacking() == True:

                # Convert the image to a numpy array before
                # packing into the file.
                img_data = np.asarray(node.GetPackedImageData())
                node_data[node_id]["packed_data"] = img_data
                node_data[node_id]["supports_packing"] = True

            else:
                node_data[node_id]["supports_packing"] = False

        return node_data

    def _GetMetaData(self):
        meta_data = {}
        meta_data["file_content"] = "Gimel Studio Project file"
        meta_data["application_version"] = self._version

        return meta_data

    # def _GetUIData(self):
    #     ui_data = {}
    #     ui_data["perspective"] = str(self._parent._mgr.SavePerspective())

    #     return ui_data

 
    def _CreateNodes(self, node_data):

        # Reset node graph
        self._parent._nodeGraph.ResetToDefault()
 
        # Create the nodes
        nodes = self._parent._nodeGraph.GetNodes()
        #print(node_data)
        for node_id in node_data:
            nd = node_data[node_id]

            node = self._parent._nodeGraph.AddNode(
                nd["name"],  
                int(node_id),
                wx.Point(nd["position"][0], nd["position"][1])
                )
            node.SetData(nd["evaldata"])

            if node.GetSupportsImagePacking() == True:

                img = Image.fromarray(nd["packed_data"])
                node.UpdatePackedImageData(img)
            else:
                pass

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


        # Connect the nodes
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
        #self._parent._nodeGraph.RefreshGraph()
        self._parent._nodeGraph._parent.Render()


    def _CreateUI(self, ui_data):
        #pass
        try:
            pass
            #self._parent._mgr.LoadPerspective(ui_data["perspective"])
        except:
            pass

  
