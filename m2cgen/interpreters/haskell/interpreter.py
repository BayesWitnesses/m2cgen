import os

from m2cgen import ast
from m2cgen.interpreters import mixins, utils
from m2cgen.interpreters.haskell.code_generator import HaskellCodeGenerator
from m2cgen.interpreters.interpreter import ToCodeInterpreter


class HaskellInterpreter(ToCodeInterpreter,
                         mixins.LinearAlgebraMixin):
    supported_bin_vector_ops = {
        ast.BinNumOpType.ADD: "addVectors",
    }

    supported_bin_vector_num_ops = {
        ast.BinNumOpType.MUL: "mulVectorNumber",
    }

    abs_function_name = "abs"
    exponent_function_name = "exp"
    sqrt_function_name = "sqrt"
    tanh_function_name = "tanh"

    def __init__(self,  module_name="Model", indent=4, function_name="score",
                 *args, **kwargs):
        self.module_name = module_name
        self.indent = indent
        self.function_name = function_name

        cg = HaskellCodeGenerator(indent=indent)
        super(HaskellInterpreter, self).__init__(cg, *args, **kwargs)

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

        if self.with_linear_algebra:
            filename = os.path.join(
                os.path.dirname(__file__), "linear_algebra.hs")
            self._cg.prepend_code_lines(utils.get_file_content(filename))

        self._cg.prepend_code_line(self._cg.tpl_module_definition(
            module_name=self.module_name))

        return self._cg.finalize_and_get_generated_code()

    def interpret_if_expr(self, expr, if_code_gen=None, **kwargs):
        if if_code_gen is None:
            code_gen = HaskellCodeGenerator(indent=self.indent)
            nested = False
        else:
            code_gen = if_code_gen
            nested = True

        code_gen.add_if_statement(self._do_interpret(
            expr.test, **kwargs))
        code_gen.add_code_line(self._do_interpret(
            expr.body, if_code_gen=code_gen, **kwargs))
        code_gen.add_else_statement()
        code_gen.add_code_line(self._do_interpret(
            expr.orelse, if_code_gen=code_gen, **kwargs))
        code_gen.add_if_termination()

        if not nested:
            return self._cache_reused_expr(
                expr, code_gen.finalize_and_get_generated_code())

    def interpret_pow_expr(self, expr, **kwargs):
        base_result = self._do_interpret(expr.base_expr, **kwargs)
        exp_result = self._do_interpret(expr.exp_expr, **kwargs)
        return self._cg.infix_expression(
            left=base_result, right=exp_result, op="**")

    # Cached expressions become functions with no arguments, i.e. values
    # which are CAFs. Therefore, they are computed only once.
    def _cache_reused_expr(self, expr, expr_result):
        if expr in self._cached_expr_results:
            return self._cached_expr_results[expr].var_name
        else:
            func_name = self._cg.get_func_name()
            self._cached_expr_results[expr] = utils.CachedResult(
                var_name=func_name, expr_result=expr_result)
            return func_name

    def _dump_cache(self):
        if self._cached_expr_results:
            self._cg.add_code_line("where")
            self._cg.increase_indent()
            for func_name, expr_result in self._cached_expr_results.values():
                self._cg.add_function(
                    function_name=func_name, function_body=expr_result)
            self._cg.decrease_indent()
