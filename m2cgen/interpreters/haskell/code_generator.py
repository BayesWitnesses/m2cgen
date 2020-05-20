import contextlib

from m2cgen.ast import CompOpType
from m2cgen.interpreters.code_generator import BaseCodeGenerator, CodeTemplate


class HaskellCodeGenerator(BaseCodeGenerator):
    tpl_num_value = CodeTemplate("{value}")
    tpl_infix_expression = CodeTemplate("({left}) {op} ({right})")
    tpl_module_definition = CodeTemplate("module {module_name} where")

    def __init__(self, *args, **kwargs):
        self._func_idx = 0
        super().__init__(*args, **kwargs)

    def reset_state(self):
        super().reset_state()
        self._func_idx = 0

    def array_index_access(self, array_name, index):
        return self.tpl_infix_expression(
            left=array_name, op="!!", right=index)

    def add_if_statement(self, if_def):
        self.add_code_line("if ({})".format(if_def))
        self.increase_indent()
        self.add_code_line("then")
        self.increase_indent()

    def add_else_statement(self):
        self.decrease_indent()
        self.add_code_line("else")
        self.increase_indent()

    def add_if_termination(self):
        self.decrease_indent()
        self.decrease_indent()

    def get_func_name(self):
        func_name = "func" + str(self._func_idx)
        self._func_idx += 1
        return func_name

    def add_function(self, function_name, function_body):
        self.add_code_line("{} =".format(function_name))
        self.increase_indent()
        self.add_code_lines(function_body)
        self.decrease_indent()

    def function_invocation(self, function_name, *args):
        return (function_name + " " +
                " ".join(map(lambda x: "({})".format(x), args)))

    def add_function_def(self, name, args, is_scalar_output):
        signature = name + " :: "
        signature += " -> ".join(
            ["[Double]" if is_vector else "Double"
             for is_vector, _ in [*args, (not is_scalar_output, None)]])
        self.add_code_line(signature)

        function_def = name + " "
        function_def += " ".join([n for _, n in args])
        function_def += " ="
        self.add_code_line(function_def)

        self.increase_indent()

    @contextlib.contextmanager
    def function_definition(self, name, args, is_scalar_output):
        self.add_function_def(name, args, is_scalar_output)
        yield
        self.decrease_indent()

    def vector_init(self, values):
        return "[" + ", ".join(values) + "]"

    def _comp_op_overwrite(self, op):
        if op == CompOpType.NOT_EQ:
            return "/="
        else:
            return op.value
