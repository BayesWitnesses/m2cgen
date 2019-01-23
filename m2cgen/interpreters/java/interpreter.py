from m2cgen.interpreters.interpreter import BaseInterpreter
from m2cgen.interpreters.java.code_generator import JavaCodeGenerator


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
        self._subroutine_expr_queue = [("score", expr)]

        top_cg = self._create_code_generator()

        if self.package_name:
            top_cg.add_package_name(self.package_name)

        with top_cg.class_definition(self.model_name):
            while len(self._subroutine_expr_queue) > 0:
                method_name, next_expr = self._subroutine_expr_queue.pop(0)
                self._cg = self._create_code_generator()

                with self._cg.method_definition(
                        name=method_name,
                        args=[("double[]", self._feature_array_name)],
                        return_type="double"):
                    last_result = self._do_interpret(next_expr)
                    self._cg.add_return_statement(last_result)

                top_cg.add_code_lines(self._cg.code)

        return [
            (self.model_name, top_cg.code),
        ]

    def interpret_subroutine_expr(self, expr, **kwargs):
        method_name = self._get_subroutine_name()
        self._subroutine_expr_queue.append((method_name, expr.expr))
        return method_name + "(" + self._feature_array_name + ")"

    def _get_subroutine_name(self):
        subroutine_name = "subroutine" + str(self._subroutine_idx)
        self._subroutine_idx += 1
        return subroutine_name

    def _create_code_generator(self):
        return JavaCodeGenerator(indent=self.indent)
