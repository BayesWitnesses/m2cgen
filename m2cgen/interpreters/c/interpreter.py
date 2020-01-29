import os

from m2cgen import ast
from m2cgen.interpreters import utils, mixins
from m2cgen.interpreters.c.code_generator import CCodeGenerator
from m2cgen.interpreters.interpreter import ToCodeInterpreter


class CInterpreter(ToCodeInterpreter,
                   mixins.LinearAlgebraMixin):

    supported_bin_vector_ops = {
        ast.BinNumOpType.ADD: "add_vectors",
    }

    supported_bin_vector_num_ops = {
        ast.BinNumOpType.MUL: "mul_vector_number",
    }

    exponent_function_name = "exp"
    power_function_name = "pow"
    tanh_function_name = "tanh"

    def __init__(self, indent=4, *args, **kwargs):
        cg = CCodeGenerator(indent=indent)
        super(CInterpreter, self).__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        self._cg.reset_state()
        self._reset_reused_expr_cache()

        args = [(True, self._feature_array_name)]

        # C doesn't allow returning vectors, so if model returns vector we will
        # have additional vector argument which we will populate at the end.
        if expr.output_size > 1:
            args += [(True, "output")]

        with self._cg.function_definition(
                name="score",
                args=args,
                is_scalar_output=expr.output_size == 1):

            last_result = self._do_interpret(expr)

            if expr.output_size > 1:
                self._cg.add_assign_array_statement(
                    last_result, "output", expr.output_size)
            else:
                self._cg.add_return_statement(last_result)

        if self.with_linear_algebra:
            filename = os.path.join(
                os.path.dirname(__file__), "linear_algebra.c")
            self._cg.prepend_code_lines(utils.get_file_content(filename))

        if self.with_vectors:
            self._cg.add_dependency("<string.h>")

        if self.with_math_module:
            self._cg.add_dependency("<math.h>")

        return self._cg.code

    # Both methods supporting linear algebra do several things:
    #
    # 1. Call super method with extra parameters. Super method will return a
    #    string with a call to the respective linear algebra function;
    # 2. Add variable declaration where the result of the operation will be
    #    stored;
    # 3. Add code returned from super method to the result code;
    # 4. Return name of the variable with current result.

    def interpret_bin_vector_expr(self, expr, **kwargs):
        var_name = self._cg.add_var_declaration(expr.output_size)

        # Result: string like "addVectors(v1, v2, <size>, <var_name>)"
        func_inv = super().interpret_bin_vector_expr(
            expr, extra_func_args=[expr.output_size, var_name], **kwargs)

        self._cg.add_code_line(func_inv + ";")

        return var_name

    def interpret_bin_vector_num_expr(self, expr, **kwargs):
        var_name = self._cg.add_var_declaration(expr.output_size)

        # Result: string like "mulVectorNumber(v1, num, <size>, <var_name>)"
        func_inv = super().interpret_bin_vector_num_expr(
            expr, extra_func_args=[expr.output_size, var_name], **kwargs)

        self._cg.add_code_line(func_inv + ";")

        return var_name
