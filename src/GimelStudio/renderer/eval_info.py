## ----------------------------------------------------------------------------
## Gimel Studio © 2020 Correct Syntax, Noah Rahm. All rights reserved.
##
## FILE: eval_info.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Supply an evaluation function for computing a node's value
## ----------------------------------------------------------------------------


class EvalInfo(object):
    """
    Evaluate node properties and parameters
    """
    def __init__(self, node):
        if node == None:
            raise TypeError
        self.node = node

    def EvaluateParameter(self, name):
        """
        Evaluates the value of a parameter.
        """
        p = self.node._parameters[name]
        if p.binding:
            # Make sure the next node is not disabled
            if p.binding.IsDisabled() != True:
                # Evaluate the next node
                info = EvalInfo(p.binding)
                return p.binding.Evaluate(info)
        return p.current_value


    def EvaluateProperty(self, name):
        """
        Evaluates the value of a property.
        """
        p = self.node._properties[name]
        return p.current_value
