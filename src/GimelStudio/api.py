## ----------------------------------------------------------------------------
## Gimel Studio © 2020 Correct Syntax, Noah Rahm. All rights reserved.
##
## FILE: api.py (API entry-point)
## AUTHOR(S): Noah Rahm
## PURPOSE: The entry-point for the Gimel Studio nodes API
## ----------------------------------------------------------------------------


# Only these parts of Gimel Studio should be
# directly accessed by the api users

from GimelStudio.meta import (__NAME__, __AUTHOR__, __VERSION__,
                              __BUILD__, __RELEASE__, __DEBUG__,
                              __TITLE__)


from GimelStudio.utils import (ConvertImageToWx, ArrayFromImage,
                               ArrayToImage, Color, RenderImage,
                               List, DrawGrid)

from GimelStudio.nodedef import (NodeBase, ParameterDefinition,
                                 PropertyDefinition, RegisterNode,
                                 UnregisterNode)
