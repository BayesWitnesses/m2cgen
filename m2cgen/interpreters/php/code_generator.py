import contextlib

from m2cgen.ast import CompOpType
from m2cgen.interpreters.code_generator import CLikeCodeGenerator
from m2cgen.interpreters.code_generator import CodeTemplate


class PhpCodeGenerator(CLikeCodeGenerator):

    tpl_array_index_access = CodeTemplate("$$${array_name}[${index}]")

    def __init__(self, *args, **kwargs):
        super(PhpCodeGenerator, self).__init__(*args, **kwargs)

    def add_function_def(self, name, args):
        function_def = "function " + name + "("
        function_def += ", ".join([
            ("array " if is_vector else "") + "$" + n
            for is_vector, n in args])
        function_def += ") {"
        self.add_code_line(function_def)
        self.increase_indent()

    @contextlib.contextmanager
    def function_definition(self, name, args):
        self.add_function_def(name, args)
        yield
        self.add_block_termination()

    def get_var_name(self):
        return "$" + super().get_var_name()

    def add_var_declaration(self, size):
        var_name = self.get_var_name()
        self.add_var_assignment(
            var_name=var_name,
            value="array()" if size > 1 else "null",
            value_size=size)
        return var_name

    def vector_init(self, values):
        return "array(" + ", ".join(values) + ")"

    def _comp_op_overwrite(self, op):
        if op == CompOpType.EQ:
            return "==="
        elif op == CompOpType.NOT_EQ:
            return "!=="
        else:
            return op.value
