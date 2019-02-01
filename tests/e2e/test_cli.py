import pickle
import subprocess

from sklearn import linear_model

from tests import utils

expected_result = """
def  score(input):
    return (((((((((((((36.006810733650326) + ((input[0]) * (-0.10081655845910455))) + ((input[1]) * (0.044035569560798626))) + ((input[2]) * (0.030804434213339508))) + ((input[3]) * (2.9326736094672414))) + ((input[4]) * (-17.093360132148693))) + ((input[5]) * (3.7450682208635504))) + ((input[6]) * (0.0033774353698582506))) + ((input[7]) * (-1.4348015681660866))) + ((input[8]) * (0.2901581119428326))) + ((input[9]) * (-0.011463487956327852))) + ((input[10]) * (-0.9500012437313152))) + ((input[11]) * (0.010374330909981539))) + ((input[12]) * (-0.571389044929473))
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
