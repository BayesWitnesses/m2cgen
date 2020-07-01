import contextlib

from m2cgen.ast import CompOpType
from m2cgen.interpreters.code_generator import CLikeCodeGenerator
from m2cgen.interpreters.code_generator import CodeTemplate as CT


class PowershellCodeGenerator(CLikeCodeGenerator):

    tpl_var_declare = CT("{var_type}{var_name} = {init_val}")
    tpl_var_assignment = CT("{var_name} = {value}")
    tpl_array_index_access = CT("${array_name}[{index}]")
    tpl_return_statement = CT("return {value}")

    scalar_type = "[double]"
    vector_type = "[double[]]"

    operator_map = {CompOpType.EQ: "-eq", CompOpType.NOT_EQ: "-ne",
                    CompOpType.GTE: "-ge", CompOpType.LTE: "-le",
                    CompOpType.GT: "-gt", CompOpType.LT: "-lt"}

    def add_function_def(self, name, args, is_scalar_output):
        func_args = ", ".join([
            f"{self._get_var_type(is_vector)} ${n}"
            for is_vector, n in args])
        function_def = f"function {name}({func_args}) {{"
        self.add_code_line(function_def)
        self.increase_indent()

    @contextlib.contextmanager
    def function_definition(self, name, args, is_scalar_output):
        self.add_function_def(name, args, is_scalar_output)
        yield
        self.add_block_termination()

    def function_invocation(self, function_name, *args):
        functions_args = " ".join(map(lambda x: f"$({x})", args))
        return f"{function_name} {functions_args}"

    def math_function_invocation(self, function_name, *args):
        return f"{function_name}({', '.join(map(str, args))})"

    def get_var_name(self):
        return f"${super().get_var_name()}"

    def add_var_declaration(self, size):
        var_name = self.get_var_name()
        self.add_code_line(
            self.tpl_var_declare(var_type=self._get_var_type(size > 1),
                                 var_name=var_name,
                                 init_val="@(0.0)" if size > 1 else "0.0"))
        return var_name

    def vector_init(self, values):
        vals = ", ".join(map(lambda x: f"$({x})", values))
        return f"@({vals})"

    def _get_var_type(self, is_vector):
        return self.vector_type if is_vector else self.scalar_type

    def _comp_op_overwrite(self, op):
        return self.operator_map[op]
