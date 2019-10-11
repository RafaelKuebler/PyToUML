import ast
import logging
from typing import List

from decorators import log_exception
from desc import ClassDesc, FuncDesc


class ClassVisitor(ast.NodeVisitor):
    def __init__(self):
        self.classes = []

    @log_exception
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        logging.debug(f"Found class def {node.name}")
        class_desc = ClassDesc()
        class_desc.name = node.name
        docstring = ast.get_docstring(node)
        class_desc.docstring = "" if docstring is None else docstring

        for base in node.bases:
            if isinstance(base, ast.Attribute):
                class_desc.bases.append(base.attr)
            elif isinstance(base, ast.Name):
                class_desc.bases.append(base.id)

        self.classes.append(class_desc)

        for field in node.body:
            if isinstance(field, ast.FunctionDef):
                self.process_class_function(class_desc, field)

    @staticmethod
    @log_exception
    def process_class_function(class_desc: ClassDesc, node: ast.FunctionDef) -> None:
        logging.debug(f"Found function def {node.name}")
        fun_desc = FuncDesc()
        fun_desc.name = node.name
        for arg in node.args.args:
            fun_desc.args.append(arg.arg)

        function_analyzer = FunctionVisitor(class_desc)
        function_analyzer.visit(node)
            
        class_desc.functions.append(fun_desc)


class FunctionVisitor(ast.NodeVisitor):
    def __init__(self, class_desc):
        self.class_desc = class_desc

    @log_exception
    def visit_Assign(self, node: ast.ClassDef) -> None:
        for attr in node.targets:
            if not isinstance(attr, ast.Attribute):
                continue
            if not isinstance(attr.value, ast.Name):
                continue
            is_class_var = attr.value.id == "self"
            already_known = attr.attr in self.class_desc.vars
            if is_class_var and not already_known:
                logging.debug(f"Found class var {attr.attr}")
                self.class_desc.vars.append(attr.attr)

    @log_exception
    def visit_AnnAssign(self, node: ast.ClassDef) -> None:
        # TODO: save type hint!
        if not isinstance(node.target, ast.Attribute):
            return
        is_class_var = node.target.value.id == "self"
        already_known = node.target.attr in self.class_desc.vars
        if is_class_var and not already_known:
            logging.debug(f"Found class var {node.target.attr}")
            self.class_desc.vars.append(node.target.attr)


def analyze_py_file(py_file_path: str) -> List[ClassDesc]:
    with open(py_file_path, "r") as source:
        tree = ast.parse(source.read())
    analyzer = ClassVisitor()
    analyzer.visit(tree)

    return analyzer.classes
