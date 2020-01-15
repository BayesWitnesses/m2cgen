import contextlib

from m2cgen.interpreters.code_generator import CLikeCodeGenerator
from m2cgen.interpreters.code_generator import CodeTemplate


class RCodeGenerator(CLikeCodeGenerator):

    tpl_return_statement = CodeTemplate("return(${value})")
    tpl_var_assignment = CodeTemplate("${var_name} <- ${value}")

    def __init__(self, *args, **kwargs):
        super(RCodeGenerator, self).__init__(*args, **kwargs)

    def add_var_declaration(self, size):
        return self.get_var_name()

    def add_function_def(self, name, args):
        function_def = name + " <- function("
        function_def += ",".join([arg for _, arg in args])
        function_def += ") {"
        self.add_code_line(function_def)
        self.increase_indent()

    @contextlib.contextmanager
    def function_definition(self, name, args, is_vector_output):
        self.add_function_def(name, args)
        yield
        self.add_block_termination()

    def array_index_access(self, array_name, index):
        return super().array_index_access(array_name, index + 1)

    def vector_init(self, values):
        return "c(" + ", ".join(values) + ")"
