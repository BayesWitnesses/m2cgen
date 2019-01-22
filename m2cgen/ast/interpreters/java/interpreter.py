from m2cgen.ast.interpreters.interpreter import BaseInterpreter
from m2cgen.ast.interpreters.java.code_generator import JavaCodeGenerator
from m2cgen.ast.ast import IfExpr


class JavaInterpreter(BaseInterpreter):

    def __init__(self, package_name=None, model_name="Model", indent=4):
        self.package_name = package_name
        self.model_name = model_name
        self.cg = JavaCodeGenerator(indent=indent)

    def interpret(self, expr):
        self.cg.reset_state()

        if self.package_name:
            self.cg.add_package_name(self.package_name)

        with self.cg.class_definition(self.model_name):
            with self.cg.method_definition(name="score",
                                           args=[("double[]", "input")],
                                           return_type="double"):
                last_result = self._do_interpret(expr)
                self.cg.add_return_statement(last_result)

        return [
            (self.model_name, self.cg.code),
        ]

    def interpret_num_val(self, expr, **kwargs):
        return str(expr.value)

    def interpret_bin_num_expr(self, expr, **kwargs):
        left_val = self._do_interpret(expr.left, **kwargs)
        right_val = self._do_interpret(expr.right, **kwargs)
        java_expr = left_val + " " + expr.op.value + " " + right_val
        return java_expr

    def interpret_feature_ref(self, expr, **kwargs):
        index = expr.index
        return "input[" + str(index) + "]"

    def interpret_if_expr(self, expr, if_var_name=None, **kwargs):
        if if_var_name is not None:
            var_name = if_var_name
        else:
            var_name = self.cg.add_var_declaration()

        if_def = self._do_interpret(expr.test, **kwargs)
        self.cg.add_if_statement(if_def)

        def handle_nested_expr(nested):
            if isinstance(nested, IfExpr):
                self._do_interpret(nested, if_var_name=var_name, **kwargs)
            else:
                res_def = var_name + " = " + self._do_interpret(nested) + ";"
                self.cg.add_code_line(res_def)

        handle_nested_expr(expr.body)
        self.cg.add_else_statement()
        handle_nested_expr(expr.orelse)
        self.cg.add_closing_bracket()

        return var_name

    def interpret_comp_expr(self, expr, **kwargs):
        return "({}) {} ({})".format(
            self._do_interpret(expr.left, **kwargs),
            expr.op.value,
            self._do_interpret(expr.right, **kwargs))
