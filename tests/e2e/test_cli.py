import pickle
import platform
import subprocess

from sklearn import linear_model

from tests import utils


def execute_test(exec_args, code_path=None):
    result = subprocess.Popen(
        " ".join(exec_args), stdout=subprocess.PIPE, shell=True)
    if code_path is None:
        generated_code = result.stdout.read().decode("utf-8")
    else:
        result.communicate()
        with open(code_path, encoding="utf-8") as f:
            generated_code = f.read()

    utils.verify_python_model_is_expected(
        generated_code,
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        expected_output=-41.89077994476439)


def _prepare_pickled_model(tmp_path):
    p = tmp_path / "model.pickle"

    estimator = linear_model.LinearRegression()
    utils.train_model_regression(estimator)

    p.write_bytes(pickle.dumps(estimator))

    return p


def test_positional_arg(tmp_path):
    pickled_model_path = _prepare_pickled_model(tmp_path)
    exec_args = ["m2cgen", "--language", "python", str(pickled_model_path)]
    execute_test(exec_args)


def test_override_input(tmp_path):
    pickled_model_path = _prepare_pickled_model(tmp_path)
    exec_args = [
        "m2cgen", "--language", "python", "<", str(pickled_model_path)]
    execute_test(exec_args)


def test_piped(tmp_path):
    pickled_model_path = _prepare_pickled_model(tmp_path)
    exec_args = [
        "type" if platform.system() in ('Windows', 'Microsoft') else "cat",
        str(pickled_model_path), " | ", "m2cgen", "--language", "python"]
    execute_test(exec_args)


def test_dash_m(tmp_path):
    pickled_model_path = _prepare_pickled_model(tmp_path)
    exec_args = ["python", "-m", "m2cgen", "--language", "python",
                 str(pickled_model_path)]
    execute_test(exec_args)


def test_write_file(tmp_path):
    pickled_model_path = _prepare_pickled_model(tmp_path)
    code_path = str(tmp_path / "code.txt")
    exec_args = ["m2cgen", "--language", "python",
                 "--output_file", code_path, str(pickled_model_path)]
    execute_test(exec_args, code_path=code_path)
