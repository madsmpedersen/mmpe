'''
Created on 11/03/2014

@author: MMPE

This is the functions module
'''
from mmpe.ui.qt_ui import QtUI
from mmpe.ui.scripting_window.ScriptingWindow import ScriptingWindow
from mmpe.ui.scripting_window.ScriptRunner import ScriptRunner
from mmpe.ui.scripting_window.script_function import ScriptFunction
import inspect
import numpy as np




class ThirdFunction(ScriptFunction):
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

class FourthFunction(ScriptFunction):
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


