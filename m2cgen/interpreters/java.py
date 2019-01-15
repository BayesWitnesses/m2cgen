from m2cgen.interpreters.base import BaseInterpreter


class JavaGenerator(BaseInterpreter):
    def __init__(self, package_name=None, model_name="Model", indent=4):
        self._reset_state()
        self._package_name = package_name
        self._model_name = model_name
        self._indent = indent

    def interpret(self, expr):
        self._reset_state()

        if self._package_name:
            package_def = "package " + self._package_name + ";\n"
            self._add_code_line(package_def)

        self._add_class_def(self._model_name)
        self._add_method_def(name="score",
                             args=[("double[]", "input")],
                             return_type="double")
        last_result = self._do_interpret(expr)
        self._add_return_statement(last_result)
        self._add_closing_bracket()  # Close method.
        self._add_closing_bracket()  # Close class.
        return self._code

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

    def _add_class_def(self, class_name, modifier="public"):
        class_def = modifier + " class " + class_name + " {\n"
        self._add_code_line(class_def)
        self._current_indent += self._indent

    def _add_method_def(self, name, args, return_type, modifier="public"):
        method_def = modifier + " static " + return_type + " " + name + "("
        method_def += ",".join([t + " " + n for t, n in args])
        method_def += ") {"
        self._add_code_line(method_def)
        self._current_indent += self._indent

    def _add_var_def(self, expr, var_type="double"):
        var_name = "var" + str(self._var_idx)
        self._var_idx += 1
        var_def = var_type + " " + var_name + " = " + expr + ";"
        self._add_code_line(var_def)
        return var_name

    def _add_return_statement(self, expr):
        self._add_code_line("return " + expr + ";")

    def _add_closing_bracket(self):
        self._current_indent -= self._indent
        self._add_code_line("}\n")

    def _add_code_line(self, line):
        indent = "".join([" "] * self._current_indent)
        self._code += indent + line + "\n"

    def _reset_state(self):
        self._current_indent = 0
        self._var_idx = 0
        self._code = ""
