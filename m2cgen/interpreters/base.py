import re
from m2cgen.ast import NumExpr, BoolExpr, CtrlExpr


class BaseInterpreter:

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
