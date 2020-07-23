import contextlib

from m2cgen.ast import CompOpType
from m2cgen.interpreters.code_generator import BaseCodeGenerator, CodeTemplate


class FSharpCodeGenerator(BaseCodeGenerator):
    tpl_num_value = CodeTemplate("{value}")
    tpl_infix_expression = CodeTemplate("({left}) {op} ({right})")
    tpl_array_index_access = CodeTemplate("{array_name}.[{index}]")

    def reset_state(self):
        super().reset_state()
        self._func_idx = 0

    def add_if_statement(self, if_def):
        self.add_code_line(f"if ({if_def}) then")
        self.increase_indent()

    def add_else_statement(self):
        self.decrease_indent()
        self.add_code_line("else")
        self.increase_indent()

    def add_if_termination(self):
        self.decrease_indent()

    def get_func_name(self):
        func_name = f"func{self._func_idx}"
        self._func_idx += 1
        return func_name

    def add_function(self, function_name, function_body):
        self.add_code_line(f"let {function_name} =")
        self.increase_indent()
        self.add_code_lines(function_body)
        self.decrease_indent()

    def function_invocation(self, function_name, *args):
        function_args = " ".join(map(lambda x: f"({x})", args))
        return f"{function_name} {function_args}"

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
