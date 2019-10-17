import os

from m2cgen import ast
from m2cgen.interpreters import mixins, utils
from m2cgen.interpreters.interpreter import ToCodeInterpreter
from m2cgen.interpreters.vba.code_generator import VbaCodeGenerator


class VbaInterpreter(ToCodeInterpreter, mixins.LinearAlgebraMixin):
    supported_bin_vector_ops = {
        ast.BinNumOpType.ADD: "addVectors",
    }

    supported_bin_vector_num_ops = {
        ast.BinNumOpType.MUL: "mulVectorNumber",
    }

    exponent_function_name = "Exp"
    power_function_name = "Application.WorksheetFunction.Power"
    tanh_function_name = "Application.WorksheetFunction.Tanh"

    def __init__(self, indent=4, *args, **kwargs):
        cg = VbaCodeGenerator(indent=indent)
        kwargs["feature_array_name"] = "input_vector"
        super(VbaInterpreter, self).__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        self._cg.reset_state()
        self._reset_reused_expr_cache()

        args = [(True, self._feature_array_name)]
        func_name = "score"

        with self._cg.function_definition(
                name=func_name,
                args=args,
                is_scalar_output=expr.output_size == 1):
            last_result = self._do_interpret(expr)
            self._cg.add_return_statement(last_result, func_name)

        if self.with_linear_algebra:
            filename = os.path.join(
                os.path.dirname(__file__), "linear_algebra.bas")
            self._cg.prepend_code_lines(utils.get_file_content(filename))

        return self._cg.code
