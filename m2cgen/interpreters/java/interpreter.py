import os

from m2cgen import ast
from m2cgen.interpreters import utils
from m2cgen.interpreters.interpreter import InterpreterWithLinearAlgebra
from m2cgen.interpreters.java.code_generator import JavaCodeGenerator

from collections import namedtuple


Subroutine = namedtuple('Subroutine', ['name', 'expr'])


class JavaInterpreter(InterpreterWithLinearAlgebra):

    supported_bin_vector_ops = {
        ast.BinNumOpType.ADD: "addVectors",
    }

    supported_bin_vector_num_ops = {
        ast.BinNumOpType.MUL: "mulVectorNumber",
    }

    def __init__(self, package_name=None, model_name="Model", indent=4,
                 *args, **kwargs):
        self.package_name = package_name
        self.model_name = model_name
        self.indent = indent
        self._subroutine_idx = 0
        self._subroutine_expr_queue = []
        cg = self._create_code_generator()
        super(JavaInterpreter, self).__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        self._subroutine_expr_queue = [Subroutine("score", expr)]

        self._subroutine_idx = 0

        top_cg = self._create_code_generator()

        if self.package_name:
            top_cg.add_package_name(self.package_name)

        with top_cg.class_definition(self.model_name):
            while len(self._subroutine_expr_queue):
                subroutine_code = self._process_next_subroutine()
                top_cg.add_code_lines(subroutine_code)

            if self.with_linear_algebra:
                filename = os.path.join(
                    os.path.dirname(__file__), "linear_algebra.java")
                top_cg.add_code_lines(utils.get_file_content(filename))

        return top_cg.code

    def _create_code_generator(self):
        return JavaCodeGenerator(indent=self.indent)

    # Methods to support ast.SubroutineExpr

    def interpret_subroutine_expr(self, expr, **kwargs):
        method_name = self._get_subroutine_name()
        return self._enqueue_subroutine(method_name, expr)

    def _enqueue_subroutine(self, name, expr):
        self._subroutine_expr_queue.append(Subroutine(name, expr.expr))
        return self._cg.method_invocation(name, self._feature_array_name)

    def _process_next_subroutine(self):
        subroutine = self._subroutine_expr_queue.pop(0)
        is_vector_output = subroutine.expr.is_vector_output

        self._cg = self._create_code_generator()

        with self._cg.method_definition(
                name=subroutine.name,
                args=[(True, self._feature_array_name)],
                is_vector_output=is_vector_output):
            last_result = self._do_interpret(subroutine.expr)
            self._cg.add_return_statement(last_result)

        return self._cg.code

    def _get_subroutine_name(self):
        subroutine_name = "subroutine" + str(self._subroutine_idx)
        self._subroutine_idx += 1
        return subroutine_name
