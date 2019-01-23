from m2cgen.interpreters.interpreter import BaseInterpreter
from m2cgen.interpreters.java.code_generator import JavaCodeGenerator


class JavaInterpreter(BaseInterpreter):

    def __init__(self, package_name=None, model_name="Model", indent=4,
                 *args, **kwargs):
        self.package_name = package_name
        self.model_name = model_name
        self.indent = indent
        self._subroutine_idx = 0
        self._subroutine_cgs = []
        cg = JavaCodeGenerator(indent=indent)
        super(JavaInterpreter, self).__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        self._cg.reset_state()
        self._subroutine_idx = 0
        self._subroutine_cgs = []

        if self.package_name:
            self._cg.add_package_name(self.package_name)

        with self._cg.class_definition(self.model_name):
            self._do_interpret_with_method("score", expr)
            for cg in self._subroutine_cgs:
                self._cg.add_code_lines(cg.code)

        return [
            (self.model_name, self._cg.code),
        ]

    def interpret_subroutine_expr(self, expr, **kwargs):
        new_cg = JavaCodeGenerator(indent=self.indent)
        old_cg = self._cg

        method_name = self._get_subroutine_name()

        self._cg = new_cg
        self._do_interpret_with_method(method_name, expr.expr)
        self._cg = old_cg

        self._subroutine_cgs.append(new_cg)

        return method_name + "(" + self._feature_array_name + ")"

    def _get_subroutine_name(self):
        subroutine_name = "subroutine" + str(self._subroutine_idx)
        self._subroutine_idx += 1
        return subroutine_name

    def _do_interpret_with_method(self, method_name, expr):
        with self._cg.method_definition(
                name=method_name,
                args=[("double[]", self._feature_array_name)],
                return_type="double"):
            last_result = self._do_interpret(expr)
            self._cg.add_return_statement(last_result)
