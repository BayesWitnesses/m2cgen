import pickle
import subprocess

from sklearn import linear_model

from tests import utils

expected_result = """
def  score(input):
    return (((((((((((((36.0068107336504) + ((input[0]) * (-0.10081655845910333))) + ((input[1]) * (0.044035569560795046))) + ((input[2]) * (0.030804434213338117))) + ((input[3]) * (2.9326736094672468))) + ((input[4]) * (-17.09336013214845))) + ((input[5]) * (3.745068220863558))) + ((input[6]) * (0.0033774353698544472))) + ((input[7]) * (-1.4348015681660797))) + ((input[8]) * (0.29015811194282753))) + ((input[9]) * (-0.011463487956327451))) + ((input[10]) * (-0.950001243731317))) + ((input[11]) * (0.010374330909981468))) + ((input[12]) * (-0.5713890449294746))
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
        "cat", str(pickled_model_path), " | ", "m2cgen", "--language",
        "python"]
    execute_test(exec_args)
