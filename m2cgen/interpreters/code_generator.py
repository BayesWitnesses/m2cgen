from string import Template


class CodeTemplate:

    def __init__(self, template):
        self.template = Template(template)
        self.str_template = template

    def __str__(self):
        return self.str_template

    def __call__(self, *args, **kwargs):
        return self.template.substitute(*args, **kwargs)


class BaseCodeGenerator:
    """
    This class provides basic functionality to generate code. It is
    language-agnostic, but exposes set of attributes which subclasses should
    use to define syntax specific for certain language(s).

    !!IMPORTANT!!: Code generators must know nothing about AST.
    """

    tpl_num_value = NotImplemented
    tpl_infix_expression = NotImplemented
    tpl_var_declaration = NotImplemented
    tpl_return_statement = NotImplemented
    tpl_if_statement = NotImplemented
    tpl_else_statement = NotImplemented
    tpl_array_index_access = NotImplemented
    tpl_block_termination = NotImplemented
    tpl_var_assignment = NotImplemented

    def __init__(self, indent=4):
        self._indent = indent
        self.reset_state()

    def reset_state(self):
        self._current_indent = 0
        self._var_idx = 0
        self.code = ""

    def get_var_name(self):
        var_name = "var" + str(self._var_idx)
        self._var_idx += 1
        return var_name

    def increase_indent(self):
        self._current_indent += self._indent

    def decrease_indent(self):
        self._current_indent -= self._indent
        assert self._current_indent >= 0, (
            "Invalid indentation: {}".format(self._current_indent))

    # All code modifications should be implemented via following methods.

    def add_code_line(self, line):
        if not line:
            return
        indent = " " * self._current_indent
        self.code += indent + line + "\n"

    def add_code_lines(self, lines):
        if isinstance(lines, str):
            lines = lines.split("\n")
        for l in lines:
            self.add_code_line(l)

    def prepend_code_line(self, line):
        self.code = line + "\n" + self.code

    def prepend_code_lines(self, lines):
        if isinstance(lines, str):
            lines = lines.strip().split("\n")
        for l in lines[::-1]:
            self.prepend_code_line(l)

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
        return function_name + "(" + ", ".join(map(str, args)) + ")"

    # Helpers

    def _get_var_declare_type(self, expr):
        return NotImplemented


class CLikeCodeGenerator(BaseCodeGenerator):
    """
    This code generator provides C-like syntax so that subclasses will only
    have to provide logic for wrapping expressions into functions/classes/etc.
    """

    tpl_num_value = CodeTemplate("${value}")
    tpl_infix_expression = CodeTemplate("(${left}) ${op} (${right})")
    tpl_var_declaration = CodeTemplate("${var_type} ${var_name};")
    tpl_return_statement = CodeTemplate("return ${value};")
    tpl_array_index_access = CodeTemplate("${array_name}[${index}]")
    tpl_if_statement = CodeTemplate("if (${if_def}) {")
    tpl_else_statement = CodeTemplate("} else {")
    tpl_block_termination = CodeTemplate("}")
    tpl_var_assignment = CodeTemplate("${var_name} = ${value};")
