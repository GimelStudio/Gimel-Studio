from PIL import Image, ImageChops, ImageOps

from GimelStudio.api import (Color, RenderImage, List, NodeBase,
                         ParameterDefinition, PropertyDefinition,
                         RegisterNode)
 
class NodeDefinition(NodeBase):

    @property
    def NodeName(self):
        return "corenode_mix"

    @property
    def NodeLabel(self):
        return "Mix"

    @property
    def NodeCategory(self):
        return "BLEND"

    @property
    def NodeDescription(self):
        return "Blends two images together using the specified blend type." 

    @property
    def NodeVersion(self):
        return "1.0.0"  

    @property
    def NodeAuthor(self):
        return "Correct Syntax Software" 

    @property
    def NodeParameters(self):
        return [
            ParameterDefinition('Image',
                                param_type='image',
                                default_value=RenderImage('RGBA', (256, 256), (0, 0, 0, 1))),
            ParameterDefinition('Overlay',
                                param_type='image',
                                default_value=RenderImage('RGBA', (256, 256), (0, 0, 0, 1))),
        ]

    @property
    def NodeProperties(self):
        return [
            PropertyDefinition('Blend Mode',
                               prop_type='list',
                               value=List([
                                 'ADD',
                                 'ADD MODULO',
                                 'SUBTRACT',
                                 'SUBTRACT MODULO',
                                 'MULTIPLY',
                                 'SCREEN',
                                 'DIFFERENCE',
                                 'DARKER',
                                 'LIGHTER'
                                 ], 'MULTIPLY')
                               ),
        ]

    def NodePropertiesUI(self, node, ui, parent, sizer):
        self.NodePropertiesHelperInit(node, ui, parent, sizer)
        
        # Resample
        current_blend_type_value = self.NodeGetPropertyValue('Blend Mode')

        blendmodelabel = ui.StaticText(parent, label="Blend Mode:")
        sizer.Add(blendmodelabel, pos=(2, 0), flag=ui.LEFT|ui.TOP, border=10)

        self.blendmodecombobox = ui.ComboBox(parent, id=ui.ID_ANY, 
             value=current_blend_type_value, choices=[
                                 'ADD',
                                 'ADD MODULO',
                                 'SUBTRACT',
                                 'SUBTRACT MODULO',
                                 'MULTIPLY',
                                 'SCREEN',
                                 'DIFFERENCE',
                                 'DARKER',
                                 'LIGHTER'
                                 ], style=ui.CB_READONLY)
        sizer.Add(self.blendmodecombobox, pos=(2, 1), span=(1, 3), flag=ui.TOP|ui.EXPAND, border=5)

        # Bindings
        parent.Bind(ui.EVT_COMBOBOX, self.EvtChoice, self.blendmodecombobox)

    def EvtChoice(self, evt):
        value = evt.GetString()
        if not value:
            return
        self.NodePropertiesUpdate('Blend Mode', value)

    def NodeEvaluation(self, eval_info):
        image1 = eval_info.EvaluateParameter('Image')
        image2 = eval_info.EvaluateParameter('Overlay')
        blendmode = eval_info.EvaluateProperty('Blend Mode')

        image = RenderImage() 
        main_image = image1.GetImage()
        layer_image = ImageOps.fit(image2.GetImage(), main_image.size)

        if blendmode == 'ADD':
            img = ImageChops.add(main_image, layer_image)

        elif blendmode == 'ADD MODULO':
            img = ImageChops.add_modulo(main_image, layer_image)

        elif blendmode == 'SUBTRACT':
            img = ImageChops.subtract(main_image, layer_image)

        elif blendmode == 'SUBTRACT MODULO':
            img = ImageChops.subtract_modulo(main_image, layer_image)

        elif blendmode == 'MULTIPLY':
            img = ImageChops.multiply(main_image, layer_image)

        elif blendmode == 'SCREEN':
            img = ImageChops.screen(main_image, layer_image)

        elif blendmode == 'DIFFERENCE':
            img = ImageChops.difference(main_image, layer_image)
            
        elif blendmode == 'DARKER':
            img = ImageChops.darker(main_image, layer_image)

        elif blendmode == 'LIGHTER':
            img = ImageChops.lighter(main_image, layer_image)

        image.SetAsImage(img)
        self.NodeSetThumbnail(image.GetImage())
        return image


RegisterNode(NodeDefinition)