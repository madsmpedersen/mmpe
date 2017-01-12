import imp
import inspect
import re
import sys
import types

from mmpe.functions.inspect_ext import argument_string
from mmpe.ui.scripting_window.script_function import ScriptFunction


if sys.version_info[0] >= 3:
    basestring = str



class ScriptRunner(object):
    def __init__(self, controller, gui, model):
        self.controller = controller
        self.model = model
        self.gui = gui
        if hasattr(self.controller, 'appFuncs'):
            for func in self.controller.appFuncs:
                setattr(self, func.class_name, func)
                globals()[func.class_name] = func
        globals()['model'] = model
        globals()['gui'] = gui
        self.last = None
        self.seq_runner_modules = {}






    def get_globals(self):
        return {k:v for (k, v) in  globals().items() if not k.startswith("__")}


    def get_seq_runner(self, f, init, fini, seq):
        def func_source(f, indent=0):
            if f is None:
                return ""
            else:
                re_def = re.compile(" *def +%s\(" % f.__name__)
                for start, line in enumerate(self.script_lines):
                    if re_def.match(line):
                        def_indent = line.index("def")
                        re_indent = re.compile(" {%d}[a-zA-Z_]" % def_indent)
                        for end, line in enumerate(self.script_lines[start + 1:], start + 1):
                            if re_indent.match(line):
                                break
                        break
                return "\n".join([" "*indent + l[def_indent:] for l in self.script_lines[start:end]]).rstrip()

        fname = f.__name__


        def func_body_source(f, indent):
            if f is None:
                return ""
            else:
                f_source = func_source(f, indent - 4)
                return f_source[f_source.index("\n") + 1:]

        fcode = """
from PdapDaemon import PdapDaemon

def seq_runner((id, seq, pdap)):
    # setup
    if pdap is None:
        pdap = PdapDaemon()
    globals().update(pdap.scriptRunner.get_globals())
    # init
%s

    #execute function
%s
    result = map(%s, seq)

    # fini
%s
    return id, result
if __name__=="__main__":
    seq_runner((0,%s,None))
""" % (func_body_source(init, 4), func_source(f, 4), fname, func_body_source(fini, 4), seq)


        with open("tmp_%s.py" % fname, 'w') as fid:
            fid.writelines(fcode)
        if fname not in self.seq_runner_modules:
            self.seq_runner_modules[fname] = __import__("tmp_%s" % fname)
        else:
            self.seq_runner_modules[fname] = imp.reload(self.seq_runner_modules[fname])
        return getattr(self.seq_runner_modules[fname], "seq_runner")






    def run(self, script_code):
        self.script_code = script_code
        self.script_lines = script_code.replace("\t", "    ").split("\n")
        pre_run_globals = globals().copy()


        exec(script_code)

        globals().clear()
        globals().update(pre_run_globals)

    def split_line(self, line):
        txt = line.strip()
        for c in " ();":
            txt = txt.split(c)[-1]

        parent = ".".join(txt.split(".")[:-1])

        residual = txt.split(".")[-1]
        return parent, residual

    def get_function_dict(self, parent, residual):
        dir_dict = {}
        if parent == "":
            for d in [{'self': self}, globals(), __builtins__]:
                dir_dict.update(d)
        else:
            try:
                parent_obj = eval(parent)
                if inspect.isclass(parent_obj):
                    parent_cls = parent_obj
                else:
                    if hasattr(parent_obj, '__dict__'):
                        dir_dict.update(vars(parent_obj))
                    parent_cls = parent_obj.__class__
                for d in [vars(obj) for obj in inspect.getmro(parent_cls)]:
                    dir_dict.update(d)
            except (NameError, AttributeError, SyntaxError):
                parent_obj = None


        object_dict = {k:v for k, v in dir_dict.items() if k.lower().startswith(residual.lower())}
        func_dict = {}
        for name, obj in object_dict.items():
            if isinstance(obj, ScriptFunction):
                obj = obj.run
                if obj.__name__ == "new_f":
                    obj = obj.f  # model changer decorator
            if inspect.isclass(obj):
                obj = obj.__init__

            if isinstance(obj, (types.FunctionType, types.MethodType)):
                func_dict[name] = obj
        return func_dict



    def get_autocomplete_list(self, line):
        parent, residual = self.split_line(line)
        if parent == self.last and self.last != '':
            return None
        else:
            self.last = parent
            return [(syntax + argument_string(func)) for syntax, func in self.get_function_dict(parent, residual).items()]
