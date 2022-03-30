from pathlib import Path

from m2cgen.ast import BinNumOpType
from m2cgen.interpreters.interpreter import ImperativeToCodeInterpreter
from m2cgen.interpreters.mixins import LinearAlgebraMixin, PowExprInfixMixin
from m2cgen.interpreters.utils import get_file_content
from m2cgen.interpreters.visual_basic.code_generator import VisualBasicCodeGenerator


class VisualBasicInterpreter(ImperativeToCodeInterpreter,
                             PowExprInfixMixin,
                             LinearAlgebraMixin):

    supported_bin_vector_ops = {
        BinNumOpType.ADD: "AddVectors",
    }

    supported_bin_vector_num_ops = {
        BinNumOpType.MUL: "MulVectorNumber",
    }

    abs_function_name = "Math.Abs"
    atan_function_name = "Atan"
    exponent_function_name = "Math.Exp"
    logarithm_function_name = "Math.Log"
    log1p_function_name = "Log1p"
    sigmoid_function_name = "Sigmoid"
    softmax_function_name = "Softmax"
    tanh_function_name = "Tanh"

    pow_operator = "^"

    with_atan_expr = False
    with_log1p_expr = False
    with_sigmoid_expr = False
    with_softmax_expr = False
    with_tanh_expr = False

    def __init__(self, module_name="Model", indent=4, function_name="Score",
                 *args, **kwargs):
        self.module_name = module_name
        self.function_name = function_name
        cg = VisualBasicCodeGenerator(indent=indent)
        kwargs["feature_array_name"] = "inputVector"
        super().__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        self._cg.reset_state()
        self._reset_reused_expr_cache()

        args = [(True, self._feature_array_name)]
        func_name = self.function_name

        with self._cg.function_definition(
                name=func_name,
                args=args,
                is_scalar_output=expr.output_size == 1):
            last_result = self._do_interpret(expr)
            self._cg.add_return_statement(last_result, func_name)

        current_dir = Path(__file__).absolute().parent

        if self.with_linear_algebra:
            filename = current_dir / "linear_algebra.bas"
            self._cg.add_code_lines(get_file_content(filename))

        if self.with_atan_expr:
            filename = current_dir / "atan.bas"
            self._cg.add_code_lines(get_file_content(filename))

        if self.with_log1p_expr:
            filename = current_dir / "log1p.bas"
            self._cg.add_code_lines(get_file_content(filename))

        if self.with_sigmoid_expr:
            filename = current_dir / "sigmoid.bas"
            self._cg.add_code_lines(get_file_content(filename))

        if self.with_softmax_expr:
            filename = current_dir / "softmax.bas"
            self._cg.add_code_lines(get_file_content(filename))

        # Use own Tanh function in order to be compatible with both VB and VBA
        if self.with_tanh_expr:
            filename = current_dir / "tanh.bas"
            self._cg.add_code_lines(get_file_content(filename))

        self._cg.prepend_code_line(self._cg.tpl_module_definition(
            module_name=self.module_name))
        self._cg.add_code_line(self._cg.tpl_block_termination(
            block_name="Module"))

        return self._cg.finalize_and_get_generated_code()

    def interpret_log1p_expr(self, expr, **kwargs):
        self.with_log1p_expr = True
        return super().interpret_log1p_expr(expr, **kwargs)

    def interpret_tanh_expr(self, expr, **kwargs):
        self.with_tanh_expr = True
        return super().interpret_tanh_expr(expr, **kwargs)

    def interpret_atan_expr(self, expr, **kwargs):
        self.with_atan_expr = True
        return super().interpret_atan_expr(expr, **kwargs)

    def interpret_softmax_expr(self, expr, **kwargs):
        self.with_softmax_expr = True
        return super().interpret_softmax_expr(expr, **kwargs)

    def interpret_sigmoid_expr(self, expr, **kwargs):
        self.with_sigmoid_expr = True
        return super().interpret_sigmoid_expr(expr, **kwargs)
