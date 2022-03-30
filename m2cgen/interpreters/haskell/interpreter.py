from pathlib import Path

from m2cgen.ast import BinNumOpType
from m2cgen.interpreters.haskell.code_generator import HaskellCodeGenerator
from m2cgen.interpreters.interpreter import FunctionalToCodeInterpreter
from m2cgen.interpreters.mixins import LinearAlgebraMixin, PowExprInfixMixin
from m2cgen.interpreters.utils import get_file_content


class HaskellInterpreter(FunctionalToCodeInterpreter,
                         PowExprInfixMixin,
                         LinearAlgebraMixin):

    supported_bin_vector_ops = {
        BinNumOpType.ADD: "addVectors",
    }

    supported_bin_vector_num_ops = {
        BinNumOpType.MUL: "mulVectorNumber",
    }

    abs_function_name = "abs"
    atan_function_name = "atan"
    exponent_function_name = "exp"
    logarithm_function_name = "log"
    log1p_function_name = "log1p"
    sigmoid_function_name = "sigmoid"
    softmax_function_name = "softmax"
    sqrt_function_name = "sqrt"
    tanh_function_name = "tanh"

    with_log1p_expr = False
    with_sigmoid_expr = False
    with_softmax_expr = False

    def __init__(self,  module_name="Model", indent=4, function_name="score",
                 *args, **kwargs):
        self.module_name = module_name
        self.indent = indent
        self.function_name = function_name

        super().__init__(self.create_code_generator(), *args, **kwargs)

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
            self._cg.add_code_line(last_result)
            self._dump_cache()

        current_dir = Path(__file__).absolute().parent

        if self.with_linear_algebra:
            filename = current_dir / "linear_algebra.hs"
            self._cg.add_code_lines(get_file_content(filename))

        if self.with_log1p_expr:
            filename = current_dir / "log1p.hs"
            self._cg.add_code_lines(get_file_content(filename))

        if self.with_softmax_expr:
            filename = current_dir / "softmax.hs"
            self._cg.add_code_lines(get_file_content(filename))

        if self.with_sigmoid_expr:
            filename = current_dir / "sigmoid.hs"
            self._cg.add_code_lines(get_file_content(filename))

        self._cg.prepend_code_line(self._cg.tpl_module_definition(
            module_name=self.module_name))

        return self._cg.finalize_and_get_generated_code()

    def create_code_generator(self):
        return HaskellCodeGenerator(indent=self.indent)

    def interpret_log1p_expr(self, expr, **kwargs):
        self.with_log1p_expr = True
        return super().interpret_log1p_expr(expr, **kwargs)

    def interpret_softmax_expr(self, expr, **kwargs):
        self.with_softmax_expr = True
        return super().interpret_softmax_expr(expr, **kwargs)

    def interpret_sigmoid_expr(self, expr, **kwargs):
        self.with_sigmoid_expr = True
        return super().interpret_sigmoid_expr(expr, **kwargs)

    def _dump_cache(self):
        if self._cached_expr_results:
            self._cg.add_code_line("where")
            self._cg.increase_indent()
            for func_name, expr_result in self._cached_expr_results.values():
                self._cg.add_function(
                    function_name=func_name, function_body=expr_result)
            self._cg.decrease_indent()
