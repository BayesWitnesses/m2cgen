import contextlib

from m2cgen.interpreters.code_generator import ImperativeCodeGenerator
from m2cgen.interpreters.code_generator import CodeTemplate as CT


class PythonCodeGenerator(ImperativeCodeGenerator):

    tpl_num_value = CT("{value}")
    tpl_infix_expression = CT("({left}) {op} ({right})")
    tpl_return_statement = CT("return {value}")
    tpl_array_index_access = CT("{array_name}[{index}]")
    tpl_if_statement = CT("if {if_def}:")
    tpl_else_statement = CT("else:")
    tpl_var_assignment = CT("{var_name} = {value}")

    tpl_var_declaration = CT("")
    tpl_block_termination = CT("")

    def add_function_def(self, name, args):
        function_def = f"def {name}({', '.join(args)}):"
        self.add_code_line(function_def)
        self.increase_indent()

    @contextlib.contextmanager
    def function_definition(self, name, args):
        self.add_function_def(name, args)
        yield

    def vector_init(self, values):
        return f"[{', '.join(values)}]"

    def add_dependency(self, dep, alias=None):
        dep_str = f"import {dep}"
        if alias:
            dep_str += f" as {alias}"
        self.prepend_code_line(dep_str)
