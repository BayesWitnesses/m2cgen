import contextlib

from m2cgen.interpreters.code_generator import CLikeCodeGenerator
from m2cgen.interpreters.code_generator import CodeTemplate as CT


ARRAY_ASSIGNMENT_FUNC = """
void assign_array(double *output, double input[], int size) {
    for(int i = 0; i < size; ++i)
        output[i] = input[i];
}
"""


class CCodeGenerator(CLikeCodeGenerator):

    with_arrays_assignment = False

    tpl_scalar_var_declare = CT("double ${var_name};")
    tpl_vector_var_declare = CT("static double ${var_name}[${size}];")

    scalar_type = "double"
    vector_type = "double *"

    def __init__(self, *args, **kwargs):
        super(CCodeGenerator, self).__init__(*args, **kwargs)

    def add_function_def(self, name, args, is_vector_output):
        return_type = self._get_var_type(is_vector_output)

        function_def = return_type + " " + name + "("
        function_def += ",".join([
            self._get_var_type(is_vector) + " " + n
            for is_vector, n in args])
        function_def += ") {"
        self.add_code_line(function_def)
        self.increase_indent()

    @contextlib.contextmanager
    def function_definition(self, name, args, is_vector_output):
        self.add_function_def(name, args, is_vector_output)
        yield
        self.add_block_termination()

    def add_var_declaration(self, expr):
        var_name = self.get_var_name()

        if expr.is_vector_output:
            tpl = self.tpl_vector_var_declare
            size = expr.size
        else:
            tpl = self.tpl_scalar_var_declare
            size = None

        self.add_code_line(tpl(var_name=var_name, size=size))
        return var_name

    def add_var_assignment(self, var_name, value, expr):
        if not expr.is_vector_output:
            return super().add_var_assignment(var_name, value, False)

        # vectors require special handling since we can't just assign
        # vectors in C.

        self.with_arrays_assignment = True

        temp_var_name = self.get_var_name()
        self.add_code_line("double {}[{}] = {};".format(
            temp_var_name, expr.size, value))
        self.add_code_line("assign_array({}, {}, {});".format(
            var_name, temp_var_name, expr.size))

    def vector_init(self, values):
        return "{" + ", ".join(values) + "}"

    def finalize(self):
        if self.with_arrays_assignment:
            self.code = ARRAY_ASSIGNMENT_FUNC + self.code

    def _get_var_type(self, is_vector):
        return (
            self.vector_type if is_vector
            else self.scalar_type)
