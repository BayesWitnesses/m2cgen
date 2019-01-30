import contextlib

from m2cgen.interpreters.code_generator import CLikeCodeGenerator


class CPPCodeGenerator(CLikeCodeGenerator):

    def __init__(self, *args, **kwargs):
        super(CPPCodeGenerator, self).__init__(*args, **kwargs)

    def add_function_def(self, name, args, is_vector_output):
        return_type = self._get_var_type(is_vector_output)

        method_def = return_type + " " + name + "("
        method_def += ",".join([
            self._get_var_type(False) + " " + n + "[]"
            for is_vector, n in args])
        method_def += ") {"
        self.add_code_line(method_def)
        self.increase_indent()

    @contextlib.contextmanager
    def function_definition(self, name, args, is_vector_output):
        self.add_function_def(name, args, is_vector_output)
        yield
        self.add_block_termination()
