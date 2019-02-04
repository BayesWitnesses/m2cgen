import os

from m2cgen.interpreters import utils
from m2cgen.interpreters.interpreter import BaseInterpreter
from m2cgen.interpreters.c.code_generator import CCodeGenerator


class CInterpreter(BaseInterpreter):

    with_vectors = False

    def __init__(self, indent=4, *args, **kwargs):
        cg = CCodeGenerator(indent=indent)
        super(CInterpreter, self).__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        self._cg.reset_state()

        args = [(True, self._feature_array_name)]

        # C doesn't allow returning vectors, so if model returns vector we will
        # have additional vector argument which we will populate at the end.
        if expr.output_size > 1:
            args += [(True, "output")]

        with self._cg.function_definition(
                name="score",
                args=args,
                is_scalar_output=expr.output_size == 1):

            last_result = self._do_interpret(expr)

            if expr.output_size > 1:
                self._cg.add_assign_array_statement(
                    last_result, "output", expr.output_size)
            else:
                self._cg.add_return_statement(last_result)

        if self.with_vectors:
            filename = os.path.join(
                os.path.dirname(__file__), "assign_array.c")
            self._cg.prepend_code_lines(utils.get_file_content(filename))

        return self._cg.code

    def interpret_vector_val(self, expr, **kwargs):
        self.with_vectors = True
        return super().interpret_vector_val(expr, **kwargs)
