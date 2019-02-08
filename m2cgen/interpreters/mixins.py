import sys
from collections import namedtuple

from m2cgen import ast
from m2cgen.interpreters.interpreter import BaseToCodeInterpreter


class BinExpressionDepthTrackingMixin(BaseToCodeInterpreter):
    """
    This mixin provides an ability to call a custom hook when depth of the
    binary expression reaches certain threshold.

    Subclasses must specify value for `bin_depth_threshold`.

    By default it creates a variable and assigns it the result of the incoming
    expression interpretation.

    Subclasses may override this default behaviour.
    """

    # disabled by default
    bin_depth_threshold = sys.maxsize

    def _pre_interpret_hook(self, expr, bin_depth=0, **kwargs):
        if not isinstance(expr, ast.BinExpr):
            return None, kwargs

        # We track depth of the binary expressions and call a hook if it
        # reaches specified threshold .
        if bin_depth == self.bin_depth_threshold:
            return self.bin_depth_threshold_hook(expr, **kwargs), kwargs

        kwargs["bin_depth"] = bin_depth + 1
        return None, kwargs

    # Default implementation. Simply adds new variable.
    def bin_depth_threshold_hook(self, expr, **kwargs):
        var_name = self._cg.add_var_declaration(expr.output_size)
        result = self._do_interpret(expr, **kwargs)
        self._cg.add_var_assignment(var_name, result, expr.output_size)
        return var_name


class LinearAlgebraMixin(BaseToCodeInterpreter):
    """
    This mixin provides simple way to interpret linear algebra expression as
    function invocation.

    It also provides flag `with_linear_algebra` which indicates whether
    linear algebra was used during interpretation. It can be used to add
    corresponding third party dependencies that provide linear algebra
    operations and/or data structures.
    """

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


Subroutine = namedtuple('Subroutine', ['name', 'expr'])


class SubroutinesAsFunctionsMixin(BaseToCodeInterpreter):
    """
    This mixin provides ability to interpret each SubroutineExpr as a function.

    Subclasses only need to implement `create_code_generator` method.

    Their code generators should implement 3 methods:
         - function_definition;
         - function_invocation;
         - add_return_statement.

    Interpreter should prepare at least one subroutine using method
    `enqueue_subroutine` and then call method `process_subroutine_queue` with
    instance of code generator, which will be populated with the result code.
    """

    def __init__(self, *args, **kwargs):
        self._subroutine_idx = 0
        self.subroutine_expr_queue = []
        super().__init__(*args, **kwargs)

    def process_subroutine_queue(self, top_code_generator):
        """
        This method should be called from the interpreter to start processing
        subroutine queue.
        """
        self._subroutine_idx = 0

        while len(self.subroutine_expr_queue):
            self._reset_reused_expr_cache()
            subroutine = self.subroutine_expr_queue.pop(0)
            subroutine_code = self.process_subroutine(subroutine)
            top_code_generator.add_code_lines(subroutine_code)

    def interpret_subroutine_expr(self, expr, **kwargs):
        """
        This method will be called whenever new subroutine is encountered.
        """
        function_name = self._get_subroutine_name()
        self.enqueue_subroutine(function_name, expr.expr)
        return self._cg.function_invocation(
            function_name, self._feature_array_name)

    def process_subroutine(self, subroutine):
        """
        Handles single subroutine. Creates new code generator and defines a
        function for a given subroutine.
        """
        is_vector_output = subroutine.expr.output_size > 1

        self._cg = self.create_code_generator()

        with self._cg.function_definition(
                name=subroutine.name,
                args=[(True, self._feature_array_name)],
                is_vector_output=is_vector_output):
            last_result = self._do_interpret(subroutine.expr)
            self._cg.add_return_statement(last_result)

        return self._cg.code

    def enqueue_subroutine(self, name, expr):
        self.subroutine_expr_queue.append(Subroutine(name, expr))

    def _get_subroutine_name(self):
        subroutine_name = "subroutine" + str(self._subroutine_idx)
        self._subroutine_idx += 1
        return subroutine_name

    # Methods to be implemented by subclasses.

    def create_code_generator(self):
        raise NotImplementedError
