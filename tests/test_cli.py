from unittest import mock
from io import StringIO
import sys
from _pytest import capture

from m2cgen import cli


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
    mocked_stderr = StringIO()

    with mock.patch.object(sys, "stderr", new=mocked_stderr):
        cli.parse_args([])

    assert (
        "the following arguments are required: --language" in
        mocked_stderr.getvalue())

    mocked_exit.assert_called_with(2)
