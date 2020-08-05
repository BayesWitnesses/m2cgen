from io import StringIO
from weakref import finalize

import numpy as np

from m2cgen.interpreters.utils import format_float


class CodeTemplate:

    def __init__(self, template):
        self.str_template = template

    def __str__(self):
        return self.str_template

    def __call__(self, *args, **kwargs):

        def _is_float(value):
            return isinstance(value, (float, np.floating))

        return self.str_template.format(
            *[format_float(i) if _is_float(i) else i for i in args],
            **{k: format_float(v) if _is_float(v) else v
               for k, v in kwargs.items()})


class BaseCodeGenerator:
    """
    This class provides basic functionality to generate code. It is
    language-agnostic, but exposes set of attributes which subclasses should
    use to define syntax specific for certain language(s).

    !!IMPORTANT!!: Code generators must know nothing about AST.
    """

    tpl_num_value = NotImplemented
    tpl_infix_expression = NotImplemented
    tpl_array_index_access = NotImplemented

    def __init__(self, indent=4):
        self._indent = indent
        self._code_buf = None
        self.reset_state()

    def reset_state(self):
        self._current_indent = 0
        self._finalize_buffer()
        self._code_buf = StringIO()
        self._code = None
        self._finalizer = finalize(self, self._finalize_buffer)

    def _finalize_buffer(self):
        if self._code_buf is not None and not self._code_buf.closed:
            self._code_buf.close()

    def _write_to_code_buffer(self, text, prepend=False):
        if self._code_buf.closed:
            raise BufferError(
                "Cannot modify code after getting generated code and "
                "closing the underlying buffer!\n"
                "Call reset_state() to allocate new buffer.")
        if prepend:
            self._code_buf.seek(0)
            old_content = self._code_buf.read()
            self._code_buf.seek(0)
            text += old_content
        self._code_buf.write(text)

    def finalize_and_get_generated_code(self):
        if not self._code_buf.closed:
            self._code = self._code_buf.getvalue()
            self._finalize_buffer()
        return self._code if self._code is not None else ""

    def increase_indent(self):
        self._current_indent += self._indent

    def decrease_indent(self):
        self._current_indent -= self._indent
        assert self._current_indent >= 0, (
            f"Invalid indentation: {self._current_indent}")

    # All code modifications should be implemented via following methods.

    def add_code_line(self, line):
        if not line:
            return
        self.add_code_lines([line.strip()])

    def add_code_lines(self, lines):
        if isinstance(lines, str):
            lines = lines.strip().split("\n")
        indent = " " * self._current_indent
        self._write_to_code_buffer(
            indent + f"\n{indent}".join(lines) + "\n")

    def prepend_code_line(self, line):
        if not line:
            return
        self.prepend_code_lines([line.strip()])

    def prepend_code_lines(self, lines):
        new_line = "\n"
        if isinstance(lines, str):
            lines = lines.strip().split(new_line)
        self._write_to_code_buffer(
            f"{new_line.join(lines)}{new_line}", prepend=True)

    # Following methods simply compute expressions using templates without
    # changing result.

    def infix_expression(self, left, right, op):
        return self.tpl_infix_expression(left=left, right=right, op=op)

    def num_value(self, value):
        return self.tpl_num_value(value=value)

    def array_index_access(self, array_name, index):
        return self.tpl_array_index_access(
            array_name=array_name, index=index)

    def function_invocation(self, function_name, *args):
        return f"{function_name}({', '.join(map(str, args))})"

    # Helpers

    def _comp_op_overwrite(self, op):
        return op.value


class ImperativeCodeGenerator(BaseCodeGenerator):
    """
    This class provides basic functionality to generate code. It is
    language-agnostic, but exposes set of attributes which subclasses should
    use to define syntax specific for certain language(s).

    !!IMPORTANT!!: Code generators must know nothing about AST.
    """

    tpl_var_declaration = NotImplemented
    tpl_return_statement = NotImplemented
    tpl_if_statement = NotImplemented
    tpl_else_statement = NotImplemented
    tpl_block_termination = NotImplemented
    tpl_var_assignment = NotImplemented

    def reset_state(self):
        super().reset_state()
        self._var_idx = 0

    def get_var_name(self):
        var_name = f"var{self._var_idx}"
        self._var_idx += 1
        return var_name

    # Following statements compute expressions using templates AND add
    # it to the result.

    def add_return_statement(self, value):
        self.add_code_line(self.tpl_return_statement(value=value))

    def add_var_declaration(self, size):
        var_name = self.get_var_name()
        is_vector = size > 1
        var_type = self._get_var_declare_type(is_vector)
        self.add_code_line(
            self.tpl_var_declaration(
                var_type=var_type, var_name=var_name))
        return var_name

    def add_if_statement(self, if_def):
        self.add_code_line(self.tpl_if_statement(if_def=if_def))
        self.increase_indent()

    def add_else_statement(self):
        self.decrease_indent()
        self.add_code_line(self.tpl_else_statement())
        self.increase_indent()

    def add_block_termination(self):
        self.decrease_indent()
        self.add_code_line(self.tpl_block_termination())

    def add_var_assignment(self, var_name, value, value_size):
        self.add_code_line(
            self.tpl_var_assignment(var_name=var_name, value=value))

    # Helpers

    def _get_var_declare_type(self, expr):
        return NotImplemented


class CLikeCodeGenerator(ImperativeCodeGenerator):
    """
    This code generator provides C-like syntax so that subclasses will only
    have to provide logic for wrapping expressions into functions/classes/etc.
    """

    tpl_num_value = CodeTemplate("{value}")
    tpl_infix_expression = CodeTemplate("({left}) {op} ({right})")
    tpl_var_declaration = CodeTemplate("{var_type} {var_name};")
    tpl_return_statement = CodeTemplate("return {value};")
    tpl_array_index_access = CodeTemplate("{array_name}[{index}]")
    tpl_if_statement = CodeTemplate("if ({if_def}) {{")
    tpl_else_statement = CodeTemplate("}} else {{")
    tpl_block_termination = CodeTemplate("}}")
    tpl_var_assignment = CodeTemplate("{var_name} = {value};")


class FunctionalCodeGenerator(BaseCodeGenerator):
    """
    This class provides basic functionality to generate code. It is
    language-agnostic, but exposes set of attributes which subclasses should
    use to define syntax specific for certain language(s).

    !!IMPORTANT!!: Code generators must know nothing about AST.
    """

    tpl_function_signature = NotImplemented
    tpl_if_statement = NotImplemented
    tpl_else_statement = NotImplemented
    tpl_block_termination = NotImplemented

    def reset_state(self):
        super().reset_state()
        self._func_idx = 0

    def get_func_name(self):
        func_name = f"func{self._func_idx}"
        self._func_idx += 1
        return func_name

    # Following statements compute expressions using templates AND add
    # it to the result.

    def add_function(self, function_name, function_body):
        self.add_code_line(self.tpl_function_signature(
            function_name=function_name))
        self.increase_indent()
        self.add_code_lines(function_body)
        self.decrease_indent()

    def function_invocation(self, function_name, *args):
        function_args = " ".join(map(lambda x: f"({x})", args))
        return f"{function_name} {function_args}"

    def add_if_statement(self, if_def):
        self.add_code_line(self.tpl_if_statement(if_def=if_def))
        self.increase_indent()

    def add_else_statement(self):
        self.decrease_indent()
        self.add_code_line(self.tpl_else_statement())
        self.increase_indent()

    def add_block_termination(self):
        self.decrease_indent()
        self.add_code_line(self.tpl_block_termination())
