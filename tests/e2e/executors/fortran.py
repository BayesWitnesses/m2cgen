import os
from contextlib import contextmanager

import numpy as np

from m2cgen.assemblers import get_assembler_cls
from m2cgen.interpreters import FortranInterpreter

from tests import utils
from tests.e2e.executors.base import BaseExecutor

EXECUTOR_CODE_TPL = """
{model_code}

program main
    use Model
    implicit none
    integer, parameter :: max_input_dim = 10000
    integer :: i, j, io
    integer, parameter :: size = {size}
    double precision :: x
    double precision, dimension({size}) :: result
    double precision, dimension(max_input_dim) :: input

    open(10, file="{fname}", action='read')
    input(:) = 0.0d0
    i = 1
    do
        read(10,*,iostat=io) x
        if (io > 0) then
            write(*,*) 'Check input.  Something was wrong'
            exit
        else if (io < 0) then
            exit
        else
            input(i) = x
            i = i+1
        end if
    end do
    close(10)

    {print_code}

end program main
"""

EXECUTE_AND_PRINT_SCALAR = """
    result(1) = score(input)
    print '(e21.14)', result(1)
"""

EXECUTE_AND_PRINT_VECTOR_TPL = """
    result = score(input)
    print '({size}e21.14)', result  
    
"""


class FortranExecutor(BaseExecutor):

    def __init__(self, model):
        self.model_name = "score"
        self.model = model
        self.interpreter = FortranInterpreter()

        assembler_cls = get_assembler_cls(model)
        self.model_ast = assembler_cls(model).assemble()

        self.exec_path = None
        self._input_fname = None

    @contextmanager
    def do_predict(self, X):
        try:
            np.savetxt(self._input_fname, X)
            yield
        finally:
            os.remove(self._input_fname)

    def predict(self, X):
        exec_args = [str(self.exec_path)]

        with self.do_predict(X):
            prediction = utils.predict_from_commandline(exec_args)

        return prediction

    def prepare(self):
        if self.model_ast.output_size > 1:
            print_code = EXECUTE_AND_PRINT_VECTOR_TPL.format(
                size=self.model_ast.output_size)
        else:
            print_code = EXECUTE_AND_PRINT_SCALAR

        self._input_fname = f'{self._resource_tmp_dir}/readinput.dat'

        executor_code = EXECUTOR_CODE_TPL.format(
            model_code=self.interpreter.interpret(self.model_ast),
            print_code=print_code,
            size=self.model_ast.output_size,
            fname=self._input_fname
        )

        file_name = self._resource_tmp_dir / f"{self.model_name}.f90"
        utils.write_content_to_file(executor_code, file_name)

        self.exec_path = self._resource_tmp_dir / self.model_name
        flags = ["-ffree-line-length-none"]
        utils.execute_command([
            "gfortran",
            str(file_name),
            "-o",
            str(self.exec_path),
            *flags
        ])
