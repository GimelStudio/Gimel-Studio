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
## FILE: parameter.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the node parameter classes and readers
##
## This file includes code that was modified from imagegen 
## (https://github.com/nfactorial/imagegen) which is licensed 
## under the Apache License Version 2.0 
## Copyright 2016 nfactorial
## ----------------------------------------------------------------------------

from GimelStudio.utils import Color, RenderImage


def ReadFloatJSON(param, desc):
    """ Reads the float parameter value from the supplied json data. """
    if 'value' in desc:
        param.current_value = desc['value']
    else:
        param.current_value = param.definition.default_value

def ReadIntegerJSON(param, desc):
    """ Reads the integer parameter value from the supplied json data. """
    if 'value' in desc:
        param.current_value = int(desc['value'])
    else:
        param.current_value = param.definition.default_value

def ReadColorJSON(param, desc):
    """ Reads the color parameter value from the supplied json data. """
    param.current_value = Color(desc['rgb'][0], desc['rgb'][1], desc['rgb'][2])

def ReadImageJSON(param, desc):
    """ Reads the color parameter value from the supplied json data. """
    param.current_value = RenderImage('RGBA', (256, 256))
    

# This dictionary maps the parsing function to the parameter types
JSON_PARAM_READERS = {
    'float': ReadFloatJSON,
    'color': ReadColorJSON,
    'integer': ReadIntegerJSON,
    'image': ReadImageJSON
}


class ParameterDefinition(object):
    """
    Describes a parameter that is exposed within the application.
    Parameters are values that may be edited by the user, they may also be connected to
    the output of a node that computes a compatible value.
    The ParameterDefinition class is used to describe a parameter, however the Parameter
    class itself is used to represent an actual instance of a parameter.
    """
    def __init__(self, name, param_type=None, default_value=None):
        if param_type not in JSON_PARAM_READERS:
            raise TypeError
        self.read_json = JSON_PARAM_READERS[param_type]
        self.name = name
        self.param_type = param_type

        self.default_value = default_value
        self.node = None


class Parameter(object):
    """
    Represents an instance of a Parameter within the application.
    A parameter may be bound to a node as long as the nodes output type matches the parameter type.
    If a parameter has been bound, its 'binding' property will contain a reference to the node it
    has been bound to.
    """
    def __init__(self, definition):
        """
        Creates an instance of a parameter described by the supplied ParameterDefinition object.
        :param definition: ParameterDefinition that describes the parameter being represented.
        """
        self.definition = definition
        self.current_value = definition.default_value
        self.binding = None

    @property
    def name(self):
        """
        Retrieves the name associated with the parameter.
        :return: The name of the parameter.
        """
        return self.definition.name

    def ReadData(self, desc):
        """
        Reads the contents of the parameter from the supplied json data.
        """
        if 'bind' in desc:
            self.binding = desc['bind']
        else:
            self.definition.read_json(self, desc)
