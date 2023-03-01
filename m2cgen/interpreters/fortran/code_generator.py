from contextlib import contextmanager

from m2cgen.interpreters.code_generator import CodeTemplate, ImperativeCodeGenerator


class FortranCodeGenerator(ImperativeCodeGenerator):
    tpl_num_value = CodeTemplate("{value}d0")
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

    def reset_state(self):
        self._var_declarations = []
        super().reset_state()

    def array_index_access(self, array_name, index):
        """Note: Fortran starts array indexing at 1 and not at 0"""
        return self.tpl_array_index_access(array_name=array_name, index=index + 1)

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

    def prepend_function_def(self, name, args, output_size):
        function_def = f"function {name}({', '.join(args)})"
        self.increase_indent()
        self.prepend_code_line(self._declaration(var_name=name, size=output_size), indent=2 * self._indent)
        self.prepend_code_lines(self._var_declarations, indent=2 * self._indent)
        self.prepend_code_lines([self.tpl_vector_var_declare(var_name=arg, size=":") for arg in args],
                                indent=2 * self._indent)
        self.prepend_code_line("implicit none", indent=2 * self._indent)
        self.prepend_code_line(function_def, indent=self._indent)

    def add_function_end(self, name):
        self.decrease_indent()
        self.add_code_line("return")
        self.decrease_indent()
        self.add_code_line(f"end function {name}")

    def add_var_declaration(self, size):
        var_name = self.get_var_name()
        self._var_declarations.append(self._declaration(var_name, size))
        return var_name

    def prepend_module_def(self, name):
        self.prepend_code_line(f"contains")
        self.prepend_code_line(f"implicit none", indent=self._indent)
        self.prepend_code_line(f"module {name}")

    def add_module_end(self, name):
        self.decrease_indent()
        self.add_code_line(f"end module {name}")

    @contextmanager
    def module_definition(self, name):
        self.increase_indent()
        yield
        self.prepend_module_def(name)
        self.add_module_end(name)

    @contextmanager
    def function_definition(self, name, args, output_size):
        self.increase_indent()
        yield
        self.prepend_function_def(name, args, output_size)
        self.add_function_end(name)

    def vector_init(self, values):
        return f"(/ {', '.join(values)} /)"
