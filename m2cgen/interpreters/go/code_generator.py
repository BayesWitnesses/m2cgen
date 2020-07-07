import contextlib

from m2cgen.interpreters.code_generator \
    import ImperativeCodeGenerator, CodeTemplate


class GoCodeGenerator(ImperativeCodeGenerator):
    tpl_num_value = CodeTemplate("{value}")
    tpl_infix_expression = CodeTemplate("({left}) {op} ({right})")
    tpl_array_index_access = CodeTemplate("{array_name}[{index}]")
    tpl_else_statement = CodeTemplate("}} else {{")
    tpl_block_termination = CodeTemplate("}}")
    tpl_var_declaration = CodeTemplate("var {var_name} {var_type}")
    tpl_return_statement = CodeTemplate("return {value}")
    tpl_if_statement = CodeTemplate("if {if_def} {{")
    tpl_var_assignment = CodeTemplate("{var_name} = {value}")

    scalar_type = "float64"
    vector_type = "[]float64"

    def add_function_def(self, name, args, is_scalar_output):
        return_type = self._get_var_declare_type(not is_scalar_output)

        func_args = ", ".join([
            f"{n} {self._get_var_declare_type(is_vector)}"
            for is_vector, n in args])
        function_def = f"func {name}({func_args}) {return_type} {{"
        self.add_code_line(function_def)
        self.increase_indent()

    @contextlib.contextmanager
    def function_definition(self, name, args, is_scalar_output):
        self.add_function_def(name, args, is_scalar_output)
        yield
        self.add_block_termination()

    def _get_var_declare_type(self, is_vector):
        return self.vector_type if is_vector else self.scalar_type

    def add_dependency(self, dep):
        self.prepend_code_line(f'import "{dep}"')

    def vector_init(self, values):
        return f"[]float64{{{', '.join(values)}}}"
