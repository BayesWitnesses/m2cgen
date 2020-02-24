import contextlib

from m2cgen.interpreters.code_generator import CLikeCodeGenerator


class DartCodeGenerator(CLikeCodeGenerator):

    scalar_type = "double"
    vector_type = "List<double>"

    def __init__(self, *args, **kwargs):
        super(DartCodeGenerator, self).__init__(*args, **kwargs)

    def add_function_def(self, name, args, is_vector_output):
        return_type = self._get_var_declare_type(is_vector_output)
        function_def = return_type + " " + name + "("
        function_def += ",".join([
            self._get_var_declare_type(is_vector) + " " + n
            for is_vector, n in args])
        function_def += ") {"
        self.add_code_line(function_def)
        self.increase_indent()

    @contextlib.contextmanager
    def function_definition(self, name, args, is_vector_output):
        self.add_function_def(name, args, is_vector_output)
        yield
        self.add_block_termination()

    def vector_init(self, values):
        return "[" + ", ".join(values) + "]"

    def _get_var_declare_type(self, is_vector):
        return (
            self.vector_type if is_vector
            else self.scalar_type)

    def add_dependency(self, dep):
        dep_str = "import '" + dep + "';"
        self.prepend_code_line(dep_str)
