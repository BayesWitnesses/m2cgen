from pathlib import Path

from m2cgen.ast import BinNumOpType
from m2cgen.interpreters.c.code_generator import CCodeGenerator
from m2cgen.interpreters.interpreter import ImperativeToCodeInterpreter
from m2cgen.interpreters.mixins import LinearAlgebraMixin, PowExprFunctionMixin
from m2cgen.interpreters.utils import get_file_content


class CInterpreter(ImperativeToCodeInterpreter,
                   PowExprFunctionMixin,
                   LinearAlgebraMixin):

    supported_bin_vector_ops = {
        BinNumOpType.ADD: "add_vectors",
    }

    supported_bin_vector_num_ops = {
        BinNumOpType.MUL: "mul_vector_number",
    }

    abs_function_name = "fabs"
    atan_function_name = "atan"
    exponent_function_name = "exp"
    logarithm_function_name = "log"
    log1p_function_name = "log1p"
    power_function_name = "pow"
    sigmoid_function_name = "sigmoid"
    softmax_function_name = "softmax"
    sqrt_function_name = "sqrt"
    tanh_function_name = "tanh"

    with_sigmoid_expr = False
    with_softmax_expr = False

    def __init__(self, indent=4, function_name="score", *args, **kwargs):
        self.function_name = function_name

        cg = CCodeGenerator(indent=indent)
        super().__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        self._cg.reset_state()
        self._reset_reused_expr_cache()

        args = [(True, self._feature_array_name)]

        # C doesn't allow returning vectors, so if model returns vector we will
        # have additional vector argument which we will populate at the end.
        if expr.output_size > 1:
            args += [(True, "output")]

        with self._cg.function_definition(
                name=self.function_name,
                args=args,
                is_scalar_output=expr.output_size == 1):

            last_result = self._do_interpret(expr)

            if expr.output_size > 1:
                self._cg.add_assign_array_statement(
                    last_result, "output", expr.output_size)
            else:
                self._cg.add_return_statement(last_result)

        current_dir = Path(__file__).absolute().parent

        if self.with_linear_algebra:
            filename = current_dir / "linear_algebra.c"
            self._cg.prepend_code_lines(get_file_content(filename))

        if self.with_softmax_expr:
            filename = current_dir / "softmax.c"
            self._cg.prepend_code_lines(get_file_content(filename))

        if self.with_sigmoid_expr:
            filename = current_dir / "sigmoid.c"
            self._cg.prepend_code_lines(get_file_content(filename))

        if self.with_vectors:
            self._cg.add_dependency("<string.h>")

        if self.with_math_module:
            self._cg.add_dependency("<math.h>")

        return self._cg.finalize_and_get_generated_code()

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

        self._cg.add_code_line(f"{func_inv};")

        return var_name

    def interpret_bin_vector_num_expr(self, expr, **kwargs):
        var_name = self._cg.add_var_declaration(expr.output_size)

        # Result: string like "mulVectorNumber(v1, num, <size>, <var_name>)"
        func_inv = super().interpret_bin_vector_num_expr(
            expr, extra_func_args=[expr.output_size, var_name], **kwargs)

        self._cg.add_code_line(f"{func_inv};")

        return var_name

    # Do the same things for softmax as for linear algebra.
    def interpret_softmax_expr(self, expr, **kwargs):
        self.with_vectors = True
        self.with_softmax_expr = True

        var_name = self._cg.add_var_declaration(expr.output_size)
        nested = [self._do_interpret(expr, **kwargs) for expr in expr.exprs]
        func_inv = self._cg.function_invocation(
            self.softmax_function_name,
            self._cg.vector_init(nested),
            expr.output_size,
            var_name)
        self._cg.add_code_line(f"{func_inv};")
        return var_name

    def interpret_sigmoid_expr(self, expr, **kwargs):
        self.with_sigmoid_expr = True
        return super().interpret_sigmoid_expr(expr, **kwargs)
