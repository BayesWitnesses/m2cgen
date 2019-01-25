import contextlib

from m2cgen.interpreters.code_generator import BaseCodeGenerator
from m2cgen.interpreters.code_generator import CodeTemplate as CT


class PythonCodeGenerator(BaseCodeGenerator):

    tpl_num_value = CT("${value}")
    tpl_infix_expression = CT("(${left}) ${op} (${right})")
    tpl_return_statement = CT("return ${value}")
    tpl_array_index_access = CT("${array_name}[${index}]")
    tpl_if_statement = CT("if ${if_def}:")
    tpl_else_statement = CT("else:")
    tpl_var_assignment = CT("${var_name} = ${value}")

    tpl_var_declaration = CT("")
    tpl_block_termination = CT("")

    def add_function_def(self, name, args):
        method_def = "def " + " " + name + "("
        method_def += ", ".join(args)
        method_def += "):"
        self.add_code_line(method_def)
        self.increase_indent()

    @contextlib.contextmanager
    def function_definition(self, name, args):
        self.add_function_def(name, args)
        yield
