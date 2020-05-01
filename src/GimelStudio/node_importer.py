## ----------------------------------------------------------------------------
## Gimel Studio © 2020 Correct Syntax, Noah Rahm. All rights reserved.
##
## FILE: node_importer.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Imports all the nodes so that they are registered
## ----------------------------------------------------------------------------


from GimelStudio.corenodes.input import (image_node,
                                         #asset_node,
                                         gradient_image_node,
                                         )
from GimelStudio.corenodes.convert import (normal_map_node,
                                           )
from GimelStudio.corenodes.color import (color_balance_node,
                                         contrast_node,
                                         brightness_node,
                                         invert_alpha_node,
                                         )
from GimelStudio.corenodes.blend import (mix_node,
                                         alpha_composite_node,
                                         )
from GimelStudio.corenodes.distort import (resize_node,
                                           rotate_node,
                                           )
from GimelStudio.corenodes.filter import (blur_node,
                                          sharpness_node,
                                          )
from GimelStudio.corenodes.value import (integer_node,
                                         color_node,
                                         )
from GimelStudio.corenodes.output import (output_node,
                                          )                                      
print('INFO: INITILIZED & LOADED CORE NODES')

try:
    from customnodes import *
    print('INFO: INITILIZED & LOADED CUSTOM NODES')
except Exception as error:
    print('WARNING: ERROR LOADING CUSTOM NODES (', error, ')')
finally:
    pass
