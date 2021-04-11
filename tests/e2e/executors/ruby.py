import os

from m2cgen import assemblers, interpreters
from tests import utils
from tests.e2e.executors.base import BaseExecutor

EXECUTOR_CODE_TPL = """
input_array = ARGV.map(&:to_f)

{model_code}

res = score(input_array)

{print_code}
"""

PRINT_SCALAR = """
puts res
"""

PRINT_VECTOR = """
puts res.join(" ")
"""


class RubyExecutor(BaseExecutor):
    model_name = "score"

    def __init__(self, model):
        self.model = model
        self.interpreter = interpreters.RubyInterpreter()

        assembler_cls = assemblers.get_assembler_cls(model)
        self.model_ast = assembler_cls(model).assemble()

        self._ruby = "ruby"

    def predict(self, X):
        file_name = os.path.join(self._resource_tmp_dir,
                                 f"{self.model_name}.rb")
        exec_args = [self._ruby,
                     file_name,
                     *map(utils.format_arg, X)]
        return utils.predict_from_commandline(exec_args)

    def prepare(self):
        if self.model_ast.output_size > 1:
            print_code = PRINT_VECTOR
        else:
            print_code = PRINT_SCALAR
        executor_code = EXECUTOR_CODE_TPL.format(
            model_code=self.interpreter.interpret(self.model_ast),
            print_code=print_code)

        file_name = os.path.join(
            self._resource_tmp_dir, f"{self.model_name}.rb")
        with open(file_name, "w") as f:
            f.write(executor_code)
