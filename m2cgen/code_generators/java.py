import contextlib

from m2cgen.code_generators.base import BaseCodeGenerator


class JavaCodeGenerator(BaseCodeGenerator):

    def __init__(self, indent=4):
        self._indent = indent
        super(JavaCodeGenerator, self).__init__()

    def reset_state(self):
        self._current_indent = 0
        self._var_idx = 0
        self.code = ""

    def add_class_def(self, class_name, modifier="public"):
        class_def = modifier + " class " + class_name + " {\n"
        self.add_code_line(class_def)
        self.increase_indent()

    def add_method_def(self, name, args, return_type, modifier="public"):
        method_def = modifier + " static " + return_type + " " + name + "("
        method_def += ",".join([t + " " + n for t, n in args])
        method_def += ") {"
        self.add_code_line(method_def)
        self.increase_indent()

    def _get_var_name(self):
        var_name = "var" + str(self._var_idx)
        self._var_idx += 1
        return var_name

    def add_var_declaration(self, var_type="double"):
        var_name = self._get_var_name()
        var_def = var_type + " " + var_name + ";"
        self.add_code_line(var_def)
        return var_name

    def add_var_def(self, expr, var_type="double"):
        var_name = self._get_var_name()
        var_def = var_type + " " + var_name + " = " + expr + ";"
        self.add_code_line(var_def)
        return var_name

    def add_return_statement(self, expr):
        self.add_code_line("return " + expr + ";")

    def add_closing_bracket(self):
        self.decrease_indent()
        self.add_code_line("}\n")

    def add_code_line(self, line):
        indent = "".join([" "] * self._current_indent)
        self.code += indent + line + "\n"

    def increase_indent(self):
        self._current_indent += self._indent

    def decrease_indent(self):
        self._current_indent -= self._indent
        assert self._current_indent >= 0, (
            "Invalid indentation: {}".format(self._current_indent))

    def add_package_name(self, package_name):
        package_def = "package " + package_name + ";\n"
        self.add_code_line(package_def)

    def add_if_statement(self, if_def):
        self.add_code_line("if (" + if_def + ") {")
        self.increase_indent()

    def add_else_statement(self):
        self.decrease_indent()
        self.add_code_line("} else {")
        self.increase_indent()

    @contextlib.contextmanager
    def class_definition(self, model_name):
        self.add_class_def(model_name)
        yield
        self.add_closing_bracket()

    @contextlib.contextmanager
    def method_definition(self):
        self.add_method_def(name="score",
                            args=[("double[]", "input")],
                            return_type="double")
        yield
        self.add_closing_bracket()
