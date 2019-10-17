import contextlib

from m2cgen.interpreters.code_generator import BaseCodeGenerator, CodeTemplate


class VbaCodeGenerator(BaseCodeGenerator):
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

    scalar_type = "Double"

    def __init__(self, *args, **kwargs):
        super(VbaCodeGenerator, self).__init__(*args, **kwargs)


    def add_return_statement(self, value, func_name):
        self.add_code_line(
            self.tpl_return_statement(
                func_name=func_name, value=value))

    def add_var_declaration(self, size):
        var_name = self.get_var_name()
        is_vector = size > 1
        type_modifier = "()" if is_vector else ""
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
        ret = self.tpl_var_declaration(
            var_name="return_arr",
            type_modifier="({})".format(len(values)),
            var_type=self.scalar_type)
        ret += "\n"
        for i, val in enumerate(values):
            ret += self.tpl_array_set_by_index(
                array_name="return_arr", index=i, value=val)
            ret += "\n"
        return ret
