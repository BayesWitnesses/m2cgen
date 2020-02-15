import contextlib

from m2cgen.interpreters.code_generator import CLikeCodeGenerator


class DartCodeGenerator(CLikeCodeGenerator):

    scalar_type = "double"
    vector_type = "List<double>"

    def __init__(self, *args, **kwargs):
        super(DartCodeGenerator, self).__init__(*args, **kwargs)

    def add_class_def(self, class_name, is_private=False):
        modifier = "_" if is_private else ""
        class_def = "class " + modifier + class_name + " {"
        self.add_code_line(class_def)
        self.increase_indent()

    def add_method_def(self, name, args, is_vector_output, is_private=True):
        modifier = "_" if is_private else ""
        return_type = self._get_var_declare_type(is_vector_output)
        method_def = "static " + return_type + " " + modifier + name + "("
        method_def += ",".join([
            self._get_var_declare_type(is_vector) + " " + n
            for is_vector, n in args])
        method_def += ") {"
        self.add_code_line(method_def)
        self.increase_indent()

    @contextlib.contextmanager
    def class_definition(self, class_name, is_private=False):
        self.add_class_def(class_name, is_private=is_private)
        yield
        self.add_block_termination()

    @contextlib.contextmanager
    def method_definition(self, name, args, is_vector_output, is_private=True):
        self.add_method_def(name, args, is_vector_output,
            is_private=is_private)
        yield
        self.add_block_termination()

    def vector_init(self, values):
        return "[" + ", ".join(values) + "]"

    def _get_var_declare_type(self, is_vector):
        return (
            self.vector_type if is_vector
            else self.scalar_type)

    def add_dependency(self, dep):
        dep_str = "import '{0}';".format(dep)
        self.prepend_code_line(dep_str)
