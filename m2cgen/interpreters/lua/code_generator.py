from contextlib import contextmanager

from m2cgen.ast import CompOpType
from m2cgen.interpreters.code_generator import CodeTemplate, ImperativeCodeGenerator


class LuaCodeGenerator(ImperativeCodeGenerator):

    # can't use "local" due to threshold in most lua(jit) compilers
    tpl_var_declaration = CodeTemplate("")
    tpl_var_assignment = CodeTemplate("{var_name} = {value}")
    tpl_num_value = CodeTemplate("{value}")
    tpl_infix_expression = CodeTemplate("{left} {op} {right}")
    tpl_return_statement = CodeTemplate("return {value}")
    tpl_array_index_access = CodeTemplate("{array_name}[{index}]")
    tpl_if_statement = CodeTemplate("if {if_def} then")
    tpl_else_statement = CodeTemplate("else")
    tpl_block_termination = CodeTemplate("end")

    def add_function_def(self, name, args):
        func_def = f"function {name}({', '.join(args)})"
        self.add_code_line(func_def)
        self.increase_indent()

    @contextmanager
    def function_definition(self, name, args):
        self.add_function_def(name, args)
        yield
        self.add_block_termination()

    def vector_init(self, values):
        return f"{{{', '.join(values)}}}"

    def array_index_access(self, array_name, index):
        return super().array_index_access(array_name, index + 1)

    def _comp_op_overwrite(self, op):
        if op == CompOpType.NOT_EQ:
            return "~="
        else:
            return op.value
