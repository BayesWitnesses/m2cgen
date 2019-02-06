import re
import sys

from m2cgen import ast


class BaseInterpreter:

    with_vectors = False

    # disabled by default
    depth_threshold = sys.maxsize

    def __init__(self, cg, feature_array_name="input"):
        self._cg = cg
        self._feature_array_name = feature_array_name

    def interpret(self, expr):
        return self._do_interpret(expr)

    # Default method implementations

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

    # Private methods implementing visitor pattern

    def _do_interpret(self, expr, depth=1, **kwargs):

        # We track depth of the expression and if it exceeds specified limit,
        # we will call hook. By default it will create a variable and store
        # result of the expression in this variable. Sub-interpreters may
        # override this behaviour.
        if depth > self.depth_threshold and isinstance(expr, ast.BinExpr):
            return self._depth_threshold_hook(expr, **kwargs)

        try:
            handler = self._select_handler(expr)
        except NotImplementedError:
            if isinstance(expr, ast.TransparentExpr):
                return self._do_interpret(expr.expr, depth=depth+1, **kwargs)
            raise
        return handler(expr, depth=depth+1, **kwargs)

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

    # Default implementation. Simply adds new variable.
    def _depth_threshold_hook(self, expr, **kwargs):
        var_name = self._cg.add_var_declaration(expr.output_size)
        result = self._do_interpret(expr, **kwargs)
        self._cg.add_var_assignment(var_name, result, expr.output_size)
        return var_name


class InterpreterWithLinearAlgebra(BaseInterpreter):

    with_linear_algebra = False

    supported_bin_vector_ops = {}
    supported_bin_vector_num_ops = {}

    def interpret_bin_vector_expr(self, expr, extra_func_args=(), **kwargs):
        if expr.op not in self.supported_bin_vector_ops:
            raise NotImplementedError(
                "Op {} is unsupported".format(expr.op.name))

        self.with_linear_algebra = True

        function_name = self.supported_bin_vector_ops[expr.op]

        return self._cg.function_invocation(
            function_name,
            self._do_interpret(expr.left, **kwargs),
            self._do_interpret(expr.right, **kwargs),
            *extra_func_args)

    def interpret_bin_vector_num_expr(self, expr, extra_func_args=(),
                                      **kwargs):
        if expr.op not in self.supported_bin_vector_num_ops:
            raise NotImplementedError(
                "Op {} is unsupported".format(expr.op.name))

        self.with_linear_algebra = True

        function_name = self.supported_bin_vector_num_ops[expr.op]

        return self._cg.function_invocation(
            function_name,
            self._do_interpret(expr.left, **kwargs),
            self._do_interpret(expr.right, **kwargs),
            *extra_func_args)
