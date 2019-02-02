from m2cgen.interpreters.interpreter import BaseInterpreter
from m2cgen.interpreters.c.code_generator import CCodeGenerator


class CInterpreter(BaseInterpreter):

    def __init__(self, indent=4, *args, **kwargs):
        cg = CCodeGenerator(indent=indent)
        super(CInterpreter, self).__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        self._cg.reset_state()

        args = [(True, self._feature_array_name)]

        # C doesn't allow returning vectors, so if model returns vector we will
        # have additional vector argument which we will populate at the end.
        if expr.is_vector_output:
            args += [(True, "output")]

        with self._cg.function_definition(
                name="score",
                args=args,
                is_scalar_output=not expr.is_vector_output):

            last_result = self._do_interpret(expr)

            if expr.is_vector_output:
                self._cg.add_assign_array_statement(
                    last_result, "output", expr.size)
            else:
                self._cg.add_return_statement(last_result)

        return self._cg.code
