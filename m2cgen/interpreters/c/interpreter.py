import os

from m2cgen import ast
from m2cgen.interpreters import utils
from m2cgen.interpreters.interpreter import InterpreterWithLinearAlgebra
from m2cgen.interpreters.c.code_generator import CCodeGenerator


class CInterpreter(InterpreterWithLinearAlgebra):

    supported_bin_vector_ops = {
        ast.BinNumOpType.ADD: "addVectors",
    }

    supported_bin_vector_num_ops = {
        ast.BinNumOpType.MUL: "mulVectorNumber",
    }

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

        if self.with_linear_algebra:
            filename = os.path.join(
                os.path.dirname(__file__), "linear_algebra.c")
            self._cg.prepend_code_lines(utils.get_file_content(filename))

        return self._cg.code

    # Both methods supporting linear algebra do several things:
    #
    # 1. Call super method with extra parameters which will produce a string
    #    with call to respective linear algebra function;
    # 2. Add variable declaration where the result of the operation will be
    #    stored;
    # 3. Add code returned from super method to the result code;
    # 4. Return name of the variable as current result.

    def interpret_bin_vector_expr(self, expr, *args):
        var_name = self._cg.get_var_name()

        # Result: string like "addVectors(v1, v2, <size>, <var_name>)"
        value = super().interpret_bin_vector_expr(expr, expr.size, var_name)

        self._cg.add_code_line("double {}[{}];".format(var_name, expr.size))
        self._cg.add_code_line(value + ";")

        return var_name

    def interpret_bin_vector_num_expr(self, expr, *args):
        var_name = self._cg.get_var_name()

        # Result: string like "mulVectorNumber(v1, num, <size>, <var_name>)"
        value = super().interpret_bin_vector_num_expr(
            expr, expr.size, var_name)

        self._cg.add_code_line("double {}[{}];".format(var_name, expr.size))
        self._cg.add_code_line(value + ";")

        return var_name
