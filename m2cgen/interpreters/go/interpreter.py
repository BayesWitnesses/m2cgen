import os

from m2cgen import ast
from m2cgen.interpreters import mixins, utils
from m2cgen.interpreters.go.code_generator import GoCodeGenerator
from m2cgen.interpreters.interpreter import ToCodeInterpreter


class GoInterpreter(ToCodeInterpreter,
                    mixins.LinearAlgebraMixin):
    supported_bin_vector_ops = {
        ast.BinNumOpType.ADD: "addVectors",
    }

    supported_bin_vector_num_ops = {
        ast.BinNumOpType.MUL: "mulVectorNumber",
    }

    exponent_function_name = "math.Exp"
    power_function_name = "math.Pow"
    tanh_function_name = "math.Tanh"

    def __init__(self, indent=4, *args, **kwargs):
        cg = GoCodeGenerator(indent=indent)
        super(GoInterpreter, self).__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        self._cg.reset_state()
        self._reset_reused_expr_cache()

        args = [(True, self._feature_array_name)]

        with self._cg.function_definition(
                name="score",
                args=args,
                is_scalar_output=expr.output_size == 1):

            last_result = self._do_interpret(expr)

            self._cg.add_return_statement(last_result)

        if self.with_linear_algebra:
            filename = os.path.join(
                os.path.dirname(__file__), "linear_algebra.go")
            self._cg.prepend_code_lines(utils.get_file_content(filename))

        if self.with_math_module:
            self._cg.add_dependency("math")

        return self._cg.code
