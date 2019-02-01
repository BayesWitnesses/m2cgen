import pickle
import subprocess

from sklearn import linear_model

from tests import utils

expected_result = """
def  score(input):
    return (((((((((((((36.00681073365041) + ((input[0]) * (-0.10081655845910313))) + ((input[1]) * (0.044035569560799306))) + ((input[2]) * (0.03080443421334909))) + ((input[3]) * (2.932673609467255))) + ((input[4]) * (-17.093360132149055))) + ((input[5]) * (3.745068220863573))) + ((input[6]) * (0.003377435369856338))) + ((input[7]) * (-1.4348015681660935))) + ((input[8]) * (0.2901581119428262))) + ((input[9]) * (-0.011463487956327553))) + ((input[10]) * (-0.9500012437313172))) + ((input[11]) * (0.010374330909981442))) + ((input[12]) * (-0.5713890449294712))
""".strip()  # NOQA


def execute_test(exec_args):
    result = subprocess.Popen(
        " ".join(exec_args), stdout=subprocess.PIPE, shell=True)
    actual_result = result.stdout.read().decode("utf-8").strip()
    assert actual_result == expected_result


def _prepare_pickled_model(tmp_path):
    p = tmp_path / "model.pickle"

    estimator = linear_model.LinearRegression()
    utils.train_model_regression(estimator)

    p.write_bytes(pickle.dumps(estimator))

    return p


def test_positional_arg(tmp_path):
    pickled_model_path = _prepare_pickled_model(tmp_path)
    exec_args = ["gen", "--language", "python", str(pickled_model_path)]
    execute_test(exec_args)


def test_override_input(tmp_path):
    pickled_model_path = _prepare_pickled_model(tmp_path)
    exec_args = ["gen", "--language", "python", "<", str(pickled_model_path)]
    execute_test(exec_args)


def test_piped(tmp_path):
    pickled_model_path = _prepare_pickled_model(tmp_path)
    exec_args = [
        "cat", str(pickled_model_path), " | ", "gen", "--language", "python"]
    execute_test(exec_args)
