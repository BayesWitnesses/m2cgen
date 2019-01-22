class BaseCodeGenerator:

    grammar = None

    tpl_num_value = NotImplemented
    tpl_infix_expression = NotImplemented
    tpl_return_statement = NotImplemented
    tpl_if_statement = NotImplemented
    tpl_else_statement = NotImplemented
    tpl_array_index_access = NotImplemented
    tpl_final_else_statement = NotImplemented
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

    def add_code_line(self, line, newline=True):
        indent = "".join([" "] * self._current_indent)
        self.code += indent + line
        if newline:
            self.code += "\n"

    # Following statements compute expressions using grammar AND add
    # it to the result.

    def add_return_statement(self, value):
        self.add_code_line(self.tpl_return_statement.format(value=value))

    def add_var_declaration(self, var_type="double"):
        var_name = self.get_var_name()
        self.add_code_line(
            self.tpl_var_declaration.format(
                var_type=var_type, var_name=var_name))
        return var_name

    def add_if_statement(self, if_def):
        self.add_code_line(self.tpl_if_statement.format(if_def=if_def))
        self.increase_indent()

    def add_else_statement(self):
        self.decrease_indent()
        self.add_code_line(self.tpl_else_statement)
        self.increase_indent()

    def add_final_else_statement(self):
        self.decrease_indent()
        self.add_code_line(self.tpl_final_else_statement)

    def add_var_assignment(self, var_name, value):
        self.add_code_line(
            self.tpl_var_assignment.format(var_name=var_name, value=value))

    # Following methods simply compute expressions using grammar without
    # changing result.

    def infix_expression(self, left, right, op):
        return self.tpl_infix_expression.format(left=left, right=right, op=op)

    def num_value(self, value):
        return self.tpl_num_value.format(value=value)

    def array_index_access(self, array_name, index):
        return self.tpl_array_index_access.format(
            array_name=array_name, index=index)
