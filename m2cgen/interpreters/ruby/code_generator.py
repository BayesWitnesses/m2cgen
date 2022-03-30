from contextlib import contextmanager

from m2cgen.interpreters.code_generator import CodeTemplate, ImperativeCodeGenerator


class RubyCodeGenerator(ImperativeCodeGenerator):

    tpl_var_declaration = CodeTemplate("")
    tpl_num_value = CodeTemplate("{value}")
    tpl_infix_expression = CodeTemplate("{left} {op} {right}")
    tpl_return_statement = tpl_num_value
    tpl_array_index_access = CodeTemplate("{array_name}[{index}]")
    tpl_if_statement = CodeTemplate("if {if_def}")
    tpl_else_statement = CodeTemplate("else")
    tpl_block_termination = CodeTemplate("end")
    tpl_var_assignment = CodeTemplate("{var_name} = {value}")

    def add_function_def(self, name, args):
        func_def = f"def {name}({', '.join(args)})"
        self.add_code_line(func_def)
        self.increase_indent()

    @contextmanager
    def function_definition(self, name, args):
        self.add_function_def(name, args)
        yield
        self.add_block_termination()

    def method_invocation(self, method_name, obj, args):
        return f"({obj}).{method_name}({', '.join(map(str, args))})"

    def vector_init(self, values):
        return f"[{', '.join(values)}]"
