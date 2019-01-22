import contextlib

from m2cgen.ast.interpreters.code_generator import BaseCodeGenerator
from m2cgen.ast.interpreters.code_generator import CodeTemplate as CT


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

    def add_class_def(self, class_name):
        class_def = "class " + class_name + "(object):"
        self.add_code_line(class_def)
        self.increase_indent()

    def add_method_def(self, name, args):
        method_def = "def " + " " + name + "(self, "
        method_def += ", ".join(args)
        method_def += "):"
        self.add_code_line(method_def)
        self.increase_indent()

    @contextlib.contextmanager
    def class_definition(self, model_name):
        self.add_class_def(model_name)
        yield

    @contextlib.contextmanager
    def method_definition(self, name, args):
        self.add_method_def(name, args)
        yield
