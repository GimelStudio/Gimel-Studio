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
