from m2cgen.ast.interpreters.base import BaseInterpreter


class JavaInterpreter(BaseInterpreter):

    def __init__(self, code_generator):
        self.cg = code_generator

    def interpret(self, expr):
        result = self._do_interpret(expr)
        self.cg.add_return_statement(result)

    def interpret_num_val(self, expr):
        return str(expr.value)

    def interpret_bin_num_expr(self, expr):
        left_val = self._do_interpret(expr.left)
        right_val = self._do_interpret(expr.right)
        java_expr = left_val + " " + expr.op.value + " " + right_val
        return java_expr

    def interpret_feature_ref(self, expr):
        index = expr.index
        return "input[" + str(index) + "]"

    def interpret_if_expr(self, expr):
        var_name = self.cg.add_var_declaration()

        if_def = self._do_interpret(expr.test)
        body_def = var_name + " = " + self._do_interpret(expr.body) + ";"
        else_body = var_name + " = " + self._do_interpret(expr.orelse) + ";"

        self.cg.add_if_statement(if_def)
        self.cg.add_code_line(body_def)
        self.cg.add_else_statement()
        self.cg.add_code_line(else_body)
        self.cg.add_closing_bracket()

        return var_name

    def interpret_comp_expr(self, expr):
        return "({}) {} ({})".format(
            self._do_interpret(expr.left),
            expr.op.value,
            self._do_interpret(expr.right))
