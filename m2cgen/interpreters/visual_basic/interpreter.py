import os

from m2cgen import ast
from m2cgen.interpreters import mixins, utils
from m2cgen.interpreters.interpreter import ImperativeToCodeInterpreter
from m2cgen.interpreters.visual_basic.code_generator \
    import VisualBasicCodeGenerator


class VisualBasicInterpreter(ImperativeToCodeInterpreter,
                             mixins.LinearAlgebraMixin):
    supported_bin_vector_ops = {
        ast.BinNumOpType.ADD: "AddVectors",
    }

    supported_bin_vector_num_ops = {
        ast.BinNumOpType.MUL: "MulVectorNumber",
    }

    abs_function_name = "Math.Abs"
    atan_function_name = "Atan"
    exponent_function_name = "Math.Exp"
    logarithm_function_name = "Math.Log"
    log1p_function_name = "Log1p"
    tanh_function_name = "Tanh"

    with_atan_expr = False
    with_log1p_expr = False
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

        if self.with_linear_algebra:
            filename = os.path.join(
                os.path.dirname(__file__), "linear_algebra.bas")
            self._cg.prepend_code_lines(utils.get_file_content(filename))

        # Use own Tanh function in order to be compatible with both VB and VBA
        if self.with_tanh_expr:
            filename = os.path.join(
                os.path.dirname(__file__), "tanh.bas")
            self._cg.prepend_code_lines(utils.get_file_content(filename))

        if self.with_log1p_expr:
            filename = os.path.join(
                os.path.dirname(__file__), "log1p.bas")
            self._cg.prepend_code_lines(utils.get_file_content(filename))

        if self.with_atan_expr:
            filename = os.path.join(
                os.path.dirname(__file__), "atan.bas")
            self._cg.prepend_code_lines(utils.get_file_content(filename))

        self._cg.prepend_code_line(self._cg.tpl_module_definition(
            module_name=self.module_name))
        self._cg.add_code_line(self._cg.tpl_block_termination(
            block_name="Module"))

        return self._cg.finalize_and_get_generated_code()

    def interpret_pow_expr(self, expr, **kwargs):
        base_result = self._do_interpret(expr.base_expr, **kwargs)
        exp_result = self._do_interpret(expr.exp_expr, **kwargs)
        return self._cg.infix_expression(
            left=base_result, right=exp_result, op="^")

    def interpret_log1p_expr(self, expr, **kwargs):
        self.with_log1p_expr = True
        return super().interpret_log1p_expr(expr, **kwargs)

    def interpret_tanh_expr(self, expr, **kwargs):
        self.with_tanh_expr = True
        return super().interpret_tanh_expr(expr, **kwargs)

    def interpret_atan_expr(self, expr, **kwargs):
        self.with_atan_expr = True
        return super().interpret_atan_expr(expr, **kwargs)
