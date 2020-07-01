import contextlib

from m2cgen.interpreters.code_generator import CLikeCodeGenerator


class JavascriptCodeGenerator(CLikeCodeGenerator):

    def add_function_def(self, name, args):
        function_def = f"function {name}({', '.join(args)}) {{"
        self.add_code_line(function_def)
        self.increase_indent()

    @contextlib.contextmanager
    def function_definition(self, name, args):
        self.add_function_def(name, args)
        yield
        self.add_block_termination()

    def vector_init(self, values):
        return f"[{', '.join(values)}]"

    def _get_var_declare_type(self, is_vector):
        return "var"
