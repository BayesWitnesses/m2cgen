from contextlib import contextmanager

from m2cgen.interpreters.code_generator import CodeTemplate, ImperativeCodeGenerator


class PythonCodeGenerator(ImperativeCodeGenerator):

    tpl_num_value = CodeTemplate("{value}")
    tpl_infix_expression = CodeTemplate("{left} {op} {right}")
    tpl_return_statement = CodeTemplate("return {value}")
    tpl_array_index_access = CodeTemplate("{array_name}[{index}]")
    tpl_if_statement = CodeTemplate("if {if_def}:")
    tpl_else_statement = CodeTemplate("else:")
    tpl_var_assignment = CodeTemplate("{var_name} = {value}")

    tpl_var_declaration = CodeTemplate("")
    tpl_block_termination = CodeTemplate("")

    def add_function_def(self, name, args):
        function_def = f"def {name}({', '.join(args)}):"
        self.add_code_line(function_def)
        self.increase_indent()

    @contextmanager
    def function_definition(self, name, args):
        self.add_function_def(name, args)
        yield

    def vector_init(self, values):
        return f"[{', '.join(values)}]"

    def add_dependency(self, dep):
        self.prepend_code_line(f"import {dep}")
