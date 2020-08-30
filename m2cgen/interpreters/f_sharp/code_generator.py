import contextlib

from m2cgen.ast import CompOpType
from m2cgen.interpreters.code_generator \
    import FunctionalCodeGenerator, CodeTemplate


class FSharpCodeGenerator(FunctionalCodeGenerator):
    tpl_function_signature = CodeTemplate("let {function_name} =")
    tpl_if_statement = CodeTemplate("if ({if_def}) then")
    tpl_else_statement = CodeTemplate("else")
    tpl_num_value = CodeTemplate("{value}")
    tpl_infix_expression = CodeTemplate("({left}) {op} ({right})")
    tpl_array_index_access = CodeTemplate("{array_name}.[{index}]")

    def add_if_termination(self):
        self.decrease_indent()

    def add_function_def(self, name, args):
        func_args = " ".join(
            [f"({n} : double{' list' if is_vector else ''})"
             for is_vector, n in args])
        function_def = f"let {name} {func_args} ="
        self.add_code_line(function_def)
        self.increase_indent()

    @contextlib.contextmanager
    def function_definition(self, name, args):
        self.add_function_def(name, args)
        yield
        self.decrease_indent()

    def vector_init(self, values):
        return f"[{'; '.join(values)}]"

    def _comp_op_overwrite(self, op):
        if op == CompOpType.EQ:
            return "="
        elif op == CompOpType.NOT_EQ:
            return "<>"
        else:
            return op.value
