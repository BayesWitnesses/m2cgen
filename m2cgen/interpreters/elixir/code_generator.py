from contextlib import contextmanager

from m2cgen.interpreters.code_generator import CodeTemplate, FunctionalCodeGenerator


class ElixirCodeGenerator(FunctionalCodeGenerator):
    tpl_function_signature = CodeTemplate("{function_name} = fn ->")
    tpl_if_statement = CodeTemplate("cond do {if_def} -> ")
    tpl_else_statement = CodeTemplate("true ->")
    tpl_num_value = CodeTemplate("{value}")
    tpl_block_termination = CodeTemplate("end")
    tpl_infix_expression = CodeTemplate("{left} {op} {right}")
    tpl_module_definition = CodeTemplate("""defmodule {module_name} do
    @compile {{:inline, read: 2}}
    defp read(bin, pos) do
        <<_::size(pos)-unit(64)-binary, value::float, _::binary>> = bin
        value
    end
    defp list_to_binary(list) do
        for i <- list, into: <<>>, do: <<i::float>>
    end
    """)
    tpl_array_index_access = CodeTemplate("read({array_name},{index})")

    def add_if_termination(self):
        self.decrease_indent()
        self.add_code_line(self.tpl_block_termination())

    def get_func_name(self):
        func_name = f"func{self._func_idx}.()"
        self._func_idx += 1
        return func_name

    def add_function(self, function_name, function_body):
        self.add_code_line(self.tpl_function_signature(
            function_name=function_name.replace(".()", "")))
        self.increase_indent()
        self.add_code_lines(function_body)
        self.decrease_indent()
        self.add_code_line(self.tpl_block_termination())

    def add_function_def(self, name, args, is_scalar_output):

        func_args = ", ".join([n for _, n in args])
        function_def = f"def {name}({func_args}) do"
        self.add_code_line(function_def)

        self.increase_indent()
        self.add_code_line("input = list_to_binary(input)")

    def function_invocation(self, function_name, *args):
        function_args = ", ".join(args)
        return f"{function_name}({function_args})"

    @contextmanager
    def function_definition(self, name, args, is_scalar_output):
        self.increase_indent()
        self.add_function_def(name, args, is_scalar_output)
        yield
        self.decrease_indent()
        self.add_code_line(self.tpl_block_termination())
        self.decrease_indent()

    def vector_init(self, values):
        return f"[{', '.join(values)}]"
