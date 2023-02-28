from contextlib import contextmanager

from m2cgen.interpreters.code_generator import CodeTemplate, ImperativeCodeGenerator


class FortranCodeGenerator(ImperativeCodeGenerator):
    tpl_num_value = CodeTemplate("{value}")
    tpl_infix_expression = CodeTemplate("{left} {op} {right}")
    tpl_return_statement_vec = CodeTemplate("{func_name}(:) = {value}")
    tpl_return_statement_single = CodeTemplate("{func_name} = {value}")
    tpl_array_index_access = CodeTemplate("{array_name}({index})")
    tpl_if_statement = CodeTemplate("if ({if_def}) then")
    tpl_else_statement = CodeTemplate("else")
    tpl_var_assignment = CodeTemplate("{var_name} = {value}")
    tpl_scalar_var_declare = CodeTemplate("double precision :: {var_name}")
    tpl_vector_var_declare = CodeTemplate("double precision, dimension({size}) :: {var_name}")

    tpl_block_termination = CodeTemplate("end if")

    def add_return_statement(self, value, func_name, output_size):
        if output_size > 1:
            tpl = self.tpl_return_statement_vec
        else:
            tpl = self.tpl_return_statement_single

        self.add_code_line(tpl(value=value, func_name=func_name))

    def _declaration(self, var_name, size):
        if size > 1:
            tpl = self.tpl_vector_var_declare
        else:
            tpl = self.tpl_scalar_var_declare

        return tpl(var_name=var_name, size=size)

    def add_function_def(self, name, args, output_size):
        function_def = f"function {name}({', '.join(args)})"
        self.add_code_line(function_def)
        self.increase_indent()
        self.add_code_line(self._declaration(var_name=name, size=output_size))
        self.add_code_lines([self.tpl_vector_var_declare(var_name=arg, size=":") for arg in args])

    def add_function_end(self, name):
        self.add_code_line("return")
        self.decrease_indent()
        self.add_code_line(f"end function {name}")

    def add_var_declaration(self, size):
        # We use implicit declerations for the local variables
        return self.get_var_name()

    @contextmanager
    def function_definition(self, name, args, output_size):
        self.add_function_def(name, args, output_size)
        yield
        self.add_function_end(name)

    def vector_init(self, values):
        return f"(/ {', '.join(values)} /)"
