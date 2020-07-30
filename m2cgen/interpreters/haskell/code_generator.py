import contextlib

from m2cgen.ast import CompOpType
from m2cgen.interpreters.code_generator \
    import FunctionalCodeGenerator, CodeTemplate


class HaskellCodeGenerator(FunctionalCodeGenerator):
    tpl_function_signature = CodeTemplate("{function_name} =")
    tpl_if_statement = CodeTemplate("if ({if_def}) then")
    tpl_else_statement = CodeTemplate("else")
    tpl_num_value = CodeTemplate("{value}")
    tpl_infix_expression = CodeTemplate("({left}) {op} ({right})")
    tpl_module_definition = CodeTemplate("module {module_name} where")

    def array_index_access(self, array_name, index):
        return self.tpl_infix_expression(
            left=array_name, op="!!", right=index)

    def add_if_termination(self):
        self.decrease_indent()

    def add_function_def(self, name, args, is_scalar_output):
        types = " -> ".join(
            ["[Double]" if is_vector else "Double"
             for is_vector, _ in [*args, (not is_scalar_output, None)]])
        signature = f"{name} :: {types}"
        self.add_code_line(signature)

        func_args = " ".join([n for _, n in args])
        function_def = f"{name} {func_args} ="
        self.add_code_line(function_def)

        self.increase_indent()

    @contextlib.contextmanager
    def function_definition(self, name, args, is_scalar_output):
        self.add_function_def(name, args, is_scalar_output)
        yield
        self.decrease_indent()

    def vector_init(self, values):
        return f"[{', '.join(values)}]"

    def _comp_op_overwrite(self, op):
        if op == CompOpType.NOT_EQ:
            return "/="
        else:
            return op.value
