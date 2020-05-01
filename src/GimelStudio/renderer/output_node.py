## ----------------------------------------------------------------------------
## Gimel Studio © 2020 Correct Syntax, Noah Rahm. All rights reserved.
##
## FILE: output_node.py
## AUTHOR(S): Noah Rahm
## PURPOSE: -
## ----------------------------------------------------------------------------

from .eval_info import EvalInfo


class OutputNode:
    """
    This class describes an image that may be output from the application.
    """
    def __init__(self):
        self.node = None

    def ReadData(self, desc, nodes):
        """
        Reads the content of the supplied json data.
        """
        try:
            node = nodes[str(desc['bind'])]
            if node.IsDisabled() != True:
                self.node = node
            else:
                self.node = None
        except KeyError:
            self.node = None

    def RenderImage(self):
        """
        This method generates an image for this output node. If the output
        node is not connected then no image will be generated.
        """
        if self.node != None:
            eval_info = EvalInfo(self.node)
            image = eval_info.node.Evaluate(eval_info)
            return image


