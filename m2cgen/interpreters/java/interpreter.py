from m2cgen.interpreters.interpreter import BaseInterpreter
from m2cgen.interpreters.java.code_generator import JavaCodeGenerator
from m2cgen import ast
from collections import namedtuple


Subroutine = namedtuple('Subroutine', ['name', 'is_multi_output', 'expr'])


class JavaInterpreter(BaseInterpreter):

    def __init__(self, package_name=None, model_name="Model", indent=4,
                 *args, **kwargs):
        self.package_name = package_name
        self.model_name = model_name
        self.indent = indent
        self._subroutine_idx = 0
        self._subroutine_expr_queue = []
        cg = self._create_code_generator()
        super(JavaInterpreter, self).__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        self._subroutine_idx = 0

        top_cg = self._create_code_generator()

        if self.package_name:
            top_cg.add_package_name(self.package_name)

        with top_cg.class_definition(self.model_name):
            if isinstance(expr, ast.SubroutineExpr):
                self._do_interpret(expr)
            else:
                self._subroutine_expr_queue = [
                    Subroutine("score", False, expr)
                ]

            while len(self._subroutine_expr_queue) > 0:
                subroutine = self._subroutine_expr_queue.pop(0)
                is_multi_output = subroutine.is_multi_output
                return_type = "double[]" if is_multi_output else "double"
                self._cg = self._create_code_generator()

                with self._cg.method_definition(
                        name=subroutine.name,
                        args=[("double[]", self._feature_array_name)],
                        return_type=return_type):
                    last_result = self._do_interpret(
                        subroutine.expr,
                        is_multi_output=is_multi_output)
                    self._cg.add_return_statement(last_result)

                top_cg.add_code_lines(self._cg.code)

        return [
            (self.model_name, top_cg.code),
        ]

    def interpret_subroutine_expr(self, expr, **kwargs):
        method_name = self._get_subroutine_name()
        return self._enqueue_subroutine(method_name, expr)

    def interpret_main_expr(self, expr, **kwargs):
        return self._enqueue_subroutine("score", expr)

    def interpret_array_expr(self, expr, **kwargs):
        nested = []
        for e in expr.exprs:
            nested.append(self._do_interpret(e, **kwargs))
        return self._cg.array_init(nested)

    def _enqueue_subroutine(self, name, expr):
        self._subroutine_expr_queue.append(
            Subroutine(name, expr.is_multi_output, expr.expr))
        return name + "(" + self._feature_array_name + ")"

    def _get_subroutine_name(self):
        subroutine_name = "subroutine" + str(self._subroutine_idx)
        self._subroutine_idx += 1
        return subroutine_name

    def _create_code_generator(self):
        return JavaCodeGenerator(indent=self.indent)
