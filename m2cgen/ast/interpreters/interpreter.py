import re
from m2cgen.ast.ast import NumExpr, BoolExpr, CtrlExpr


class BaseInterpreter:

    cg = None

    def interpret(self, expr):
        return self._do_interpret(expr)

    def _do_interpret(self, expr):
        handler = self._select_handler(expr, (NumExpr, BoolExpr, CtrlExpr))
        return handler(expr)

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

    def interpret_comp_expr(self, expr):
        return self.cg.grammar.comp_expression(
            left=self._do_interpret(expr.left),
            op=expr.op.value,
            right=self._do_interpret(expr.right))

    def interpret_bin_num_expr(self, expr):
        return self.cg.grammar.bin_num_expression(
            left=self._do_interpret(expr.left),
            op=expr.op.value,
            right=self._do_interpret(expr.right))

    def interpret_num_val(self, expr):
        return self.cg.grammar.num_value(value=expr.value)

    def interpret_feature_ref(self, expr):
        return self.cg.grammar.array_index_access(array_name="input", index=expr.index)

    def interpret_if_expr(self, expr):
        var_name = self.cg.add_var_declaration()

        if_def = self._do_interpret(expr.test)
        body_def = var_name + " = " + self._do_interpret(expr.body) + ";"
        else_body = var_name + " = " + self._do_interpret(expr.orelse) + ";"

        self.cg.add_if_expr(if_def, body_def, else_body)

        return var_name
