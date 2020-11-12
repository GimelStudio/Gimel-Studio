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
## FILE: node_importer.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Imports the core and custom nodes so that they are registered
## ----------------------------------------------------------------------------


from GimelStudio.corenodes.input import (image_node, color_image_node,
                                        noise_image_node, gradient_image_node)
#from GimelStudio.corenodes.mask import  # add nodes here
#from GimelStudio.corenodes.draw import text_node
from GimelStudio.corenodes.color import (color_balance_node, contrast_node,
                                        brightness_node, invert_alpha_node,
                                        get_channel_node)
from GimelStudio.corenodes.blend import (mix_node, composite_node,
                                        alpha_composite_node)
from GimelStudio.corenodes.distort import flip_node #resize_node, rotate_node
from GimelStudio.corenodes.filter import (blur_node, opacity_node,
                                         sharpness_node, effect_spread_node,
                                         invert_node)
from GimelStudio.corenodes.convert import (to_normal_map_node, to_bump_map_node,
                                           to_roughness_map_node,
                                           to_specular_map_node, to_ao_map_node)
from GimelStudio.corenodes.output import output_node


print('INFO: INITILIZED & LOADED CORE NODES')
try:
    from customnodes import *
    print('INFO: INITILIZED & LOADED CUSTOM NODES')
except Exception as error:
    print('WARNING: ERROR LOADING CUSTOM NODES (', error, ')')
finally:
    pass
