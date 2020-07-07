import contextlib

from m2cgen.interpreters.code_generator import CLikeCodeGenerator
from m2cgen.interpreters.code_generator import CodeTemplate as CT


class CCodeGenerator(CLikeCodeGenerator):

    tpl_scalar_var_declare = CT("double {var_name};")
    tpl_vector_var_declare = CT("double {var_name}[{size}];")

    scalar_type = "double"
    vector_type = "double *"

    def add_function_def(self, name, args, is_scalar_output):
        return_type = self.scalar_type if is_scalar_output else "void"

        func_args = ", ".join([
            f"{self._get_var_type(is_vector)} {n}"
            for is_vector, n in args])
        function_def = f"{return_type} {name}({func_args}) {{"
        self.add_code_line(function_def)
        self.increase_indent()

    @contextlib.contextmanager
    def function_definition(self, name, args, is_scalar_output):
        self.add_function_def(name, args, is_scalar_output)
        yield
        self.add_block_termination()

    def add_var_declaration(self, size):
        var_name = self.get_var_name()

        if size > 1:
            tpl = self.tpl_vector_var_declare
        else:
            tpl = self.tpl_scalar_var_declare

        self.add_code_line(tpl(var_name=var_name, size=size))
        return var_name

    def add_var_assignment(self, var_name, value, value_size):
        if value_size == 1:
            return super().add_var_assignment(var_name, value, value_size)

        # vectors require special handling since we can't just assign
        # vectors in C.
        self.add_assign_array_statement(value, var_name, value_size)

    def add_assign_array_statement(self, source_var, target_var, size):
        self.add_code_line(f"memcpy({target_var}, {source_var}, "
                           f"{size} * sizeof(double));")

    def add_dependency(self, dep):
        self.prepend_code_line(f"#include {dep}")

    def vector_init(self, values):
        return f"(double[]){{{', '.join(values)}}}"

    def _get_var_type(self, is_vector):
        return (
            self.vector_type if is_vector
            else self.scalar_type)
