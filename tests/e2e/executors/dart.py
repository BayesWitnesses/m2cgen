import os

from m2cgen import assemblers, interpreters
from tests import utils
from tests.e2e.executors import base

EXECUTOR_CODE_TPL = """
{model_code}

void main(List<String> args) {{
    List<double> input_ = args.map((x) => double.parse(x)).toList();
    {print_code}
}}
"""

EXECUTE_AND_PRINT_SCALAR = """
    double res = score(input_);
    print(res);
"""

EXECUTE_AND_PRINT_VECTOR = """
    List<double> res = score(input_);
    print(res.join(" "));
"""


class DartExecutor(base.BaseExecutor):

    executor_name = "score"

    def __init__(self, model):
        self.model = model
        self.interpreter = interpreters.DartInterpreter()

        assembler_cls = assemblers.get_assembler_cls(model)
        self.model_ast = assembler_cls(model).assemble()

        self._dart = "dart"

    def predict(self, X):
        file_name = os.path.join(self._resource_tmp_dir,
                                 f"{self.executor_name}.dart")
        exec_args = [self._dart,
                     file_name,
                     *map(interpreters.utils.format_float, X)]
        return utils.predict_from_commandline(exec_args)

    def prepare(self):
        if self.model_ast.output_size > 1:
            print_code = EXECUTE_AND_PRINT_VECTOR
        else:
            print_code = EXECUTE_AND_PRINT_SCALAR

        model_code = self.interpreter.interpret(self.model_ast)
        executor_code = EXECUTOR_CODE_TPL.format(
            model_code=model_code,
            print_code=print_code)

        executor_file_name = os.path.join(
            self._resource_tmp_dir, f"{self.executor_name}.dart")
        with open(executor_file_name, "w") as f:
            f.write(executor_code)
