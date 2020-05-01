## ----------------------------------------------------------------------------
## Gimel Studio © 2020 Correct Syntax, Noah Rahm. All rights reserved.
##
## FILE: property.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the node property classes and readers
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

