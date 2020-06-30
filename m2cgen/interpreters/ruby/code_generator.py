import contextlib

from m2cgen.interpreters.code_generator import ImperativeCodeGenerator
from m2cgen.interpreters.code_generator import CodeTemplate as CT


class RubyCodeGenerator(ImperativeCodeGenerator):

    tpl_var_declaration = CT("")
    tpl_num_value = CT("{value}")
    tpl_infix_expression = CT("({left}) {op} ({right})")
    tpl_return_statement = tpl_num_value
    tpl_array_index_access = CT("{array_name}[{index}]")
    tpl_if_statement = CT("if {if_def}")
    tpl_else_statement = CT("else")
    tpl_block_termination = CT("end")
    tpl_var_assignment = CT("{var_name} = {value}")

    def add_function_def(self, name, args):
        func_def = f"def {name}({', '.join(args)})"
        self.add_code_line(func_def)
        self.increase_indent()

    @contextlib.contextmanager
    def function_definition(self, name, args):
        self.add_function_def(name, args)
        yield
        self.add_block_termination()

    def method_invocation(self, method_name, obj, args):
        return f"({obj}).{method_name}({', '.join(map(str, args))})"

    def vector_init(self, values):
        return f"[{', '.join(values)}]"
