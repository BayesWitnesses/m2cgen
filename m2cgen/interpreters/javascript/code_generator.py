from contextlib import contextmanager

from m2cgen.ast import CompOpType
from m2cgen.interpreters.code_generator import CLikeCodeGenerator


class JavascriptCodeGenerator(CLikeCodeGenerator):

    def add_function_def(self, name, args):
        function_def = f"function {name}({', '.join(args)}) {{"
        self.add_code_line(function_def)
        self.increase_indent()

    @contextmanager
    def function_definition(self, name, args):
        self.add_function_def(name, args)
        yield
        self.add_block_termination()

    def vector_init(self, values):
        return f"[{', '.join(values)}]"

    def _get_var_declare_type(self, is_vector):
        return "var"

    def _comp_op_overwrite(self, op):
        if op == CompOpType.EQ:
            return "==="
        elif op == CompOpType.NOT_EQ:
            return "!=="
        else:
            return op.value
