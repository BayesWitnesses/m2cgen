from m2cgen.assemblers import get_assembler_cls
from m2cgen.interpreters import DartInterpreter

from tests import utils
from tests.e2e.executors.base import BaseExecutor

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


class DartExecutor(BaseExecutor):

    def __init__(self, model):
        self.model_name = "score"
        self.model = model
        self.interpreter = DartInterpreter()

        assembler_cls = get_assembler_cls(model)
        self.model_ast = assembler_cls(model).assemble()

        self.script_path = None

    def predict(self, X):
        exec_args = [
            "dart",
            str(self.script_path),
            *map(utils.format_arg, X)
        ]
        return utils.predict_from_commandline(exec_args)

    def prepare(self):
        if self.model_ast.output_size > 1:
            print_code = EXECUTE_AND_PRINT_VECTOR
        else:
            print_code = EXECUTE_AND_PRINT_SCALAR

        executor_code = EXECUTOR_CODE_TPL.format(
            model_code=self.interpreter.interpret(self.model_ast),
            print_code=print_code)

        self.script_path = self._resource_tmp_dir / f"{self.model_name}.dart"
        utils.write_content_to_file(executor_code, self.script_path)
