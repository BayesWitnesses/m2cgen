from contextlib import contextmanager

from m2cgen.interpreters.code_generator import CLikeCodeGenerator, CodeTemplate


class RustCodeGenerator(CLikeCodeGenerator):

    tpl_var_declaration = CodeTemplate("let {var_name}: {var_type};")
    tpl_num_value = CodeTemplate("{value}_f64")
    tpl_if_statement = CodeTemplate("if {if_def} {{")
    tpl_return_statement = CodeTemplate("{value}")

    scalar_type = "f64"
    vector_type = "Vec<f64>"

    def add_function_def(self, name, args, is_scalar_output):
        func_args = ", ".join([
            f"{n}: {self._get_var_declare_type(is_vector)}"
            for is_vector, n in args])
        return_type = self._get_var_declare_type(not is_scalar_output)
        function_def = f"fn {name}({func_args}) -> {return_type} {{"
        self.add_code_line(function_def)
        self.increase_indent()

    @contextmanager
    def function_definition(self, name, args, is_scalar_output):
        self.add_function_def(name, args, is_scalar_output)
        yield
        self.add_block_termination()

    def vector_init(self, values):
        return (f"vec![{', '.join(values)}]")

    def _get_var_declare_type(self, is_vector):
        return self.vector_type if is_vector else self.scalar_type
