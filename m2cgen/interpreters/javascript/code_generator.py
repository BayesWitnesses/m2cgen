import contextlib

from m2cgen.interpreters.code_generator import CLikeCodeGenerator


class JavascriptCodeGenerator(CLikeCodeGenerator):
    def __init__(self, *args, **kwargs):
        super(JavascriptCodeGenerator, self).__init__(*args, **kwargs)

    def add_method_def(self, name, args, is_vector_output, modifier=""):        
        method_def = "function " + name + "("
        method_def += ",".join([n for is_vector, n in args])
        method_def += ") {"
        self.add_code_line(method_def)
        self.increase_indent()

    @contextlib.contextmanager
    def method_definition(self, name, args, is_vector_output,
                          modifier=""):
        self.add_method_def(name, args, is_vector_output, modifier=modifier)
        yield
        self.add_block_termination()

    def vector_init(self, values):
        return "[" + ", ".join(values) + "]"

    def _get_var_declare_type(self, is_vector):
        return "var"

    # Method `function_definition` is required by SubroutinesAsFunctionsMixin.
    # We already have this functionality in `method_definition` method.
    function_definition = method_definition
