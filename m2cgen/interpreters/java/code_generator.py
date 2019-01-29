import contextlib

from m2cgen.interpreters.code_generator import CLikeCodeGenerator


class JavaCodeGenerator(CLikeCodeGenerator):

    def __init__(self, *args, **kwargs):
        super(JavaCodeGenerator, self).__init__(*args, **kwargs)

    def add_class_def(self, class_name, modifier="public"):
        class_def = modifier + " class " + class_name + " {\n"
        self.add_code_line(class_def)
        self.increase_indent()

    def add_method_def(self, name, args, return_type, modifier="public"):
        method_def = modifier + " static " + return_type + " " + name + "("
        method_def += ",".join([
            self._get_var_type(is_vector) + " " + n
            for is_vector, n in args])
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
        self.add_block_termination()

    @contextlib.contextmanager
    def method_definition(self, name, args, return_vector, modifier="public"):
        return_type = self._get_var_type(return_vector)

        self.add_method_def(name, args, return_type, modifier=modifier)
        yield
        self.add_block_termination()

    def method_invocation(self, method_name, *args):
        return method_name + "(" + ", ".join(args) + ")"

    def array_init(self, values):
        return "new " + self.vector_output_type + (
            " {" + ", ".join(values) + "}")
