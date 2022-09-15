import io
import sys
from unittest import mock

from _pytest import capture

from m2cgen import __version__, cli

from tests.utils import verify_python_model_is_expected


def _get_mock_args(
    indent=4,
    function_name=None,
    namespace=None,
    module_name=None,
    package_name=None,
    class_name=None,
    infile=None,
    language=None,
    lib="pickle"
):
    return mock.MagicMock(
        indent=indent,
        function_name=function_name,
        namespace=namespace,
        module_name=module_name,
        package_name=package_name,
        class_name=class_name,
        infile=infile,
        language=language,
        recursion_limit=cli.MAX_RECURSION_DEPTH,
        lib=lib)


def test_file_as_input(tmp_path):
    f = tmp_path / "hello.txt"
    f.write_text("123")

    input_args = ["-l", "python", str(f)]
    args = cli.parse_args(input_args)

    assert args.language == "python"
    assert isinstance(args.infile, io.BufferedReader)
    assert args.infile.name == str(f)


def test_stdin_as_input(request):
    input_args = ["--language", "python"]
    args = cli.parse_args(input_args)

    assert args.language == "python"

    # Since pytest by default captures stdin, but sometimes we need to disable
    # it (primarily for using (i)pdb), we have 2 different strategies to verify
    # that stdin was returned as infile.
    capturemanager = request.config.pluginmanager.getplugin("capturemanager")
    if capturemanager.is_globally_capturing():
        assert isinstance(args.infile, capture.DontReadFromInput)
    else:
        assert args.infile.name == "<stdin>"


@mock.patch.object(sys, "exit")
def test_language_is_required(mocked_exit):
    mocked_stderr = io.StringIO()

    with mock.patch.object(sys, "stderr", new=mocked_stderr):
        cli.parse_args([])

    assert "the following arguments are required: --language" in mocked_stderr.getvalue()
    mocked_exit.assert_called_with(2)


def test_generate_code(pickled_model):
    mock_args = _get_mock_args(infile=pickled_model, language="python")
    generated_code = cli.generate_code(mock_args)

    verify_python_model_is_expected(
        generated_code,
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        expected_output=-44.40540274041321)


def test_function_name(pickled_model):
    mock_args = _get_mock_args(infile=pickled_model, language="python", function_name="predict")
    generated_code = cli.generate_code(mock_args).strip()

    assert generated_code.startswith("def predict")


def test_function_name_csharp_default(pickled_model):
    mock_args = _get_mock_args(infile=pickled_model, language="c_sharp")
    generated_code = cli.generate_code(mock_args).strip()

    assert 'public static double Score' in generated_code


def test_class_name(pickled_model):
    mock_args = _get_mock_args(infile=pickled_model, language="java", class_name="TestClassName")
    generated_code = cli.generate_code(mock_args).strip()

    assert generated_code.startswith("public class TestClassName")


def test_package_name(pickled_model):
    mock_args = _get_mock_args(infile=pickled_model, language="java", package_name="foo.bar.baz")
    generated_code = cli.generate_code(mock_args).strip()

    assert generated_code.startswith("package foo.bar.baz;")


def test_module_name(pickled_model):
    mock_args = _get_mock_args(infile=pickled_model, language="visual_basic", module_name="TestModule")
    generated_code = cli.generate_code(mock_args).strip()

    assert generated_code.startswith("Module TestModule")


def test_namespace(pickled_model):
    mock_args = _get_mock_args(infile=pickled_model, language="c_sharp", namespace="Tests.ML")
    generated_code = cli.generate_code(mock_args).strip()

    assert "namespace Tests.ML {" in generated_code


def test_joblib_loading(pickled_model):
    mock_args = _get_mock_args(infile=pickled_model, language="go", lib="joblib")
    generated_code = cli.generate_code(mock_args).strip()

    assert generated_code.startswith("func score(input []float64) float64 {\n")


def test_indent(pickled_model):
    mock_args = _get_mock_args(infile=pickled_model, indent=0, language="c_sharp")
    generated_code = cli.generate_code(mock_args).strip()

    assert generated_code.startswith("""
namespace ML {
public static class Model {
public static double Score(double[] input) {
return
""".strip())


@mock.patch.object(sys, "exit")
def test_version(mocked_exit):
    mocked_stdout = io.StringIO()

    with mock.patch.object(sys, "stdout", new=mocked_stdout):
        cli.parse_args(["-v"])

    assert mocked_stdout.getvalue().strip() == f"m2cgen {__version__}"


def test_unsupported_args_are_ignored(pickled_model):
    mock_args = _get_mock_args(
        infile=pickled_model, language="python", class_name="TestClassName", package_name="foo.bar.baz")
    generated_code = cli.generate_code(mock_args)

    verify_python_model_is_expected(
        generated_code,
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        expected_output=-44.40540274041321)
