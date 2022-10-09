import math
import sys
from collections import namedtuple

from m2cgen import ast
from m2cgen.interpreters.interpreter import BaseToCodeInterpreter
from m2cgen.interpreters.utils import chunks


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
            return super()._pre_interpret_hook(expr, **kwargs)

        # We track depth of the binary expressions and call a hook if it
        # reaches specified threshold.
        if bin_depth >= self.bin_depth_threshold:
            return self.bin_depth_threshold_hook(expr, **kwargs), kwargs

        kwargs["bin_depth"] = bin_depth + 1
        return super()._pre_interpret_hook(expr, **kwargs)

    # Default implementation. Simply adds new variable.
    def bin_depth_threshold_hook(self, expr, **kwargs):
        if expr in self._cached_expr_results:
            return self._cached_expr_results[expr].var_name
        result = self._do_interpret(expr, **kwargs)
        var_name = self._cg.add_var_declaration(expr.output_size)
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
            raise NotImplementedError(f"Op '{expr.op.name}' is unsupported")

        self.with_linear_algebra = True

        function_name = self.supported_bin_vector_ops[expr.op]

        return self._cg.function_invocation(
            function_name,
            self._do_interpret(expr.left, **kwargs),
            self._do_interpret(expr.right, **kwargs),
            *extra_func_args)

    def interpret_bin_vector_num_expr(self, expr, extra_func_args=(), **kwargs):
        if expr.op not in self.supported_bin_vector_num_ops:
            raise NotImplementedError(f"Op '{expr.op.name}' is unsupported")

        self.with_linear_algebra = True

        function_name = self.supported_bin_vector_num_ops[expr.op]

        return self._cg.function_invocation(
            function_name,
            self._do_interpret(expr.left, **kwargs),
            self._do_interpret(expr.right, **kwargs),
            *extra_func_args)


Subroutine = namedtuple('Subroutine', ['name', 'idx', 'expr'])


class SubroutinesMixin(BaseToCodeInterpreter):
    """
    This mixin provides ability to split the code into subroutines based on
    the size of the AST.

    Subclasses only need to implement `create_code_generator` method.

    Their code generators should implement 5 methods:
         - function_definition;
         - function_invocation;
         - module_definition;
         - module_function_invocation;
         - add_return_statement.

    Interpreter should prepare at least one subroutine using method
    `enqueue_subroutine` and then call method `process_subroutine_queue` with
    instance of code generator, which will be populated with the result code.
    """

    # disabled by default
    ast_size_check_frequency = sys.maxsize
    ast_size_per_subroutine_threshold = sys.maxsize
    subroutine_per_group_threshold = sys.maxsize

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
        subroutines = []

        while self.subroutine_expr_queue:
            self._reset_reused_expr_cache()
            subroutine = self.subroutine_expr_queue.pop(0)
            subroutine_code = self._process_subroutine(subroutine)
            subroutines.append((subroutine, subroutine_code))

        subroutines.sort(key=lambda subroutine: subroutine[0].idx)

        groups = chunks(subroutines, self.subroutine_per_group_threshold)
        for _, subroutine_code in next(groups):
            top_code_generator.add_code_lines(subroutine_code)

        for index, subroutine_group in enumerate(groups):
            cg = self.create_code_generator()

            with cg.module_definition(
                    module_name=self._format_group_name(index + 1)):
                for _, subroutine_code in subroutine_group:
                    cg.add_code_lines(subroutine_code)

            top_code_generator.add_code_lines(
                cg.finalize_and_get_generated_code())

    def enqueue_subroutine(self, name, idx, expr):
        self.subroutine_expr_queue.append(Subroutine(name, idx, expr))

    def _pre_interpret_hook(self, expr, ast_size_check_counter=0, **kwargs):
        if isinstance(expr, ast.BinExpr) and not expr.to_reuse:
            frequency = self._adjust_ast_check_frequency(expr)
            self.ast_size_check_frequency = min(frequency, self.ast_size_check_frequency)

            ast_size_check_counter += 1
            if ast_size_check_counter >= self.ast_size_check_frequency:
                ast_size_check_counter = 0
                ast_size = ast.count_exprs(expr)
                if ast_size > self.ast_size_per_subroutine_threshold:
                    function_name = self._get_subroutine_name()

                    self.enqueue_subroutine(function_name, self._subroutine_idx, expr)

                    group_idx = self._subroutine_idx // self.subroutine_per_group_threshold
                    if group_idx != 0:
                        return self._cg.module_function_invocation(
                            self._format_group_name(group_idx),
                            function_name,
                            self._feature_array_name), kwargs

                    return self._cg.function_invocation(function_name, self._feature_array_name), kwargs

            kwargs['ast_size_check_counter'] = ast_size_check_counter

        return super()._pre_interpret_hook(expr, **kwargs)

    def _adjust_ast_check_frequency(self, expr):
        """
        The logic below counts the number of non-binary expressions
        in a non-recursive branch of a binary expression to account
        for large tree-like models and adjust the size check frequency
        if necessary.
        """
        cnt = None
        if not isinstance(expr.left, ast.BinExpr):
            cnt = ast.count_exprs(expr.left, exclude_list={ast.BinExpr})
        elif not isinstance(expr.right, ast.BinExpr):
            cnt = ast.count_exprs(expr.right, exclude_list={ast.BinExpr})
        if cnt and cnt < self.ast_size_per_subroutine_threshold:
            return math.ceil(self.ast_size_per_subroutine_threshold / cnt)
        return self.ast_size_check_frequency

    def _process_subroutine(self, subroutine):
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

        return self._cg.finalize_and_get_generated_code()

    def _get_subroutine_name(self):
        subroutine_name = f"subroutine{self._subroutine_idx}"
        self._subroutine_idx += 1
        return subroutine_name

    @staticmethod
    def _format_group_name(group_idx):
        return f"SubroutineGroup{group_idx}"

    # Methods to be implemented by subclasses.

    def create_code_generator(self):
        raise NotImplementedError


class PowExprInfixMixin(BaseToCodeInterpreter):
    """
    This mixin is used for languages that provide the exponentiation operation in a form
    of an infix operator. Such languages inlcude Haskell, F#, R and others.

    The operator used by default is "**", but it can be overriden by setting an appropriate
    value in `pow_operator`.
    """

    pow_operator = "**"

    infix_expressions = (*BaseToCodeInterpreter.infix_expressions, ast.PowExpr)

    def interpret_pow_expr(
        self,
        expr,
        is_left_from_parent=None,
        parent_precedence=None,
        is_parent_associative=None,
        **kwargs
    ):
        base_result = self._do_interpret(
            expr.base_expr,
            is_left_from_parent=True,
            parent_precedence=expr.precedence,
            **kwargs
        )
        exp_result = self._do_interpret(
            expr.exp_expr,
            is_left_from_parent=False,
            parent_precedence=expr.precedence,
            is_parent_associative=expr.is_associative,
            **kwargs
        )
        return self._cg.infix_expression(
            left=base_result,
            right=exp_result,
            op=self.pow_operator,
            wrap=self._wrap_infix_expr(
                expr,
                is_left_from_parent=is_left_from_parent,
                parent_precedence=parent_precedence,
                is_parent_associative=is_parent_associative
            )
        )


class PowExprFunctionMixin(BaseToCodeInterpreter):
    """
    This mixin is used for languages that provide the exponentiation operation as a function.
    Such languages inlcude C, Java, Python and others.

    The name of the function must be set in `power_function_name` by implementing subclasses.
    """

    power_function_name = NotImplemented

    def interpret_pow_expr(self, expr, **kwargs):
        if self.power_function_name is NotImplemented:
            raise NotImplementedError("Power function is not provided")
        self.with_math_module = True
        base_result = self._do_interpret(expr.base_expr, **kwargs)
        exp_result = self._do_interpret(expr.exp_expr, **kwargs)
        return self._cg.function_invocation(self.power_function_name, base_result, exp_result)
