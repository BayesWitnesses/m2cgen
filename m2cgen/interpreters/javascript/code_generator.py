import contextlib

from m2cgen.interpreters.code_generator import CLikeCodeGenerator


class JavascriptCodeGenerator(CLikeCodeGenerator):
    def __init__(self, *args, **kwargs):
        super(JavascriptCodeGenerator, self).__init__(*args, **kwargs)

    def add_function_def(self, name, args):
        function_def = "function " + name + "("
        function_def += ",".join(args)
        function_def += ") {"
        self.add_code_line(function_def)
        self.increase_indent()

    @contextlib.contextmanager
    def function_definition(self, name, args):
        self.add_function_def(name, args)
        yield
        self.add_block_termination()

    def vector_init(self, values):
        return "[" + ", ".join(values) + "]"

    def _get_var_declare_type(self, is_vector):
        return "var"
