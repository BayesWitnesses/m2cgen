from m2cgen.assemblers import get_assembler_cls
from m2cgen.interpreters import RustInterpreter

from tests import utils
from tests.e2e.executors.base import BaseExecutor

EXECUTOR_CODE_TPL = """
use std::env;

{model_code}

fn main() {{
    let args_raw: Vec<String> = env::args().collect::<Vec<String>>();
    let args: Vec<f64> = args_raw[1..].iter().flat_map(|x| x.parse::<f64>()).collect::<Vec<f64>>();
    {execute_code}
    println!("{{}}", res);
}}
"""

EXECUTE_SCALAR = """
    let res: f64 = score(args);
"""

EXECUTE_VECTOR = """
    let res_vec: Vec<f64> = score(args);
    let res: String = res_vec.iter().map(|&x| x.to_string()).collect::<Vec<String>>().join(" ");
"""


class RustExecutor(BaseExecutor):

    def __init__(self, model):
        self.model_name = "score"
        self.model = model
        self.interpreter = RustInterpreter()

        assembler_cls = get_assembler_cls(model)
        self.model_ast = assembler_cls(model).assemble()

        self.exec_path = None

    def predict(self, X):
        exec_args = [str(self.exec_path), *map(utils.format_arg, X)]
        return utils.predict_from_commandline(exec_args)

    def prepare(self):
        if self.model_ast.output_size > 1:
            execute_code = EXECUTE_VECTOR
        else:
            execute_code = EXECUTE_SCALAR

        executor_code = EXECUTOR_CODE_TPL.format(
            model_code=self.interpreter.interpret(self.model_ast),
            execute_code=execute_code)

        executor_file_name = self._resource_tmp_dir / f"{self.model_name}.rs"
        utils.write_content_to_file(executor_code, executor_file_name)
        self.exec_path = self._resource_tmp_dir / self.model_name
        utils.execute_command([
            "rustc",
            str(executor_file_name),
            "-o",
            str(self.exec_path)
        ])
