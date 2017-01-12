'''
Created on 17/03/2014

@author: MMPE
'''
from mmpe.ui.scripting_window.controller import ScriptingWindowController
import os
from mmpe.functions.process_exec import pexec
import sys
from mmpe.functions import process_exec
from mmpe.ui.scripting_window import script_function
import re
from mmpe.functions import argument_string

import numpy as np


import shutil
import os
from mmpe.functions.deep_coding import to_str


def copy_doc(doc_path):
    #shutil.rmtree(dst_path, ignore_errors=True)
    shutil.copytree(os.path.join(doc_path, 'templates/_static'), os.path.join(doc_path, '_static/'))

    shutil.copy2(os.path.join(doc_path, 'sphinx/_build/html/ScriptFunctions.html'), doc_path)
    shutil.copytree(os.path.join(doc_path, 'sphinx/_build/html/_modules'), os.path.join(doc_path, '_modules'))
    template = os.path.join(doc_path, "templates/template.html")
    shutil.copy2(template, os.path.join(doc_path, "doc.html"))
    shutil.copy2(template, os.path.join(doc_path, "source.html"))
    shutil.copy2(template, os.path.join(doc_path, "index.html"))


def make_doc(doc_path, appfunc_path):
    for folder in ['_modules', '_static', '_sources']:
        shutil.rmtree(os.path.join(doc_path, folder), ignore_errors=True)

    appfunc_lst = script_function.script_function_class_list(appfunc_path)

    with open(doc_path + 'ui.scripting_window.rst', 'w') as fid:
        header = "Scripting_window Package"
        fid.write('%s\n%s\n\n' % (header, "="*len(header)))
        for module in set([appfunc.__module__ for appfunc in appfunc_lst]):
            s = ':mod:`%s` Module' % module.split(".")[-1]  #somefunctions
            fid.write('%s\n%s\n\n' % (s, "-"*len(s)))
            fid.write('.. automodule:: %s\n' % module)  #ui.scripting_window.appfuncs.somefunctions
            fid.write("""    :members:
    :undoc-members:
    :show-inheritance:\n\n""")
#

    sphinx_path = os.path.join(doc_path, "sphinx")
    errorcode, stdout, stderr, _ = pexec(["make.bat", "html"], sphinx_path)
    print (stdout)
    sys.stderr.write(stderr)
    sys.stderr.flush()

    if errorcode == 0:
        copy_doc(doc_path)

        lst = script_function.script_function_class_list(appfunc_path)
        with open(doc_path + "scriptfunctions.html") as fid:
            doc_html_src = to_str(fid.read())

        for appfunc in lst:

            module = appfunc.__module__
            name = appfunc.__name__
            arguments = argument_string(appfunc.run)

        abc_lst = sorted(set([appfunc.__name__[0].upper() for appfunc in lst]))
        index_html = '<h1 id="index">Index</h1>'
        index_html += '<div class="genindex-jumpbox">\n'
        index_html += "\n|".join(['<a href="#%s"><strong>%s</strong></a>' % (abc, abc) for abc in abc_lst])
        index_html += '\n</div>\n\n'
        for abc in abc_lst:
            index_html += '<h2 id="%s">%s</h2>\n' % (abc, abc)
            index_html += '<table style="width: 100%" class="indextable genindextable"><tr>\n'
            for appfunc in [appfunc for appfunc in lst if appfunc.__name__[0].upper() == abc]:
                module = appfunc.__module__.replace(appfunc_path.replace("/", ".") + ".", "")
                name = appfunc.__name__
                arguments = argument_string(appfunc.run)
                index_html += '\n<tr><td style="width: 33%" valign="top"><dl>'

                index_html += '<dt><a href="doc.html#%s"><tt class="descclassname">%s.</tt><tt class="descname"><big>%s</big>' % (appfunc, module, name)
                index_html += arguments.replace("(", '<big>(</big><em>').replace(',', '</em>, <em>').replace(')', '</em><big>)</big>')
                index_html += '</tt></a></dt></dl></td>'
                index_html += '</tr>'

                start_tag = '<dt id="appfuncs.%s.%s.run">' % (module, name)
                end_tag = '</dd>'

                #scriptFunction_name = url_fragment.split(".")[-2]
                method_html = start_tag + doc_html_src.split(start_tag)[1].split(end_tag)[0]  #+ end_tag
                at = "&#64;"
                for a, b in [('<tt class="descname">run</tt>', '<tt class="descname">%s</tt>' % name),
                    ('href="_modules', 'href="source.html?#_modules'),
                    ('href="#appfuncs', 'href="appfuncs.html?#appfuncs'),
                    #('</th>', '</th></tr>\n<tr>'),
                    ("Parameters :", "Parameters:"),
                    ("Return :", "Return:"),

                    ]:
                    method_html = method_html.replace(a, b)

                for a, b in [
                    ('attribute', "<a href='Attributes.html'>attribute</a>"),
                    ('dataset', "<a href='Datasets.html'>dataset</a>"),
                    ('model', "<a href='model.html'>model</a>"),
                    ('selection', "<a href='Selection.html'>selection</a>"),
                    ('dataItemList', "<a href='DataItemList.html'>dataItemList</a>"),
                    ('dataitem', "<a title='Dataset, attribute or attributegroup'>dataitem</a>"),
                    ('basis attribute', "<a title='The Time-attribute, if it exists, otherwise the Index-attribute'>basis attribute</a>"),
                    ('cell', "<a href='Cell.html'>cell</a>"),
                    ('tab', "<a href='Tabs.html'>tab</a>"),
                    ]:
                    for a_ in [a + 's', a[0].upper() + a[1:] + 's', a, a[0].upper() + a[1:]]:
                        method_html = method_html.replace(at + a_, b.replace(a, a_))

                link_pattern = re.compile(at + "(\w+)\W")
                missing = re.findall(link_pattern, method_html)


                if missing:
                    raise Exception("@%s found in %s.%s not implemented" % (missing[0], module, name))

                appfuncs_html += method_html

            index_html += '</table>'

        with open(os.path.join(doc_path, 'index.html'), 'r') as fid:
            html = fid.read()
        with open(os.path.join(doc_path, 'index.html'), 'w') as fid:
            fid.write(html.replace("#Contents", index_html))

        with open(os.path.join(doc_path, 'doc.html'), 'r') as fid:
            html = fid.read()
        with open(os.path.join(doc_path, 'appfuncs.html'), 'w') as fid:
            fid.write(to_str(html.replace("#Contents", appfuncs_html.replace(".run", ""))))

#        pattern = 'class="descclassname">[^<]+<'  #</tt><tt class="descname">MyFirstFunction</tt><big>(</big>'
#        print re.findall(pattern, docs)
        #print re.findall('<tt class="descclassname">ui.scripting_window.appfuncs.somefunctions.</tt><tt class="descname">MyFirstFunction</tt><big>(</big>', docs)


if __name__ == "__main__":
    make_doc("mmpe/ui/scripting_window/docs/", 'mmpe/ui/scripting_window/appfuncs')
    controller = ScriptingWindowController()
