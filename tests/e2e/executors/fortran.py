from m2cgen.assemblers import get_assembler_cls
from m2cgen.interpreters import CInterpreter

from tests import utils
from tests.e2e.executors.base import BaseExecutor

# TODO: All of this is still C...
EXECUTOR_CODE_TPL = """
{model_code}

progtam main
{{
    implicit none
    for (int i = 1; i < argc; ++i) {{
        sscanf(argv[i], "%lf", &input[i-1]);
    }}

    {print_code}

    return 0;
}}
"""

EXECUTE_AND_PRINT_SCALAR = """
    printf("%f\\n", score(input));
"""

EXECUTE_AND_PRINT_VECTOR_TPL = """
    double result[{size}];
    score(input, result);

    for (int i = 0; i < {size}; ++i) {{
        printf("%f ", *(result+i));
    }}
"""


class FortranExecutor(BaseExecutor):

    def __init__(self, model):
        self.model_name = "score"
        self.model = model
        self.interpreter = CInterpreter()

        assembler_cls = get_assembler_cls(model)
        self.model_ast = assembler_cls(model).assemble()

        self.exec_path = None

    def predict(self, X):
        exec_args = [str(self.exec_path), *map(utils.format_arg, X)]
        return utils.predict_from_commandline(exec_args)

    def prepare(self):
        if self.model_ast.output_size > 1:
            print_code = EXECUTE_AND_PRINT_VECTOR_TPL.format(
                size=self.model_ast.output_size)
        else:
            print_code = EXECUTE_AND_PRINT_SCALAR

        executor_code = EXECUTOR_CODE_TPL.format(
            model_code=self.interpreter.interpret(self.model_ast),
            print_code=print_code)

        file_name = self._resource_tmp_dir / f"{self.model_name}.c"
        utils.write_content_to_file(executor_code, file_name)

        self.exec_path = self._resource_tmp_dir / self.model_name
        flags = ["-std=c99", "-lm"]
        utils.execute_command([
            "gcc",
            str(file_name),
            "-o",
            str(self.exec_path),
            *flags
        ])
