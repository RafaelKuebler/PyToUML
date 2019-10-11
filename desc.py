from typing import List


class FuncDesc:
    def __init__(self, name: str = "", args: List[str] = None, returns: str = ""):
        self.name = name
        self.args = [] if args is None else args
        self.returns = returns


class ClassDesc:
    def __init__(self):
        self.name: str = ""
        self.docstring: str = ""
        self.bases: List[str] = []
        self.vars: List[str] = []
        self.functions: List[FuncDesc] = []
        self.dependencies: List[str] = []
