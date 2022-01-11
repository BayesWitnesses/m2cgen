from platform import system

import pytest

from tests import utils


def execute_test(exec_args):
    generated_code = utils.execute_command(" ".join(exec_args), shell=True)
    utils.verify_python_model_is_expected(
        generated_code,
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        expected_output=-47.62913662138064)


def test_positional_arg(path_to_pickled_model):
    exec_args = ["m2cgen", "--language", "python", str(path_to_pickled_model)]
    execute_test(exec_args)


def test_override_input(path_to_pickled_model):
    exec_args = ["m2cgen", "--language", "python", "<", str(path_to_pickled_model)]
    execute_test(exec_args)


def test_piped(path_to_pickled_model):
    exec_args = [
        "type" if system() == "Windows" else "cat",
        str(path_to_pickled_model), "|", "m2cgen", "--language", "python"]
    execute_test(exec_args)


@pytest.mark.skip(reason="utils.verify_python_model_is_expected doesn't support modules")
def test_dash_m(path_to_pickled_model):
    exec_args = ["python", "-m", "m2cgen", "--language", "python", str(path_to_pickled_model)]
    execute_test(exec_args)
