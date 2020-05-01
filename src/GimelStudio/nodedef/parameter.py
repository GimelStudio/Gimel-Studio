## ----------------------------------------------------------------------------
## Gimel Studio © 2020 Correct Syntax, Noah Rahm. All rights reserved.
##
## FILE: parameter.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the node parameter classes and readers
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
