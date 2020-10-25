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
## FILE: eval_info.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Supply an evaluation function for computing a node's value
##
## This file includes code that was modified from imagegen
## (https://github.com/nfactorial/imagegen) which is licensed
## under the Apache License Version 2.0
## Copyright 2016 nfactorial
## ----------------------------------------------------------------------------


class EvalInfo(object):
    """
    Evaluate node properties and parameters
    """
    def __init__(self, node):
        if node == None:
            raise TypeError
        self.node = node

    def EvaluateParameter(self, name):
        """
        Evaluates the value of a parameter.
        """
        p = self.node.Parameters[name]
        if p.binding:
            # Make sure the next node is not disabled
            if p.binding.IsMuted() != True:
                # Evaluate the next node
                info = EvalInfo(p.binding)
                return p.binding.EvaluateNode(info)
        return p.value


    def EvaluateProperty(self, name):
        """
        Evaluates the value of a property.
        """
        p = self.node.Properties[name]
        return p.value
