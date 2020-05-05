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
## FILE: property.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the node property classes and readers
##
## This file includes code that was modified from imagegen 
## (https://github.com/nfactorial/imagegen) which is licensed 
## under the Apache License Version 2.0 
## Copyright 2016 nfactorial
## ----------------------------------------------------------------------------

from GimelStudio.utils import Color, RenderImage, List


# TODO: remove the unused(?) readers / combine the readers
def ReadFilepathJSON(prop, desc):
    if 'value' in desc:
        prop.current_value = desc['value']
    else:
        prop.current_value = prop.definition.value
        
def ReadStringJSON(prop, desc):
    if 'value' in desc:
        prop.current_value = desc['value']
    else:
        prop.current_value = prop.definition.value        

def ReadListJSON(prop, desc):
    if 'value' in desc:
        prop.current_value = desc['value']
    else:
        prop.current_value = prop.definition.value.GetValue()

def ReadReglistJSON(prop, desc):
    if 'value' in desc:
        prop.current_value = desc['value']
    else:
        prop.current_value = prop.definition.value

def ReadIntegerJSON(prop, desc):
    if 'value' in desc:
        prop.current_value = desc['value']
    else:
        prop.current_value = prop.definition.value

def ReadColorJSON(prop, desc):
    if 'value' in desc:
        prop.current_value = desc['value']
    else:
        prop.current_value = prop.definition.value

def ReadFloatJSON(prop, desc):
    if 'value' in desc:
        prop.current_value = desc['value']
    else:
        prop.current_value = prop.definition.value

def ReadBooleanJSON(prop, desc):
    if 'value' in desc:
        prop.current_value = desc['value']
    else:
        prop.current_value = prop.definition.value


JSON_PROP_READERS = {
    'filepath': ReadFilepathJSON,
    'string': ReadStringJSON,
    'list': ReadListJSON,
    'integer': ReadIntegerJSON,
    'reglist': ReadReglistJSON,
    'color': ReadColorJSON,
    'float': ReadFloatJSON,
    'boolean': ReadBooleanJSON,
}


class PropertyDefinition(object):
    def __init__(self, name, prop_type=None, value=None):
        if prop_type not in JSON_PROP_READERS:
            raise TypeError
        self.read_json = JSON_PROP_READERS[prop_type]
        self.name = name
        self.prop_type = prop_type
        self.value = value
        self.node = None

        
class Property(object):
    def __init__(self, definition):
        self.definition = definition
        self.current_value = definition.value

    @property
    def name(self):
        return self.definition.name

    def ReadData(self, desc):
        self.definition.read_json(self, desc)

