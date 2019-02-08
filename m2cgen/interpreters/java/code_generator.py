import contextlib

from m2cgen.interpreters.code_generator import CLikeCodeGenerator


class JavaCodeGenerator(CLikeCodeGenerator):

    scalar_output_type = "double"
    vector_output_type = "double[]"

    def __init__(self, *args, **kwargs):
        super(JavaCodeGenerator, self).__init__(*args, **kwargs)

    def add_class_def(self, class_name, modifier="public"):
        class_def = modifier + " class " + class_name + " {\n"
        self.add_code_line(class_def)
        self.increase_indent()

    def add_method_def(self, name, args, is_vector_output, modifier="public"):
        return_type = self._get_var_declare_type(is_vector_output)

        method_def = modifier + " static " + return_type + " " + name + "("
        method_def += ",".join([
            self._get_var_declare_type(is_vector) + " " + n
            for is_vector, n in args])
        method_def += ") {"
        self.add_code_line(method_def)
        self.increase_indent()

    def add_package_name(self, package_name):
        package_def = "package " + package_name + ";\n"
        self.add_code_line(package_def)

    @contextlib.contextmanager
    def class_definition(self, class_name):
        self.add_class_def(class_name)
        yield
        self.add_block_termination()

    @contextlib.contextmanager
    def method_definition(self, name, args, is_vector_output,
                          modifier="public"):
        self.add_method_def(name, args, is_vector_output, modifier=modifier)
        yield
        self.add_block_termination()

    def vector_init(self, values):
        return "new " + self.vector_output_type + (
            " {" + ", ".join(values) + "}")

    def _get_var_declare_type(self, is_vector):
        return (
            self.vector_output_type if is_vector
            else self.scalar_output_type)

    # Method `function_definition` is required by SubroutinesAsFunctionsMixin.
    # We already have this functionality in `method_definition` method.
    function_definition = method_definition
