import re

from m2cgen.ast import ast
from m2cgen.ast.ast import NumExpr, BoolExpr, CtrlExpr


class BaseInterpreter:

    def __init__(self, cg, feature_array_name="input"):
        self._cg = cg
        self._feature_array_name = feature_array_name

    def interpret(self, expr):
        return self._do_interpret(expr)

    def _do_interpret(self, expr, **kwargs):
        handler = self._select_handler(expr, (NumExpr, BoolExpr, CtrlExpr))
        return handler(expr, **kwargs)

    def _select_handler(self, expr, fallback_tpes):
        handler_name = self._handler_name(type(expr))
        if hasattr(self, handler_name):
            return getattr(self, handler_name)

        for expr_tpe in fallback_tpes:
            if isinstance(expr, expr_tpe):
                handler_name = self._handler_name(expr_tpe)
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

    # Default method implementations

    def interpret_if_expr(self, expr, if_var_name=None, **kwargs):
        if if_var_name is not None:
            var_name = if_var_name
        else:
            var_name = self._cg.add_var_declaration()

        if_def = self._do_interpret(expr.test, **kwargs)
        self._cg.add_if_statement(if_def)

        def handle_nested_expr(nested):
            if isinstance(nested, ast.IfExpr):
                self._do_interpret(nested, if_var_name=var_name, **kwargs)
            else:
                self._cg.add_var_assignment(
                    var_name, self._do_interpret(nested))

        handle_nested_expr(expr.body)
        self._cg.add_else_statement()
        handle_nested_expr(expr.orelse)
        self._cg.add_close_block()

        return var_name

    def interpret_comp_expr(self, expr):
        return self._cg.infix_expression(
            left=self._do_interpret(expr.left),
            op=expr.op.value,
            right=self._do_interpret(expr.right))

    def interpret_bin_num_expr(self, expr):
        return self._cg.infix_expression(
            left=self._do_interpret(expr.left),
            op=expr.op.value,
            right=self._do_interpret(expr.right))

    def interpret_num_val(self, expr):
        return self._cg.num_value(value=expr.value)

    def interpret_feature_ref(self, expr):
        return self._cg.array_index_access(
            array_name=self._feature_array_name,
            index=expr.index)
