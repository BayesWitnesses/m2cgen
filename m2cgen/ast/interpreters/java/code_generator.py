import contextlib

from m2cgen.ast.interpreters.code_generator import BaseCodeGenerator
from m2cgen.ast.interpreters.grammar import BaseGrammar


class JavaCodeGenerator(BaseCodeGenerator):

    class grammar(BaseGrammar):
        num_value = "${value}"
        infix_expression = "(${left}) ${op} (${right})"
        var_declaration = "${var_type} ${var_name};"
        return_statement = "return ${value};"
        array_index_access = "${array_name}[${index}]"
        if_statement = "if (${if_def}) {"
        else_statement = "} else {"

    def __init__(self, *args, **kwargs):
        super(JavaCodeGenerator, self).__init__(*args, **kwargs)

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

    def add_closing_bracket(self):
        self.decrease_indent()
        self.add_code_line("}")

    def finalize_else_statement(self):
        self.add_closing_bracket()

    def add_package_name(self, package_name):
        package_def = "package " + package_name + ";\n"
        self.add_code_line(package_def)

    @contextlib.contextmanager
    def class_definition(self, model_name):
        self.add_class_def(model_name)
        yield
        self.add_closing_bracket()

    @contextlib.contextmanager
    def method_definition(self, name, args, return_type, modifier="public"):
        self.add_method_def(name, args, return_type, modifier=modifier)
        yield
        self.add_closing_bracket()
