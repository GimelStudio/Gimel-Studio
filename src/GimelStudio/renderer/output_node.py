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
## FILE: output_node.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Defines the output node in an abstract way
##
## This file includes code that was modified from imagegen 
## (https://github.com/nfactorial/imagegen) which is licensed 
## under the Apache License Version 2.0 
## Copyright 2016 nfactorial
## ----------------------------------------------------------------------------

from .eval_info import EvalInfo


class OutputNode(object):
    """
    This class describes the composite output node.
    """
    def __init__(self):
        self.node = None

    def ReadData(self, desc, nodes):
        """
        Reads the content of the supplied json data.
        """
        try:
            node = nodes[str(desc['bind'])]
            if node.IsDisabled() != True:
                self.node = node
            else:
                self.node = None
        except KeyError:
            self.node = None

    def RenderImage(self):
        """
        This method generates an image for this output node. If the output
        node is not connected then no image will be generated.
        """
        if self.node != None:
            eval_info = EvalInfo(self.node)
            image = eval_info.node.Evaluate(eval_info)
            return image
