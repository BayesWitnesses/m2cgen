import re

from m2cgen import ast


class BaseInterpreter:

    def __init__(self, cg, feature_array_name="input"):
        self._cg = cg
        self._feature_array_name = feature_array_name

    def interpret(self, expr):
        return self._do_interpret(expr)

    # Default method implementations

    def interpret_if_expr(self, expr, if_var_name=None,
                          _is_vector_output=False, **kwargs):
        if if_var_name is not None:
            var_name = if_var_name
        else:
            var_name = self._cg.add_var_declaration(
                is_vector_type=_is_vector_output)

        def handle_nested_expr(nested):
            if isinstance(nested, ast.IfExpr):
                self._do_interpret(nested, if_var_name=var_name,
                                   _is_vector_output=_is_vector_output,
                                   **kwargs)
            else:
                nested_result = self._do_interpret(
                    nested, _is_vector_output=_is_vector_output)
                self._cg.add_var_assignment(var_name, nested_result)

        self._cg.add_if_statement(self._do_interpret(expr.test, **kwargs))
        handle_nested_expr(expr.body)
        self._cg.add_else_statement()
        handle_nested_expr(expr.orelse)
        self._cg.add_block_termination()

        return var_name

    def interpret_comp_expr(self, expr, **kwargs):
        return self._cg.infix_expression(
            left=self._do_interpret(expr.left),
            op=expr.op.value,
            right=self._do_interpret(expr.right))

    def interpret_bin_num_expr(self, expr, **kwargs):
        return self._cg.infix_expression(
            left=self._do_interpret(expr.left),
            op=expr.op.value,
            right=self._do_interpret(expr.right))

    def interpret_num_val(self, expr, **kwargs):
        return self._cg.num_value(value=expr.value)

    def interpret_feature_ref(self, expr, **kwargs):
        return self._cg.array_index_access(
            array_name=self._feature_array_name,
            index=expr.index)

    # Private methods implementing visitor pattern

    def _do_interpret(self, expr, **kwargs):
        try:
            handler = self._select_handler(expr)
        except NotImplementedError:
            if isinstance(expr, ast.TransparentExpr):
                return self._do_interpret(expr.expr, **kwargs)
            raise
        return handler(expr, **kwargs)

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
