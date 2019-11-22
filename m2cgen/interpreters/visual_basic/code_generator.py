import contextlib

from m2cgen.interpreters.code_generator import BaseCodeGenerator, CodeTemplate


class VisualBasicCodeGenerator(BaseCodeGenerator):
    tpl_num_value = CodeTemplate("${value}")
    tpl_infix_expression = CodeTemplate("(${left}) ${op} (${right})")
    tpl_var_declaration = \
        CodeTemplate("Dim ${var_name}${type_modifier} As ${var_type}")
    tpl_return_statement = CodeTemplate("${func_name} = ${value}")
    tpl_if_statement = CodeTemplate("If ${if_def} Then")
    tpl_else_statement = CodeTemplate("Else")
    tpl_block_termination = CodeTemplate("End ${block_name}")
    tpl_array_index_access = CodeTemplate("${array_name}(${index})")
    tpl_array_set_by_index = CodeTemplate("${array_name}(${index}) = ${value}")
    tpl_var_assignment = CodeTemplate("${var_name} = ${value}")
    tpl_module_definition = CodeTemplate("Module ${module_name}")

    scalar_type = "Double"

    def __init__(self, *args, **kwargs):
        super(VisualBasicCodeGenerator, self).__init__(*args, **kwargs)

    def add_return_statement(self, value, func_name):
        self.add_code_line(self.tpl_return_statement(
            func_name=func_name, value=value))

    def add_var_declaration(self, size, exac_size=False):
        var_name = self.get_var_name()
        type_modifier = ("({})".format((size - 1) if exac_size else "")
                         if size > 1 else "")
        self.add_code_line(
            self.tpl_var_declaration(
                var_name=var_name,
                type_modifier=type_modifier,
                var_type=self.scalar_type))
        return var_name

    def add_block_termination(self, block_name="If"):
        self.decrease_indent()
        self.add_code_line(self.tpl_block_termination(block_name=block_name))

    def add_function_def(self, name, args, is_scalar_output):
        return_type = self.scalar_type
        return_type += "" if is_scalar_output else "()"

        function_def = "Function " + name + "("
        function_def += ", ".join([
            ("ByRef " if is_vector else "ByVal ") + n +
            ("()" if is_vector else "") + " As " + self.scalar_type
            for is_vector, n in args])
        function_def += ") As " + return_type
        self.add_code_line(function_def)
        self.increase_indent()

    @contextlib.contextmanager
    def function_definition(self, name, args, is_scalar_output):
        self.add_function_def(name, args, is_scalar_output)
        yield
        self.decrease_indent()
        self.add_code_line(self.tpl_block_termination(block_name="Function"))

    def vector_init(self, values):
        var_name = self.add_var_declaration(len(values), exac_size=True)
        for i, val in enumerate(values):
            self.add_code_line(self.tpl_array_set_by_index(
                array_name=var_name, index=i, value=val))
        return var_name
