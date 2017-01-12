'''
Created on 11/03/2014

@author: MMPE

This is the functions module
'''

from mmpe.ui.scripting_window.script_function import ScriptFunction




class FirstFunction(ScriptFunction):
    def __init__(self, controller, gui, model):
        ScriptFunction.__init__(self, controller, gui, model, "My First Function")

    def run(self, x, y):
        """This function does something.

        Parameters
        ----------
        var1 : array_like
            This is a type.
        var2 : int
            This is another var.
        Long_variable_name : {'hi', 'ho'}, optional
            Choices in brackets, default first when optional.

        Returns
        -------
        describe : type
            Explanation
        """
        return x * y

class SecondFunction(ScriptFunction):
    def __init__(self, controller, gui, model):
        ScriptFunction.__init__(self, controller, gui, model, "My Second Function")

    def run(self, x, y):
        """This function does something.

        Parameters
        ----------
        var1 : array_like
            This is a type.
        var2 : int
            This is another var.
        Long_variable_name : {'hi', 'ho'}, optional
            Choices in brackets, default first when optional.

        Returns
        -------
        describe : type
            Explanation
        """
        return x * y


