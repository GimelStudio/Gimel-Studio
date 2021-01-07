# ----------------------------------------------------------------------------
# Gimel Studio Copyright 2019-2020 by Noah Rahm and contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# FILE: node_importer.py
# AUTHOR(S): Noah Rahm
# PURPOSE: Imports the core and custom nodes so that they are registered
# ----------------------------------------------------------------------------

import os

# First, we import the custom nodes
# directly from the corenode directory.
from GimelStudio.corenodes.output import output_node
from GimelStudio.corenodes.input import (image_node,
                                         color_image_node,
                                         noise_image_node,
                                         gradient_image_node)
from GimelStudio.corenodes.mask import edge_detect_node
# from GimelStudio.corenodes.draw import text_node
# from GimelStudio.corenodes import glsl
from GimelStudio.corenodes.color import (color_balance_node,
                                         contrast,
                                         brightness,
                                         exposure,
                                         invert_alpha_node,
                                         get_channel)
from GimelStudio.corenodes.blend import (mix_node,
                                         composite_node,
                                         alpha_composite_node)
from GimelStudio.corenodes.distort import flip_node
from GimelStudio.corenodes.filter import (blur_node,
                                          opacity,
                                          sharpness,
                                          gaussian_blur,
                                          effect_spread_node,
                                          invert_node,
                                          dilate_erode_node)
from GimelStudio.corenodes.convert import (to_normal_map_node,
                                           to_bump_map_node,
                                           to_roughness_map_node,
                                           to_specular_map_node,
                                           to_ao_map_node)

print("[INFO] Registered core nodes")

# Next, we load the custom nodes
# from the 'customnodes' directory.
try:
    paths = os.listdir("customnodes")
    for path in paths:
        name, ext = os.path.splitext(path)
        if ext != ".py":
            continue
        node_module = __import__("customnodes", fromlist=[name])

    print("[INFO] Registered custom node scripts")
except Exception as error:
    print("[WARNING] Error registering custom nodes: \n", error)
finally:
    pass
