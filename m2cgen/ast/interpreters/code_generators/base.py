class BaseCodeGenerator:

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
