import contextlib

from m2cgen.ast.interpreters.code_generator import BaseCodeGenerator
from m2cgen.ast.interpreters.code_generator import CodeTemplate as CT


class JavaCodeGenerator(BaseCodeGenerator):

    tpl_num_value = CT("${value}")
    tpl_infix_expression = CT("(${left}) ${op} (${right})")
    tpl_var_declaration = CT("${var_type} ${var_name};")
    tpl_return_statement = CT("return ${value};")
    tpl_array_index_access = CT("${array_name}[${index}]")
    tpl_if_statement = CT("if (${if_def}) {")
    tpl_else_statement = CT("} else {")
    tpl_close_block = CT("}")
    tpl_var_assignment = CT("${var_name} = ${value};")

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

    def add_package_name(self, package_name):
        package_def = "package " + package_name + ";\n"
        self.add_code_line(package_def)

    @contextlib.contextmanager
    def class_definition(self, model_name):
        self.add_class_def(model_name)
        yield
        self.add_close_block()

    @contextlib.contextmanager
    def method_definition(self, name, args, return_type, modifier="public"):
        self.add_method_def(name, args, return_type, modifier=modifier)
        yield
        self.add_close_block()
