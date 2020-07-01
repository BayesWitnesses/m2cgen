import contextlib

from m2cgen.interpreters.code_generator import CLikeCodeGenerator


class DartCodeGenerator(CLikeCodeGenerator):

    scalar_type = "double"
    vector_type = "List<double>"

    def add_function_def(self, name, args, is_vector_output):
        return_type = self._get_var_declare_type(is_vector_output)
        func_args = ",".join([
            f"{self._get_var_declare_type(is_vector)} {n}"
            for is_vector, n in args])
        function_def = f"{return_type} {name}({func_args}) {{"
        self.add_code_line(function_def)
        self.increase_indent()

    @contextlib.contextmanager
    def function_definition(self, name, args, is_vector_output):
        self.add_function_def(name, args, is_vector_output)
        yield
        self.add_block_termination()

    def method_invocation(self, method_name, obj, args):
        return f"({obj}).{method_name}({', '.join(map(str, args))})"

    def vector_init(self, values):
        return f"[{', '.join(values)}]"

    def _get_var_declare_type(self, is_vector):
        return (
            self.vector_type if is_vector
            else self.scalar_type)

    def add_dependency(self, dep):
        self.prepend_code_line(f"import '{dep}';")
