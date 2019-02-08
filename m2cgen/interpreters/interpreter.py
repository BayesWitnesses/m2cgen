import re

from m2cgen import ast


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

    def _do_interpret(self, expr, **kwargs):
        # Hook which allows to override kwargs and to return custom result.
        result, kwargs = self._pre_interpret_hook(expr, **kwargs)

        # If result is empty, it means that we still need to process expr.
        if result is not None:
            return result

        try:
            handler = self._select_handler(expr)
        except NotImplementedError:
            if isinstance(expr, ast.TransparentExpr):
                return self._do_interpret(expr.expr, **kwargs)
            raise

        if not expr.to_reuse:
            return handler(expr, **kwargs)

        if expr in self._cached_expr_results:
            return self._cached_expr_results[expr]

        result = handler(expr, **kwargs)
        return self._cache_reused_expr(expr, result)

    def _cache_reused_expr(self, expr, expr_result):
        # No caching by default.
        return expr_result

    def _reset_reused_expr_cache(self):
        self._cached_expr_results = {}

    def _select_handler(self, expr):
        handler_name = self._handler_name(type(expr))
        if hasattr(self, handler_name):
            return getattr(self, handler_name)
        raise NotImplementedError(
            "No handler found for {}".format(type(expr).__name__))

    @staticmethod
    def _handler_name(expr_tpe):
        expr_name = BaseInterpreter._normalize_expr_name(expr_tpe.__name__)
        return "interpret_" + expr_name

    @staticmethod
    def _normalize_expr_name(name):
        return re.sub("(?!^)([A-Z]+)", r"_\1", name).lower()


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

    def __init__(self, cg, feature_array_name="input"):
        super().__init__(cg, feature_array_name=feature_array_name)
        self.with_vectors = False

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

    def interpret_comp_expr(self, expr, **kwargs):
        return self._cg.infix_expression(
            left=self._do_interpret(expr.left, **kwargs),
            op=expr.op.value,
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

    def _cache_reused_expr(self, expr, expr_result):
        var_name = self._cg.add_var_declaration(expr.output_size)
        self._cg.add_var_assignment(var_name, expr_result, expr.output_size)
        self._cached_expr_results[expr] = var_name
        return var_name
