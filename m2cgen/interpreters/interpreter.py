from m2cgen import ast
from m2cgen.assemblers import fallback_expressions
from m2cgen.interpreters.utils import CachedResult, _get_handler_name


class BaseInterpreter:
    """
    Base class of AST interpreter. Provides single public method .interpret()
    which takes instance of AST expression and recursively applies method
    _do_interpret() to it.
    """
    def __init__(self):
        self._cached_expr_results = {}

    def interpret(self, expr):
        self._reset_reused_expr_cache()
        return self._do_interpret(expr)

    # Private methods implementing Visitor pattern

    def _pre_interpret_hook(self, expr, **kwargs):
        return None, kwargs

    def _do_interpret(self, expr, to_reuse=None, **kwargs):
        # Hook which allows to override kwargs and to return custom result.
        result, kwargs = self._pre_interpret_hook(expr, **kwargs)

        # If result is empty, it means that we still need to process expr.
        if result is not None:
            return result

        if expr in self._cached_expr_results:
            return self._cached_expr_results[expr].var_name

        handler = self._select_handler(expr)

        # Note that the reuse flag passed in the arguments has a higher
        # precedence than one specified in the expression. One use case for
        # this behavior is to override the original to_reuse flag for
        # expressions that are wrapped by subroutine expression in case when
        # subroutines are not supported by specific interpreter implementation.
        expr_to_reuse = to_reuse if to_reuse is not None else expr.to_reuse
        if not expr_to_reuse:
            return handler(expr, **kwargs)

        result = handler(expr, **kwargs)
        return self._cache_reused_expr(expr, result)

    def _cache_reused_expr(self, expr, expr_result):
        # No caching by default.
        return expr_result

    def _reset_reused_expr_cache(self):
        self._cached_expr_results = {}

    def _select_handler(self, expr):
        handler_name = _get_handler_name(type(expr))
        if hasattr(self, handler_name):
            return getattr(self, handler_name)
        raise NotImplementedError(
            f"No handler found for '{type(expr).__name__}'")


class BaseToCodeInterpreter(BaseInterpreter):

    def __init__(self, cg, feature_array_name="input"):
        super().__init__()
        self._cg = cg
        self._feature_array_name = feature_array_name


class ToCodeInterpreter(BaseToCodeInterpreter):
    """
    This interpreter provides default implementation for the methods
    interpreting AST expression into code.

    It can be used for the most programming languages and requires only
    language-specific instance of the CodeGenerator.

    !!IMPORTANT!!: Code generators used by this interpreter must know nothing
    about AST.
    """

    abs_function_name = NotImplemented
    atan_function_name = NotImplemented
    exponent_function_name = NotImplemented
    logarithm_function_name = NotImplemented
    log1p_function_name = NotImplemented
    power_function_name = NotImplemented
    sqrt_function_name = NotImplemented
    tanh_function_name = NotImplemented

    def __init__(self, cg, feature_array_name="input"):
        super().__init__(cg, feature_array_name=feature_array_name)
        self.with_vectors = False
        self.with_math_module = False

    def interpret_id_expr(self, expr, **kwargs):
        return self._do_interpret(expr.expr, **kwargs)

    def interpret_comp_expr(self, expr, **kwargs):
        op = self._cg._comp_op_overwrite(expr.op)
        return self._cg.infix_expression(
            left=self._do_interpret(expr.left, **kwargs),
            op=op,
            right=self._do_interpret(expr.right, **kwargs))

    def interpret_bin_num_expr(self, expr, **kwargs):
        return self._cg.infix_expression(
            left=self._do_interpret(expr.left, **kwargs),
            op=expr.op.value,
            right=self._do_interpret(expr.right, **kwargs))

    def interpret_num_val(self, expr, **kwargs):
        return self._cg.num_value(value=expr.value)

    def interpret_feature_ref(self, expr, **kwargs):
        return self._cg.array_index_access(
            array_name=self._feature_array_name,
            index=expr.index)

    def interpret_vector_val(self, expr, **kwargs):
        self.with_vectors = True
        nested = [self._do_interpret(expr, **kwargs) for expr in expr.exprs]
        return self._cg.vector_init(nested)

    def interpret_abs_expr(self, expr, **kwargs):
        if self.abs_function_name is NotImplemented:
            return self._do_interpret(
                fallback_expressions.abs(expr.expr), **kwargs)
        self.with_math_module = True
        nested_result = self._do_interpret(expr.expr, **kwargs)
        return self._cg.function_invocation(
            self.abs_function_name, nested_result)

    def interpret_atan_expr(self, expr, **kwargs):
        if self.atan_function_name is NotImplemented:
            return self._do_interpret(
                fallback_expressions.atan(expr.expr), **kwargs)
        self.with_math_module = True
        nested_result = self._do_interpret(expr.expr, **kwargs)
        return self._cg.function_invocation(
            self.atan_function_name, nested_result)

    def interpret_exp_expr(self, expr, **kwargs):
        if self.exponent_function_name is NotImplemented:
            return self._do_interpret(
                fallback_expressions.exp(expr.expr),
                **kwargs)
        self.with_math_module = True
        nested_result = self._do_interpret(expr.expr, **kwargs)
        return self._cg.function_invocation(
            self.exponent_function_name, nested_result)

    def interpret_log_expr(self, expr, **kwargs):
        if self.logarithm_function_name is NotImplemented:
            raise NotImplementedError("Logarithm function is not provided")
        self.with_math_module = True
        nested_result = self._do_interpret(expr.expr, **kwargs)
        return self._cg.function_invocation(
            self.logarithm_function_name, nested_result)

    def interpret_log1p_expr(self, expr, **kwargs):
        if self.log1p_function_name is NotImplemented:
            return self._do_interpret(
                fallback_expressions.log1p(expr.expr), **kwargs)
        self.with_math_module = True
        nested_result = self._do_interpret(expr.expr, **kwargs)
        return self._cg.function_invocation(
            self.log1p_function_name, nested_result)

    def interpret_sqrt_expr(self, expr, **kwargs):
        if self.sqrt_function_name is NotImplemented:
            return self._do_interpret(
                fallback_expressions.sqrt(expr.expr),
                **kwargs)
        self.with_math_module = True
        nested_result = self._do_interpret(expr.expr, **kwargs)
        return self._cg.function_invocation(
            self.sqrt_function_name, nested_result)

    def interpret_tanh_expr(self, expr, **kwargs):
        if self.tanh_function_name is NotImplemented:
            return self._do_interpret(
                fallback_expressions.tanh(expr.expr), **kwargs)
        self.with_math_module = True
        nested_result = self._do_interpret(expr.expr, **kwargs)
        return self._cg.function_invocation(
            self.tanh_function_name, nested_result)

    def interpret_pow_expr(self, expr, **kwargs):
        if self.power_function_name is NotImplemented:
            raise NotImplementedError("Power function is not provided")
        self.with_math_module = True
        base_result = self._do_interpret(expr.base_expr, **kwargs)
        exp_result = self._do_interpret(expr.exp_expr, **kwargs)
        return self._cg.function_invocation(
            self.power_function_name, base_result, exp_result)


class ImperativeToCodeInterpreter(ToCodeInterpreter):
    """
    This interpreter provides default implementation for the methods
    interpreting AST expression into code.

    It can be used for the most programming languages and requires only
    language-specific instance of the CodeGenerator.

    !!IMPORTANT!!: Code generators used by this interpreter must know nothing
    about AST.
    """

    def interpret_if_expr(self, expr, if_var_name=None, **kwargs):
        if if_var_name is not None:
            var_name = if_var_name
        else:
            var_name = self._cg.add_var_declaration(expr.output_size)

        def handle_nested_expr(nested):
            if isinstance(nested, ast.IfExpr):
                self._do_interpret(nested, if_var_name=var_name, **kwargs)
            else:
                nested_result = self._do_interpret(nested, **kwargs)
                self._cg.add_var_assignment(var_name, nested_result,
                                            nested.output_size)

        self._cg.add_if_statement(self._do_interpret(expr.test, **kwargs))
        handle_nested_expr(expr.body)
        self._cg.add_else_statement()
        handle_nested_expr(expr.orelse)
        self._cg.add_block_termination()

        return var_name

    def _cache_reused_expr(self, expr, expr_result):
        var_name = self._cg.add_var_declaration(expr.output_size)
        self._cg.add_var_assignment(var_name, expr_result, expr.output_size)
        self._cached_expr_results[expr] = CachedResult(
            var_name=var_name, expr_result=None)
        return var_name


class FunctionalToCodeInterpreter(ToCodeInterpreter):
    """
    This interpreter provides default implementation for the methods
    interpreting AST expression into code.

    It can be used for the most functional programming languages and requires
    only language-specific instance of the CodeGenerator.

    !!IMPORTANT!!: Code generators used by this interpreter must know nothing
    about AST.
    """

    def interpret_if_expr(self, expr, if_code_gen=None, **kwargs):
        if if_code_gen is None:
            code_gen = self.create_code_generator()
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

    # Cached expressions become functions with no arguments, i.e. values
    # which are CAFs. Therefore, they are computed only once.
    def _cache_reused_expr(self, expr, expr_result):
        if expr in self._cached_expr_results:
            return self._cached_expr_results[expr].var_name
        else:
            func_name = self._cg.get_func_name()
            self._cached_expr_results[expr] = CachedResult(
                var_name=func_name, expr_result=expr_result)
            return func_name

    def create_code_generator(self):
        raise NotImplementedError
