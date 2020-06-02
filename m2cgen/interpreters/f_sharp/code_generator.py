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
        self.add_code_line("if ({}) then".format(if_def))
        self.increase_indent()

    def add_else_statement(self):
        self.decrease_indent()
        self.add_code_line("else")
        self.increase_indent()

    def add_if_termination(self):
        self.decrease_indent()

    def get_func_name(self):
        func_name = "func" + str(self._func_idx)
        self._func_idx += 1
        return func_name

    def add_function(self, function_name, function_body):
        self.add_code_line("let {} =".format(function_name))
        self.increase_indent()
        self.add_code_lines(function_body)
        self.decrease_indent()

    def function_invocation(self, function_name, *args):
        return (function_name + " " +
                " ".join(map(lambda x: "({})".format(x), args)))

    def add_function_def(self, name, args):
        function_def = "let {} ".format(name)
        function_def += " ".join(
            ["({0} : double{1})".format(n, " list" if is_vector else "")
             for is_vector, n in args])
        function_def += " ="
        self.add_code_line(function_def)
        self.increase_indent()

    @contextlib.contextmanager
    def function_definition(self, name, args):
        self.add_function_def(name, args)
        yield
        self.decrease_indent()

    def vector_init(self, values):
        return "[" + "; ".join(values) + "]"

    def _comp_op_overwrite(self, op):
        if op == CompOpType.EQ:
            return "="
        elif op == CompOpType.NOT_EQ:
            return "<>"
        else:
            return op.value
