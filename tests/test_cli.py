import pickle
import io
from unittest import mock
import sys
from _pytest import capture
from sklearn import linear_model

from m2cgen import cli
from tests import utils


def test_file_as_input(tmp_path):
    f = tmp_path / "hello.txt"
    f.write_text("123")

    args = ["--language", "python", str(f)]
    infile, language = cli.parse_args(args)

    assert language == "python"


def test_stdin_as_input(request):
    args = ["--language", "python"]
    infile, language = cli.parse_args(args)

    assert language == "python"

    # Since pytest by default captures stdin, but sometimes we need to disable
    # it (primarily for using (i)pdb), we have 2 different strategies to verify
    # that stdin was returned as infile.
    capturemanager = request.config.pluginmanager.getplugin("capturemanager")
    if capturemanager.is_globally_capturing():
        assert isinstance(infile, capture.DontReadFromInput)
    else:
        assert infile.name == "<stdin>"


@mock.patch.object(sys, "exit")
def test_language_is_required(mocked_exit):
    mocked_stderr = io.StringIO()

    with mock.patch.object(sys, "stderr", new=mocked_stderr):
        cli.parse_args([])

    assert (
        "the following arguments are required: --language" in
        mocked_stderr.getvalue())

    mocked_exit.assert_called_with(2)


def test_generate_code():
    expected_code = """
def  score(input):
    return (((((((((((((36.0068107336504) + ((input[0]) * (-0.10081655845910333))) + ((input[1]) * (0.044035569560795046))) + ((input[2]) * (0.030804434213338117))) + ((input[3]) * (2.9326736094672468))) + ((input[4]) * (-17.09336013214845))) + ((input[5]) * (3.745068220863558))) + ((input[6]) * (0.0033774353698544472))) + ((input[7]) * (-1.4348015681660797))) + ((input[8]) * (0.29015811194282753))) + ((input[9]) * (-0.011463487956327451))) + ((input[10]) * (-0.950001243731317))) + ((input[11]) * (0.010374330909981468))) + ((input[12]) * (-0.5713890449294746))
"""  # NOQA

    estimator = linear_model.LinearRegression()
    utils.train_model_regression(estimator)

    infile = io.BytesIO()

    pickle.dump(estimator, infile)
    infile.seek(0)

    actual_code = cli.generate_code(infile, "python")
    assert actual_code.strip() == expected_code.strip()
